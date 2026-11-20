from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database.session import get_db
from app.ml.recommendation import recommendation_engine
from app.models.models import Concept, KnowledgeState, Question, ConceptPrerequisite, LearningGoal

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("", response_model=List[Dict[str, Any]])
def get_recommendations(learner_id: int = 1, limit: int = 5, db: Session = Depends(get_db)):
    return recommendation_engine.generate_recommendations(db, learner_id, limit=limit)

@router.get("/explain/{concept_id}")
def explain_recommendation(concept_id: int, learner_id: int = 1, db: Session = Depends(get_db)):
    recs = recommendation_engine.generate_recommendations(db, learner_id, limit=20)
    for r in recs:
        if r["concept_id"] == concept_id:
            return r

    concept = db.query(Concept).get(concept_id)
    if not concept:
        return {
            "concept_id": concept_id,
            "action_type": "UNKNOWN",
            "reason_text": "Concept not found in curriculum.",
            "rationale": {}
        }

    ks = db.query(KnowledgeState).filter(
        KnowledgeState.learner_id == learner_id,
        KnowledgeState.concept_id == concept_id
    ).first()
    mastery = ks.mastery_probability if ks else 0.10
    q_count = db.query(Question).filter(Question.concept_id == concept_id).count()

    # Prerequisite verification
    prereqs = db.query(ConceptPrerequisite).filter(ConceptPrerequisite.concept_id == concept_id).all()
    prereq_details = []
    all_met = True
    for p in prereqs:
        p_ks = db.query(KnowledgeState).filter(
            KnowledgeState.learner_id == learner_id,
            KnowledgeState.concept_id == p.prerequisite_id
        ).first()
        p_mastery = p_ks.mastery_probability if p_ks else 0.10
        p_concept = db.query(Concept).get(p.prerequisite_id)
        p_title = p_concept.title if p_concept else f"Concept #{p.prerequisite_id}"
        is_met = p_mastery >= p.minimum_mastery
        if not is_met:
            all_met = False
        prereq_details.append({
            "parent_title": p_title,
            "parent_mastery": round(p_mastery * 100, 1),
            "required_mastery": round(p.minimum_mastery * 100, 1),
            "is_met": is_met
        })

    # Check goal
    active_goal = db.query(LearningGoal).filter(
        LearningGoal.learner_id == learner_id,
        LearningGoal.status == "ACTIVE"
    ).order_by(LearningGoal.id.desc()).first()

    goal_info = None
    if active_goal:
        is_goal_concept = (active_goal.concept_id == concept.id) or (active_goal.concept_id is None)
        goal_info = {
            "id": active_goal.id,
            "goal_name": active_goal.goal_name,
            "target_mastery": round((active_goal.target_mastery or 0.8) * 100, 1),
            "is_direct_goal_concept": is_goal_concept,
            "status": active_goal.status
        }

    if q_count == 0:
        return {
            "concept_id": concept.id,
            "concept_code": concept.code,
            "concept_title": concept.title,
            "action_type": "STUDY_MATERIAL",
            "target_difficulty": "Introductory",
            "current_mastery": round(mastery * 100, 1),
            "prerequisites_met": all_met,
            "prerequisite_details": prereq_details,
            "reason_text": f"Study verified reference material for {concept.title}. Practice questions are currently in content review.",
            "rationale": {"available_questions": 0},
            "active_goal": goal_info
        }

    return {
        "concept_id": concept.id,
        "concept_code": concept.code,
        "concept_title": concept.title,
        "action_type": "LOCKED" if not all_met else "PRACTICE",
        "target_difficulty": "Prerequisites Required" if not all_met else "Medium",
        "current_mastery": round(mastery * 100, 1),
        "prerequisites_met": all_met,
        "prerequisite_details": prereq_details,
        "reason_text": f"{concept.title} is currently locked pending prerequisite mastery completion." if not all_met else f"Standard practice recommended for {concept.title}.",
        "rationale": {"available_questions": q_count},
        "active_goal": goal_info
    }
