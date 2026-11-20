from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database.session import get_db
from app.models.models import Concept, ConceptPrerequisite, KnowledgeState, Question
from app.schemas.schemas import ConceptResponse
from app.ml.bkt import BKTEngine

router = APIRouter(prefix="/api/concepts", tags=["Concepts"])

@router.get("", response_model=List[ConceptResponse])
def list_concepts(learner_id: int = 1, db: Session = Depends(get_db)):
    concepts = db.query(Concept).order_by(Concept.display_order).all()
    k_states = {
        ks.concept_id: ks for ks in db.query(KnowledgeState).filter(KnowledgeState.learner_id == learner_id).all()
    }
    prereqs = db.query(ConceptPrerequisite).all()
    prereq_map = {}
    for p in prereqs:
        if p.concept_id not in prereq_map:
            prereq_map[p.concept_id] = []
        prereq_map[p.concept_id].append(p)

    q_counts = dict(
        db.query(Question.concept_id, func.count(Question.id)).group_by(Question.concept_id).all()
    )

    results = []
    for c in concepts:
        ks = k_states.get(c.id)
        mastery = ks.mastery_probability if ks else 0.10

        is_unlocked = True
        for p in prereq_map.get(c.id, []):
            if p.prerequisite_id not in q_counts:
                continue
            p_ks = k_states.get(p.prerequisite_id)
            p_mastery = p_ks.mastery_probability if p_ks else 0.10
            if p_mastery < p.minimum_mastery:
                is_unlocked = False

        status = BKTEngine.get_status_from_mastery(mastery, is_unlocked)

        res = ConceptResponse.from_orm(c)
        res.mastery_probability = round(mastery, 3)
        res.status = status
        results.append(res)

    return results

@router.get("/{code}", response_model=ConceptResponse)
def get_concept(code: str, learner_id: int = 1, db: Session = Depends(get_db)):
    c = db.query(Concept).filter(Concept.code == code.upper()).first()
    if not c:
        raise HTTPException(status_code=404, detail=f"Concept {code} not found")

    ks = db.query(KnowledgeState).filter(
        KnowledgeState.learner_id == learner_id,
        KnowledgeState.concept_id == c.id
    ).first()

    mastery = ks.mastery_probability if ks else 0.10
    res = ConceptResponse.from_orm(c)
    res.mastery_probability = round(mastery, 3)
    res.status = BKTEngine.get_status_from_mastery(mastery, True)
    return res
