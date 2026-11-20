from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database.session import get_db
from app.models.models import LearningGoal, LearnerProfile, Concept, KnowledgeState
from app.schemas.schemas import GoalCreate, GoalResponse

router = APIRouter(prefix="/api/goals", tags=["Goals"])

def _build_goal_response(goal: LearningGoal, db: Session) -> GoalResponse:
    # Derive live mastery from KnowledgeState (BKT source of truth)
    current_mastery = 0.10
    concept_title = "Data Structures"
    if goal.concept_id:
        ks = db.query(KnowledgeState).filter(
            KnowledgeState.learner_id == goal.learner_id,
            KnowledgeState.concept_id == goal.concept_id
        ).first()
        if ks:
            current_mastery = ks.mastery_probability
        concept = db.query(Concept).get(goal.concept_id)
        if concept:
            concept_title = concept.title
    else:
        # If no specific concept_id, calculate average mastery
        all_ks = db.query(KnowledgeState).filter(KnowledgeState.learner_id == goal.learner_id).all()
        if all_ks:
            current_mastery = sum(k.mastery_probability for k in all_ks) / len(all_ks)

    target_m = goal.target_mastery or 0.80
    progress_pct = min(100.0, round((current_mastery / target_m) * 100.0, 1))
    remaining_points = max(0.0, round((target_m - current_mastery) * 100.0, 1))

    # Auto-complete status if target reached
    if current_mastery >= target_m and goal.status == "ACTIVE":
        goal.status = "COMPLETED"
        goal.progress_percentage = 100.0
        goal.updated_at = datetime.utcnow()
        db.commit()

    return GoalResponse(
        id=goal.id,
        learner_id=goal.learner_id,
        concept_id=goal.concept_id,
        concept_title=concept_title,
        goal_name=goal.goal_name,
        target_mastery=round(target_m, 2),
        current_mastery=round(current_mastery, 3),
        progress_percentage=round(goal.progress_percentage if goal.status == "COMPLETED" else progress_pct, 1),
        remaining_percentage_points=0.0 if goal.status == "COMPLETED" else remaining_points,
        target_date=goal.target_date,
        status=goal.status,
        created_at=goal.created_at,
        updated_at=goal.updated_at
    )

@router.get("", response_model=List[GoalResponse])
def get_goals(learner_id: int = 1, status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(LearningGoal).filter(LearningGoal.learner_id == learner_id)
    if status:
        query = query.filter(LearningGoal.status == status)
    goals = query.order_by(LearningGoal.id.desc()).all()
    return [_build_goal_response(g, db) for g in goals]

@router.get("/active", response_model=Optional[GoalResponse])
def get_active_goal(learner_id: int = 1, db: Session = Depends(get_db)):
    goal = db.query(LearningGoal).filter(
        LearningGoal.learner_id == learner_id,
        LearningGoal.status == "ACTIVE"
    ).order_by(LearningGoal.id.desc()).first()
    if not goal:
        # Fall back to any goal
        goal = db.query(LearningGoal).filter(LearningGoal.learner_id == learner_id).order_by(LearningGoal.id.desc()).first()
    if not goal:
        return None
    return _build_goal_response(goal, db)

@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(LearningGoal).get(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return _build_goal_response(goal, db)

@router.post("", response_model=GoalResponse)
def create_or_update_goal(payload: GoalCreate, learner_id: int = 1, db: Session = Depends(get_db)):
    learner = db.query(LearnerProfile).get(learner_id)
    if not learner:
        raise HTTPException(status_code=404, detail="Learner profile not found")

    concept = db.query(Concept).get(payload.concept_id)
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    goal_name = payload.goal_name or f"Master {concept.title}"
    target_mastery = max(0.10, min(1.0, payload.target_mastery))

    # Enforce uniqueness rule: Only one ACTIVE goal per learner & concept
    existing_goal = db.query(LearningGoal).filter(
        LearningGoal.learner_id == learner_id,
        LearningGoal.concept_id == payload.concept_id,
        LearningGoal.status == "ACTIVE"
    ).first()

    if existing_goal:
        # Update existing goal idempotently rather than duplicating
        existing_goal.target_mastery = target_mastery
        existing_goal.goal_name = goal_name
        if payload.target_date:
            existing_goal.target_date = payload.target_date
        existing_goal.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_goal)
        return _build_goal_response(existing_goal, db)

    # Create new goal
    new_goal = LearningGoal(
        learner_id=learner_id,
        concept_id=payload.concept_id,
        goal_name=goal_name,
        target_mastery=target_mastery,
        progress_percentage=0.0,
        target_date=payload.target_date or learner.target_date,
        status="ACTIVE",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return _build_goal_response(new_goal, db)

@router.post("/{goal_id}/progress", response_model=GoalResponse)
def submit_goal_progress(goal_id: int, db: Session = Depends(get_db)):
    """
    Idempotent repeated progress submission.
    Derives progress strictly from actual BKT knowledge state.
    Does NOT duplicate records or artificially inflate progress.
    """
    goal = db.query(LearningGoal).get(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    # Live BKT mastery lookup
    current_mastery = 0.10
    if goal.concept_id:
        ks = db.query(KnowledgeState).filter(
            KnowledgeState.learner_id == goal.learner_id,
            KnowledgeState.concept_id == goal.concept_id
        ).first()
        if ks:
            current_mastery = ks.mastery_probability
    else:
        all_ks = db.query(KnowledgeState).filter(KnowledgeState.learner_id == goal.learner_id).all()
        if all_ks:
            current_mastery = sum(k.mastery_probability for k in all_ks) / len(all_ks)

    target_m = goal.target_mastery or 0.80
    progress_pct = min(100.0, round((current_mastery / target_m) * 100.0, 1))

    if current_mastery >= target_m:
        goal.status = "COMPLETED"
        goal.progress_percentage = 100.0
    else:
        goal.status = "ACTIVE"
        goal.progress_percentage = progress_pct

    goal.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(goal)

    return _build_goal_response(goal, db)
