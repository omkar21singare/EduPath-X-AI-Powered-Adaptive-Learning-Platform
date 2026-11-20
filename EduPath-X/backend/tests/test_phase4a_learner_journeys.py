import pytest
from app.database.session import SessionLocal
from app.models.models import User, LearnerProfile, LearningGoal, Concept, KnowledgeState, Question, QuestionAttempt
from app.api.goals import create_or_update_goal, submit_goal_progress, get_active_goal, get_goals
from app.schemas.schemas import GoalCreate, QuestionSubmit
from app.api.questions import submit_question_attempt
from app.ml.recommendation import recommendation_engine

@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()

def test_goal_model_and_uniqueness_protection(db):
    """
    PART 4 & PART 6:
    Verify exactly one active goal exists for that learner/concept,
    and repeated UI submission does not duplicate records.
    """
    learner_id = 1
    concept_id = 3 # Arrays & Strings

    # 1. Create Goal
    payload1 = GoalCreate(concept_id=concept_id, target_mastery=0.80, goal_name="Master Arrays")
    goal1 = create_or_update_goal(payload1, learner_id=learner_id, db=db)
    assert goal1.id is not None
    assert goal1.concept_id == concept_id
    assert goal1.status in ["ACTIVE", "COMPLETED"]

    # 2. Attempt to create duplicate goal for the same concept
    payload2 = GoalCreate(concept_id=concept_id, target_mastery=0.85, goal_name="Master Arrays Enhanced")
    goal2 = create_or_update_goal(payload2, learner_id=learner_id, db=db)
    assert goal2.id == goal1.id, "Expected existing goal to be updated idempotently, not duplicated!"
    assert goal2.target_mastery == 0.85

    # 3. Verify exactly one active goal exists for this learner & concept in DB
    active_goals = db.query(LearningGoal).filter(
        LearningGoal.learner_id == learner_id,
        LearningGoal.concept_id == concept_id,
        LearningGoal.status == "ACTIVE"
    ).all()
    assert len(active_goals) <= 1, "There must be at most one active goal for the concept."

def test_repeated_submission_protection(db):
    """
    PART 6:
    Test:
    1. Create goal.
    2. Submit progress.
    3. Submit progress again.
    4. Refresh page (re-query).
    5. Submit progress again.
    6. Answer another question.
    7. Submit progress again.
    Verify idempotency and true BKT derivation.
    """
    learner_id = 1
    concept_id = 3

    # Reset mastery for concept to baseline 0.20 for deterministic test
    ks = db.query(KnowledgeState).filter(KnowledgeState.learner_id == learner_id, KnowledgeState.concept_id == concept_id).first()
    if not ks:
        ks = KnowledgeState(learner_id=learner_id, concept_id=concept_id, mastery_probability=0.20)
        db.add(ks)
    else:
        ks.mastery_probability = 0.20
    db.commit()

    # 1. Create goal
    goal = create_or_update_goal(GoalCreate(concept_id=concept_id, target_mastery=0.80), learner_id=learner_id, db=db)
    initial_progress = goal.progress_percentage

    # 2. Submit progress
    p1 = submit_goal_progress(goal.id, db=db)
    # 3. Submit progress again
    p2 = submit_goal_progress(goal.id, db=db)
    assert p1.progress_percentage == p2.progress_percentage, "Progress must be identical without new interactions!"
    assert p1.current_mastery == p2.current_mastery

    # 4. Refresh / Re-query
    refreshed_goal = get_active_goal(learner_id=learner_id, db=db)
    assert refreshed_goal is not None
    assert refreshed_goal.concept_id == concept_id

    # 5. Submit progress again
    p3 = submit_goal_progress(goal.id, db=db)
    assert p3.progress_percentage == p2.progress_percentage

    # 6. Answer a question correctly on concept 3
    q = db.query(Question).filter(Question.concept_id == concept_id).first()
    assert q is not None, "Need at least one question for concept"
    attempt = submit_question_attempt(
        QuestionSubmit(question_id=q.id, selected_option=q.correct_answer, response_time_seconds=15.0),
        learner_id=learner_id,
        db=db
    )
    assert attempt.is_correct is True
    assert attempt.bkt_posterior > attempt.bkt_prior

    # 7. Submit progress again
    p4 = submit_goal_progress(goal.id, db=db)
    assert p4.current_mastery == round(attempt.bkt_posterior, 3)
    assert p4.progress_percentage > p3.progress_percentage, "Goal progress must increase after BKT posterior increase!"

