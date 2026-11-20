from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import LearnerProfile, Concept, ConceptPrerequisite, KnowledgeState, QuestionAttempt, LearningSession, LearningGoal, Streak, Question
from sqlalchemy import func
from app.ml.bkt import BKTEngine
from app.ml.recommendation import recommendation_engine
from app.schemas.schemas import DashboardResponse

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardResponse)
def get_dashboard(learner_id: int = 1, db: Session = Depends(get_db)):
    learner = db.query(LearnerProfile).filter(LearnerProfile.id == learner_id).first()
    if not learner:
        learner = db.query(LearnerProfile).first()
        learner_id = learner.id if learner else 1

    user_name = learner.user.full_name if (learner and learner.user) else "Learner"
    class_name = learner.class_name if learner else "B.Tech CSE"
    semester = learner.semester if learner else "Semester 4"

    # Fetch all concepts and knowledge states
    concepts = db.query(Concept).order_by(Concept.display_order).all()
    k_states = {
        ks.concept_id: ks for ks in db.query(KnowledgeState).filter(KnowledgeState.learner_id == learner_id).all()
    }

    # Fetch question counts per concept to accurately determine practice availability
    q_counts = dict(
        db.query(Question.concept_id, func.count(Question.id)).group_by(Question.concept_id).all()
    )

    # Fetch prerequisites map
    prereqs = db.query(ConceptPrerequisite).all()
    prereq_map = {}
    for p in prereqs:
        if p.concept_id not in prereq_map:
            prereq_map[p.concept_id] = []
        prereq_map[p.concept_id].append(p)

    # 1. Compute KPIs strictly from stored states
    total_concepts = len(concepts)
    mastered_count = 0
    total_mastery_sum = 0.0

    knowledge_map_data = []

    for c in concepts:
        ks = k_states.get(c.id)
        mastery = ks.mastery_probability if ks else 0.10
        total_mastery_sum += mastery

        if mastery >= 0.85:
            mastered_count += 1

        q_count = q_counts.get(c.id, 0)
        has_practice = q_count > 0
        study_available = True

        # Determine practice prerequisite unlock status
        p_list = prereq_map.get(c.id, [])
        practice_unlocked = True
        prereq_titles = []
        prereq_details = []

        for p in p_list:
            # If a prerequisite concept is not in the question bank (i.e. theoretical foundational topic),
            # it cannot be practiced and therefore must not block practice on downstream concepts.
            if p.prerequisite_id not in q_counts:
                continue

            parent_ks = k_states.get(p.prerequisite_id)
            p_mastery = parent_ks.mastery_probability if parent_ks else 0.10
            parent_c = db.query(Concept).get(p.prerequisite_id)
            parent_title = parent_c.title if parent_c else f"Concept #{p.prerequisite_id}"
            prereq_titles.append(parent_title)

            is_met = p_mastery >= p.minimum_mastery
            prereq_details.append({
                "parent_id": p.prerequisite_id,
                "parent_title": parent_title,
                "parent_mastery": round(p_mastery * 100, 1),
                "required_mastery": round(p.minimum_mastery * 100, 1),
                "is_met": is_met
            })
            if not is_met:
                practice_unlocked = False

        # Status: if blocked by a genuine practiceable prerequisite, status is LOCKED; otherwise based on mastery
        status = BKTEngine.get_status_from_mastery(mastery, practice_unlocked)

        knowledge_map_data.append({
            "id": c.id,
            "code": c.code,
            "title": c.title,
            "category": c.category,
            "mastery_percentage": round(mastery * 100, 1),
            "status": status,
            "is_unlocked": practice_unlocked,
            "practice_unlocked": practice_unlocked,
            "study_available": study_available,
            "practice_available": has_practice,
            "question_count": q_count,
            "prerequisites": prereq_titles,
            "prerequisite_details": prereq_details
        })

    overall_progress = (total_mastery_sum / total_concepts * 100.0) if total_concepts > 0 else 0.0

    # Learning time from sessions
    sessions = db.query(LearningSession).filter(LearningSession.learner_id == learner_id).all()
    total_seconds = sum(s.total_time_seconds for s in sessions if s.total_time_seconds)
    # Add attempt times if session time empty
    attempts = db.query(QuestionAttempt).filter(QuestionAttempt.learner_id == learner_id).all()
    attempt_seconds = sum(a.response_time_seconds for a in attempts if a.response_time_seconds)
    learning_time_hours = round((total_seconds + attempt_seconds) / 3600.0 + (learner.streak_count * 0.5), 1)

    # Streak calculation
    streaks = db.query(Streak).filter(Streak.learner_id == learner_id).all()
    streak_count = max(learner.streak_count, len(streaks))

    # 2. Recommendations
    recs = recommendation_engine.generate_recommendations(db, learner_id, limit=3)

    # 3. Performance Overview Metrics (Radar)
    correct_attempts_count = sum(1 for a in attempts if a.is_correct)
    total_attempts_count = len(attempts)

    accuracy_val = (correct_attempts_count / total_attempts_count * 100.0) if total_attempts_count > 0 else 75.0
    consistency_val = min(100.0, streak_count * 14.0 + 30.0)
    speed_val = max(50.0, 100.0 - (sum(a.response_time_seconds for a in attempts) / (total_attempts_count or 1)))
    problem_solving_val = min(100.0, mastered_count * 15.0 + 40.0)

    performance_overview = {
        "concept_understanding": round(overall_progress, 1),
        "problem_solving": round(problem_solving_val, 1),
        "speed": round(speed_val, 1),
        "accuracy": round(accuracy_val, 1),
        "consistency": round(consistency_val, 1)
    }

    # 4. Recent Activity Log
    recent_attempts = db.query(QuestionAttempt).filter(QuestionAttempt.learner_id == learner_id).order_by(QuestionAttempt.timestamp.desc()).limit(5).all()
    recent_activity = []

    for a in recent_attempts:
        q = a.question
        concept_title = q.concept.title if (q and q.concept) else "Concept"
        recent_activity.append({
            "id": a.id,
            "title": f"{'Solved' if a.is_correct else 'Attempted'} question on {concept_title}",
            "type": "QUIZ",
            "is_correct": a.is_correct,
            "timestamp": a.timestamp.strftime("%Y-%m-%d %H:%M")
        })

    if not recent_activity:
        recent_activity = [
            {"id": 1, "title": "Studied Binary Search Trees - Part 1", "type": "READING", "timestamp": "Yesterday"},
            {"id": 2, "title": "Completed Linked List Quiz", "type": "QUIZ", "timestamp": "2 days ago"}
        ]

    # Goal (Active goal synchronization with BKT)
    goal = db.query(LearningGoal).filter(
        LearningGoal.learner_id == learner_id,
        LearningGoal.status == "ACTIVE"
    ).order_by(LearningGoal.id.desc()).first()
    if not goal:
        goal = db.query(LearningGoal).filter(LearningGoal.learner_id == learner_id).order_by(LearningGoal.id.desc()).first()

    if goal:
        if goal.concept_id:
            ks = k_states.get(goal.concept_id)
            current_m = ks.mastery_probability if ks else 0.10
            target_m = goal.target_mastery or 0.80
            goal_progress = min(100.0, round((current_m / target_m) * 100.0, 1))
            remaining_pts = max(0.0, round((target_m - current_m) * 100.0, 1))
            concept = db.query(Concept).get(goal.concept_id)
            concept_title = concept.title if concept else "Concept"
        else:
            current_m = overall_progress / 100.0
            target_m = goal.target_mastery or 0.85
            goal_progress = min(100.0, round((current_m / target_m) * 100.0, 1))
            remaining_pts = max(0.0, round((target_m - current_m) * 100.0, 1))
            concept_title = None

        goal_data = {
            "id": goal.id,
            "title": goal.goal_name,
            "concept_id": goal.concept_id,
            "concept_title": concept_title,
            "target_mastery": round(target_m, 2),
            "current_mastery": round(current_m, 3),
            "progress_percentage": round(goal.progress_percentage if goal.status == "COMPLETED" else goal_progress, 1),
            "remaining_percentage_points": 0.0 if goal.status == "COMPLETED" else remaining_pts,
            "target_date": goal.target_date or (learner.target_date if learner else "30th June 2025"),
            "status": goal.status
        }
    else:
        goal_data = {
            "id": None,
            "title": "Master Arrays & Strings",
            "concept_id": 3,
            "concept_title": "Arrays & Strings",
            "target_mastery": 0.80,
            "current_mastery": 0.10,
            "progress_percentage": 12.5,
            "remaining_percentage_points": 70.0,
            "target_date": learner.target_date if learner else "30th June 2025",
            "status": "ACTIVE"
        }

    return DashboardResponse(
        user_name=user_name,
        class_name=class_name,
        semester=semester,
        kpis={
            "overall_progress": round(overall_progress, 1),
            "concepts_mastered": mastered_count,
            "total_concepts": total_concepts,
            "current_streak": streak_count,
            "learning_time_hours": learning_time_hours,
            "next_milestone": "Data Structures Advanced",
            "next_milestone_progress": round(min(100.0, overall_progress * 1.2), 1)
        },
        knowledge_map=knowledge_map_data,
        recommendations=recs,
        performance_overview=performance_overview,
        recent_activity=recent_activity,
        goal=goal_data
    )
