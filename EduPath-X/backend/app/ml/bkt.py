"""
Bayesian Knowledge Tracing (BKT) Engine for EduPath-X.
Estimates P(K_c | learner interaction history) continuously with dynamic parameter calibration.
"""

from typing import Tuple, Optional

# Default BKT parameters
DEFAULT_P_INIT = 0.20
DEFAULT_P_TRANS = 0.15
DEFAULT_P_SLIP = 0.10
DEFAULT_P_GUESS = 0.25

class BKTEngine:
    def __init__(self, p_init=DEFAULT_P_INIT, p_trans=DEFAULT_P_TRANS, p_slip=DEFAULT_P_SLIP, p_guess=DEFAULT_P_GUESS):
        self.p_init = p_init
        self.p_trans = p_trans
        self.p_slip = p_slip
        self.p_guess = p_guess

    def update_knowledge(
        self,
        current_p_know: float,
        is_correct: bool,
        difficulty: str = "Medium",
        response_time_sec: float = 15.0,
        item_slip: Optional[float] = None,
        item_guess: Optional[float] = None,
        item_difficulty_value: Optional[float] = None
    ) -> Tuple[float, float]:
        """
        Updates P(K) given correctness, question difficulty, and response time.
        Supports dynamic item-calibrated slip, guess, and continuous Rasch difficulty.
        Returns tuple: (prior, posterior)
        """
        prior = max(0.01, min(0.99, current_p_know))
        
        # 1. Use calibrated slip/guess if provided, otherwise compute from difficulty
        if item_slip is not None:
            p_s = max(0.02, min(0.40, item_slip))
        elif difficulty == "Easy":
            p_s = 0.05
        elif difficulty == "Hard":
            p_s = 0.15
        else:
            p_s = self.p_slip

        if item_guess is not None:
            p_g = max(0.05, min(0.45, item_guess))
        elif difficulty == "Easy":
            p_g = 0.35
        elif difficulty == "Hard":
            p_g = 0.15
        else:
            p_g = self.p_guess

        # 2. Continuous difficulty calibration adjustments (if Rasch b-parameter supplied)
        if item_difficulty_value is not None:
            # item_difficulty_value typically in [-2.5, +2.5]
            # Higher difficulty raises slip slightly, lowers guess
            diff_factor = max(-2.0, min(2.0, float(item_difficulty_value)))
            p_g = max(0.05, min(0.40, p_g - 0.05 * diff_factor))
            p_s = max(0.03, min(0.35, p_s + 0.03 * diff_factor))

        # 3. Response time heuristic: very quick wrong answer implies guessing/rush
        if not is_correct and response_time_sec < 5.0:
            p_s = min(0.25, p_s * 1.5)

        # 4. Calculate P(K | Observation)
        if is_correct:
            numerator = prior * (1.0 - p_s)
            denominator = numerator + (1.0 - prior) * p_g
        else:
            numerator = prior * p_s
            denominator = numerator + (1.0 - prior) * (1.0 - p_g)

        p_obs = numerator / (denominator if denominator > 0 else 1e-6)

        # 5. Transition update: P(K_t) = P(K_t | obs) + (1 - P(K_t | obs)) * P(T)
        posterior = p_obs + (1.0 - p_obs) * self.p_trans

        # Bound to [0.01, 0.99]
        posterior = max(0.01, min(0.99, posterior))
        return prior, posterior

    @staticmethod
    def get_status_from_mastery(p_know: float, is_unlocked: bool = True) -> str:
        """
        Maps probability P(K) to UI concept status.
        """
        if not is_unlocked:
            return "LOCKED"
        if p_know >= 0.85:
            return "MASTERED"
        if p_know >= 0.50:
            return "IN_PROGRESS"
        if p_know >= 0.20:
            return "WEAK"
        return "NOT_STARTED"

bkt_engine = BKTEngine()
