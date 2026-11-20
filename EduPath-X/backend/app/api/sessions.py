from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any
from app.database.session import get_db
from app.models.models import LearningSession, Concept, LearningMaterial, Question
from app.ml.recommendation import recommendation_engine

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])

@router.post("/start")
def start_adaptive_session(session_type: str = "ADAPTIVE", learner_id: int = 1, db: Session = Depends(get_db)):
    # Get top recommendation
    recs = recommendation_engine.generate_recommendations(db, learner_id, limit=1)
    if not recs:
        # Pick default concept
        concept = db.query(Concept).first()
        rec_data = {
            "concept_id": concept.id,
            "concept_code": concept.code,
            "concept_title": concept.title,
            "action_type": "PRACTICE",
            "reason_text": "Default practice session.",
            "rationale": {}
        }
    else:
        rec_data = recs[0]

    session = LearningSession(
        learner_id=learner_id,
        session_type=session_type,
        started_at=datetime.utcnow()
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # Material & questions for target concept
    concept_id = rec_data["concept_id"]
    material = db.query(LearningMaterial).filter(LearningMaterial.concept_id == concept_id).first()
    questions = db.query(Question).filter(Question.concept_id == concept_id).all()

    return {
        "session_id": session.id,
        "recommendation": rec_data,
        "material": material,
        "questions": questions[:5]
    }
