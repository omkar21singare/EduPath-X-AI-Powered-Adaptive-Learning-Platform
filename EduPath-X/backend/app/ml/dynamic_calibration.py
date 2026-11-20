"""
Dynamic EM (Expectation-Maximization) calibration engine for item slip and guess parameters.
Updates calibrated parameters based on empirical response history.
"""

from typing import List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from app.database.base import Base
from app.models.models import QuestionAttempt, Question

class BKTParameters(Base):
    __tablename__ = "bkt_parameters"

    id = Column(Integer, primary_key=True, index=True)
    concept_id = Column(Integer, unique=True, index=True, nullable=False)
    p_init = Column(Float, default=0.20)
    p_trans = Column(Float, default=0.15)
    p_slip = Column(Float, default=0.10)
    p_guess = Column(Float, default=0.25)
    sample_size = Column(Integer, default=0)
    last_calibrated = Column(DateTime, default=datetime.utcnow)

def calibrate_concept_parameters(db: Session, concept_id: int) -> Tuple[float, float]:
    """
    Calibrate slip and guess using EM / Bayesian posterior estimation from empirical attempts.
    Triggered when a concept accumulates >= 5 attempts.
    """
    # Fetch all attempts for questions belonging to this concept
    attempts = db.query(QuestionAttempt).join(Question).filter(Question.concept_id == concept_id).all()
    n = len(attempts)
    if n < 5:
        return 0.10, 0.25

    # Prior expectations
    sum_know = 0.0
    sum_slip_num = 0.0
    sum_slip_den = 0.0
    sum_guess_num = 0.0
    sum_guess_den = 0.0

    for a in attempts:
        # P(Know) from BKT posterior
        p_k = max(0.01, min(0.99, a.bkt_posterior))
        p_not_k = 1.0 - p_k
        sum_know += p_k

        if not a.is_correct:
            # Slipped while knowing
            sum_slip_num += p_k
        else:
            # Guessed without knowing
            sum_guess_num += p_not_k

        sum_slip_den += p_k
        sum_guess_den += p_not_k

    # M-step estimation with Laplace smoothing
    est_slip = (sum_slip_num + 1.0) / (sum_slip_den + 10.0)
    est_guess = (sum_guess_num + 2.5) / (sum_guess_den + 10.0)

    # Constrain to realistic boundaries [0.03, 0.35]
    est_slip = max(0.03, min(0.35, round(est_slip, 3)))
    est_guess = max(0.05, min(0.40, round(est_guess, 3)))

    # Persist in BKTParameters table
    param_record = db.query(BKTParameters).filter(BKTParameters.concept_id == concept_id).first()
    if not param_record:
        param_record = BKTParameters(
            concept_id=concept_id,
            p_slip=est_slip,
            p_guess=est_guess,
            sample_size=n,
            last_calibrated=datetime.utcnow()
        )
        db.add(param_record)
    else:
        param_record.p_slip = est_slip
        param_record.p_guess = est_guess
        param_record.sample_size = n
        param_record.last_calibrated = datetime.utcnow()

    # Also update questions belonging to concept
    for q in db.query(Question).filter(Question.concept_id == concept_id).all():
        q.calibrated_slip = est_slip
        q.calibrated_guess = est_guess

    db.commit()
    return est_slip, est_guess
