from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database.session import get_db
from app.models.models import KnowledgeState, KnowledgeStateHistory, Concept
from app.schemas.schemas import KnowledgeStateResponse, KnowledgeHistoryPoint
from app.ml.bkt import BKTEngine

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge"])

@router.get("/states", response_model=List[KnowledgeStateResponse])
def get_knowledge_states(learner_id: int = 1, db: Session = Depends(get_db)):
    states = db.query(KnowledgeState).filter(KnowledgeState.learner_id == learner_id).all()
    results = []
    for s in states:
        c = s.concept
        results.append(KnowledgeStateResponse(
            concept_id=s.concept_id,
            concept_code=c.code if c else "",
            concept_title=c.title if c else "",
            mastery_probability=round(s.mastery_probability, 3),
            status=BKTEngine.get_status_from_mastery(s.mastery_probability, True),
            total_attempts=s.total_attempts,
            correct_attempts=s.correct_attempts,
            last_updated=s.last_updated
        ))
    return results

@router.get("/history/{concept_id}", response_model=List[KnowledgeHistoryPoint])
def get_knowledge_history(concept_id: int, learner_id: int = 1, db: Session = Depends(get_db)):
    history = db.query(KnowledgeStateHistory).filter(
        KnowledgeStateHistory.learner_id == learner_id,
        KnowledgeStateHistory.concept_id == concept_id
    ).order_by(KnowledgeStateHistory.timestamp.asc()).all()

    c = db.query(Concept).get(concept_id)
    code = c.code if c else "DSA"

    return [
        KnowledgeHistoryPoint(
            timestamp=h.timestamp.strftime("%Y-%m-%d %H:%M"),
            mastery_probability=round(h.mastery_probability, 3),
            concept_code=code,
            change_delta=round(h.change_delta, 3)
        ) for h in history
    ]
