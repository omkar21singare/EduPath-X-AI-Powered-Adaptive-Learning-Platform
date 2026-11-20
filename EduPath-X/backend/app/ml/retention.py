"""
Retention Decay Engine for EduPath-X.
Models memory decay over time: P(K_t) = P(K_0) * exp(-lambda * delta_days)
"""

import math
from datetime import datetime

LAMBDA_DECAY = 0.025 # Memory decay rate per day

class RetentionEngine:
    @staticmethod
    def calculate_decayed_mastery(initial_mastery: float, last_interaction_date: datetime, current_date: datetime = None) -> float:
        if current_date is None:
            current_date = datetime.utcnow()
        
        days_elapsed = (current_date - last_interaction_date).total_seconds() / 86400.0
        if days_elapsed <= 1.0:
            return initial_mastery

        # Exponential decay towards baseline
        decay_factor = math.exp(-LAMBDA_DECAY * (days_elapsed - 1.0))
        decayed = initial_mastery * decay_factor
        return max(0.10, decayed)

retention_engine = RetentionEngine()
