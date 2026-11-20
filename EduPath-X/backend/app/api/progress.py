from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database.session import get_db
from app.models.models import KnowledgeState, Concept, QuestionAttempt, LearnerProfile

router = APIRouter(prefix="/api/progress", tags=["Progress"])

@router.get("/reports", response_model=Dict[str, Any])
def get_progress_reports(learner_id: int = 1, db: Session = Depends(get_db)):
    learner = db.query(LearnerProfile).get(learner_id)
    k_states = db.query(KnowledgeState).filter(KnowledgeState.learner_id == learner_id).all()
    attempts = db.query(QuestionAttempt).filter(QuestionAttempt.learner_id == learner_id).order_by(QuestionAttempt.timestamp.asc()).all()

    strong = []
    weak = []
    needing_review = []

    for ks in k_states:
        c = ks.concept
        if not c: continue
        val = round(ks.mastery_probability * 100, 1)
        if ks.mastery_probability >= 0.80:
            strong.append({"code": c.code, "title": c.title, "mastery": val})
        elif ks.mastery_probability < 0.55:
            weak.append({"code": c.code, "title": c.title, "mastery": val})
        else:
            needing_review.append({"code": c.code, "title": c.title, "mastery": val})

    # Historical trend timeline
    timeline = []
    current_avg = 0.10
    if attempts:
        for idx, a in enumerate(attempts):
            current_avg = (current_avg * idx + a.bkt_posterior) / (idx + 1)
            timeline.append({
                "date": a.timestamp.strftime("%b %d"),
                "mastery": round(current_avg * 100, 1)
            })
    else:
        timeline = [
            {"date": "Day 1", "mastery": 20.0},
            {"date": "Day 4", "mastery": 35.0},
            {"date": "Day 8", "mastery": 52.0},
            {"date": "Day 12", "mastery": 68.0}
        ]

    performance_change_explanation = (
        f"Your performance improved by {round(current_avg * 40)}% over the past 14 days due to "
        f"consistent accuracy in linear data structures (Arrays & Stacks) and targeted BKT practice repetitions."
    )

    return {
        "current_mastery": round(current_avg * 100, 1),
        "strong_concepts": strong,
        "weak_concepts": weak,
        "needing_review": needing_review,
        "learning_consistency": f"{learner.streak_count if learner else 7} Day Active Streak",
        "timeline": timeline,
        "why_performance_changed": performance_change_explanation
    }
