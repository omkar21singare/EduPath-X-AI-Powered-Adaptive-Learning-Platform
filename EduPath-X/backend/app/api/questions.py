from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database.session import get_db
from app.models.models import Question, QuestionAttempt, KnowledgeState, KnowledgeStateHistory, LearnerProfile, Streak
from app.schemas.schemas import QuestionResponse, QuestionSubmit, QuestionAttemptResult
from app.ml.bkt import bkt_engine
from app.ml.recommendation import recommendation_engine

router = APIRouter(prefix="/api/questions", tags=["Questions"])

@router.get("", response_model=List[QuestionResponse])
def get_questions(concept_id: Optional[int] = None, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(Question)
    if concept_id:
        query = query.filter(Question.concept_id == concept_id)
    questions = query.limit(limit).all()
    return questions

@router.get("/next", response_model=QuestionResponse)
def get_next_question(learner_id: int = 1, db: Session = Depends(get_db)):
    recs = recommendation_engine.generate_recommendations(db, learner_id, limit=3)
    if not recs:
        q = db.query(Question).first()
        if not q:
            raise HTTPException(status_code=404, detail="No questions available")
        return q

    for rec in recs:
        concept_id = rec["concept_id"]
        action = rec["action_type"]
        
        diff_target = "Medium"
        if action in ["LEARN", "REVISE"]:
            diff_target = "Easy"
        elif action == "CHALLENGE":
            diff_target = "Hard"
            
        q = db.query(Question).filter(Question.concept_id == concept_id, Question.difficulty == diff_target).first()
        if q: return q
        q = db.query(Question).filter(Question.concept_id == concept_id).first()
        if q: return q
            
    q = db.query(Question).first()
    if not q:
        raise HTTPException(status_code=404, detail="No questions available")
    return q

@router.post("/submit", response_model=QuestionAttemptResult)
def submit_question_attempt(payload: QuestionSubmit, learner_id: int = 1, db: Session = Depends(get_db)):
    question = db.query(Question).get(payload.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = (payload.selected_option.strip() == question.correct_answer.strip())

    # Get current knowledge state for learner & concept
    ks = db.query(KnowledgeState).filter(
        KnowledgeState.learner_id == learner_id,
        KnowledgeState.concept_id == question.concept_id
    ).first()

    if not ks:
        ks = KnowledgeState(learner_id=learner_id, concept_id=question.concept_id, mastery_probability=0.10)
        db.add(ks)
        db.flush()

    prior_p = ks.mastery_probability

    # Execute BKT Update
    prior, posterior = bkt_engine.update_knowledge(
        current_p_know=prior_p,
        is_correct=is_correct,
        difficulty=question.difficulty,
        response_time_sec=payload.response_time_seconds
    )

    # Persist Attempt
    attempt = QuestionAttempt(
        learner_id=learner_id,
        question_id=question.id,
        session_id=payload.session_id,
        selected_option=payload.selected_option,
        is_correct=is_correct,
        response_time_seconds=payload.response_time_seconds,
        bkt_prior=prior,
        bkt_posterior=posterior,
        timestamp=datetime.utcnow()
    )
    db.add(attempt)

    # Update KnowledgeState
    ks.mastery_probability = posterior
    ks.total_attempts += 1
    if is_correct:
        ks.correct_attempts += 1
    ks.last_updated = datetime.utcnow()

    # Log History
    history = KnowledgeStateHistory(
        learner_id=learner_id,
        concept_id=question.concept_id,
        timestamp=datetime.utcnow(),
        mastery_probability=posterior,
        evidence_type="QUESTION_ATTEMPT",
        session_id=payload.session_id,
        change_delta=posterior - prior
    )
    db.add(history)

    # Update Streak for Today
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    streak_rec = db.query(Streak).filter(Streak.learner_id == learner_id, Streak.date == today_str).first()
    if not streak_rec:
        db.add(Streak(learner_id=learner_id, date=today_str, minimum_activity_completed=True))

    db.commit()

    # Get dynamic next recommendation
    recs = recommendation_engine.generate_recommendations(db, learner_id, limit=1)
    next_rec = recs[0] if recs else None

    return QuestionAttemptResult(
        attempt_id=attempt.id,
        question_id=question.id,
        is_correct=is_correct,
        correct_answer=question.correct_answer,
        explanation=question.explanation,
        bkt_prior=round(prior, 3),
        bkt_posterior=round(posterior, 3),
        mastery_change=round(posterior - prior, 3),
        concept_code=question.concept.code if question.concept else "DSA",
        next_recommendation=next_rec
    )