def test_controlled_learner_journeys(db):
    """
    PART 2:
    Controlled journeys for 3 learner profiles:
    1. Fast learner (high accuracy, rapid progression to completion)
    2. Average learner (mixed responses, steady advancement)
    3. Struggling learner (low accuracy, stays in remediation)
    """
    concept_id = 3 # Arrays & Strings
    questions = db.query(Question).filter(Question.concept_id == concept_id).all()
    assert len(questions) >= 4

    profiles = [
        {"name": "Fast Learner", "accuracy_sequence": [True, True, True, True]},
        {"name": "Average Learner", "accuracy_sequence": [True, False, True, True]},
        {"name": "Struggling Learner", "accuracy_sequence": [False, False, False, True]},
    ]

    journey_records = {}

    for profile in profiles:
        pname = profile["name"]
        # Reset learner state
        ks = db.query(KnowledgeState).filter(KnowledgeState.learner_id == 1, KnowledgeState.concept_id == concept_id).first()
        ks.mastery_probability = 0.15
        ks.total_attempts = 0
        ks.correct_attempts = 0
        db.commit()

        # Create fresh active goal
        goal = create_or_update_goal(GoalCreate(concept_id=concept_id, target_mastery=0.80), learner_id=1, db=db)

        history = []
        for step_idx, is_correct in enumerate(profile["accuracy_sequence"]):
            # Check recommendation before action
            recs = recommendation_engine.generate_recommendations(db, 1, limit=3)
            assert len(recs) > 0, "Recommendation engine must return eligible concepts!"
            top_rec = recs[0]
            assert top_rec["concept_id"] in [3, 4, 5, 9, 12], "Must only recommend concepts with practice questions!"

            # Select question (repeated or sequential)
            q = questions[step_idx % len(questions)]
            selected_ans = q.correct_answer if is_correct else (q.options[1] if q.options[1] != q.correct_answer else q.options[0])

            # Submit answer
            res = submit_question_attempt(
                QuestionSubmit(question_id=q.id, selected_option=selected_ans, response_time_seconds=15.0),
                learner_id=1,
                db=db
            )

            # Update goal progress
            g_state = submit_goal_progress(goal.id, db=db)

            history.append({
                "step": step_idx + 1,
                "rec_action": top_rec["action_type"],
                "target_difficulty": top_rec.get("target_difficulty", "Medium"),
                "is_correct": is_correct,
                "bkt_prior": res.bkt_prior,
                "bkt_posterior": res.bkt_posterior,
                "goal_progress_pct": g_state.progress_percentage,
                "goal_status": g_state.status
            })

        journey_records[pname] = history

    # Verifications for Fast Learner
    fast_hist = journey_records["Fast Learner"]
    assert fast_hist[-1]["bkt_posterior"] > fast_hist[0]["bkt_prior"]
    assert fast_hist[-1]["goal_progress_pct"] > fast_hist[0]["goal_progress_pct"]
    assert fast_hist[-1]["bkt_posterior"] >= 0.70

    # Verifications for Struggling Learner
    struggle_hist = journey_records["Struggling Learner"]
    assert struggle_hist[2]["bkt_posterior"] < 0.20, "Successive incorrect answers should keep mastery depressed."
    assert struggle_hist[2]["rec_action"] in ["LEARN", "REVISE"], "Struggling learner should receive revision or foundational actions."

    # Average Learner has moderate progress
    avg_hist = journey_records["Average Learner"]
    assert avg_hist[-1]["bkt_posterior"] > struggle_hist[-1]["bkt_posterior"]
