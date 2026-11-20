import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.database.session import get_db
from app.models.models import Question, QuestionAttempt, KnowledgeState, KnowledgeStateHistory, LearnerProfile, Streak, User
from app.schemas.schemas import QuestionResponse, QuestionSubmit, QuestionAttemptResult
from app.ml.bkt import bkt_engine
from app.ml.recommendation import recommendation_engine
from app.core.auth import resolve_learner_id, get_current_user_optional
from app.core.runner import execute_python_code, TestCase
from app.core.ws_manager import manager
from app.ml.dynamic_calibration import calibrate_concept_parameters

router = APIRouter(prefix="/api/questions", tags=["Questions"])

@router.get("", response_model=List[QuestionResponse])
def get_questions(concept_id: Optional[int] = None, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(Question)
    if concept_id:
        query = query.filter(Question.concept_id == concept_id)
    questions = query.limit(limit).all()
    return questions

@router.get("/next", response_model=QuestionResponse)
def get_next_question(
    learner_id: Optional[int] = None,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    resolved_id = resolve_learner_id(learner_id, current_user, db)
    recs = recommendation_engine.generate_recommendations(db, resolved_id, limit=3)
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
def submit_question_attempt(
    payload: QuestionSubmit,
    learner_id: Optional[int] = None,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    resolved_id = resolve_learner_id(learner_id, current_user, db)
    question = db.query(Question).filter(Question.id == payload.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    code_exec_result = None
    # Check if question is a coding question with live sandbox execution
    if question.question_type == "CODING" or payload.submitted_code:
        code_to_run = payload.submitted_code or payload.selected_option
        test_cases_objs = []
        if question.test_cases:
            for tc in question.test_cases:
                test_cases_objs.append(TestCase(input=tc.get("input", ""), expected_output=tc.get("expected_output", "")))

        runner_res = execute_python_code(code_to_run, test_cases_objs)
        code_exec_result = runner_res.model_dump()
        is_correct = runner_res.passed_all
        selected_text = code_to_run[:200]
    else:
        # Standard multiple choice / conceptual evaluation
        selected_text = payload.selected_option.strip() if payload.selected_option else ""
        is_correct = (selected_text == question.correct_answer.strip())

    # Get current knowledge state for learner & concept
    ks = db.query(KnowledgeState).filter(
        KnowledgeState.learner_id == resolved_id,
        KnowledgeState.concept_id == question.concept_id
    ).first()

    if not ks:
        ks = KnowledgeState(learner_id=resolved_id, concept_id=question.concept_id, mastery_probability=0.10)
        db.add(ks)
        db.flush()

    prior_p = ks.mastery_probability

    # Execute dynamic BKT Update with item-level calibration parameters
    prior, posterior = bkt_engine.update_knowledge(
        current_p_know=prior_p,
        is_correct=is_correct,
        difficulty=question.difficulty,
        response_time_sec=payload.response_time_seconds,
        item_slip=getattr(question, 'calibrated_slip', None),
        item_guess=getattr(question, 'calibrated_guess', None),
        item_difficulty_value=getattr(question, 'calibrated_difficulty', None)
    )

    # Persist Attempt
    attempt = QuestionAttempt(
        learner_id=resolved_id,
        question_id=question.id,
        session_id=payload.session_id,
        selected_option=selected_text,
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
        learner_id=resolved_id,
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
    streak_rec = db.query(Streak).filter(Streak.learner_id == resolved_id, Streak.date == today_str).first()
    if not streak_rec:
        db.add(Streak(learner_id=resolved_id, date=today_str, minimum_activity_completed=True))

    db.commit()

    # Dynamic EM calibration if attempts >= 5
    if ks.total_attempts >= 5 and ks.total_attempts % 3 == 0:
        try:
            calibrate_concept_parameters(db, question.concept_id)
        except Exception:
            pass

    # Broadcast real-time update via WebSocket
    ws_payload = {
        "event": "KNOWLEDGE_UPDATED",
        "learner_id": resolved_id,
        "concept_id": question.concept_id,
        "concept_code": question.concept.code if question.concept else "DSA",
        "concept_title": question.concept.title if question.concept else "Concept",
        "prior_mastery": round(prior, 3),
        "posterior_mastery": round(posterior, 3),
        "is_correct": is_correct,
        "status": bkt_engine.get_status_from_mastery(posterior)
    }
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(manager.broadcast_to_learner(resolved_id, ws_payload))
    except Exception:
        pass

    # Get dynamic next recommendation
    recs = recommendation_engine.generate_recommendations(db, resolved_id, limit=1)
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
        code_execution_result=code_exec_result,
        next_recommendation=next_rec
    )
