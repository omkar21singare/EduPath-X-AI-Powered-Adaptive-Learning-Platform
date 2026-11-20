from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database.session import get_db
from app.models.models import QuestionAttempt

router = APIRouter(prefix="/api/attempts", tags=["Attempts"])

@router.get("/history", response_model=List[Dict[str, Any]])
def get_attempt_history(learner_id: int = 1, limit: int = 20, db: Session = Depends(get_db)):
    attempts = db.query(QuestionAttempt).filter(
        QuestionAttempt.learner_id == learner_id
    ).order_by(QuestionAttempt.timestamp.desc()).limit(limit).all()

    result = []
    for a in attempts:
        q = a.question
        concept_title = q.concept.title if (q and q.concept) else "General"
        result.append({
            "id": a.id,
            "question_text": q.question_text if q else "Question",
            "concept_title": concept_title,
            "selected_option": a.selected_option,
            "is_correct": a.is_correct,
            "bkt_prior": round(a.bkt_prior, 3),
            "bkt_posterior": round(a.bkt_posterior, 3),
            "timestamp": a.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return result
