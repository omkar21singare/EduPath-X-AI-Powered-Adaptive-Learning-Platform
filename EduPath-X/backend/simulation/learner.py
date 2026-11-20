import numpy as np

class LearnerProfile:
    def __init__(self, name, learning_rate, base_slip, base_guess, decay_rate):
        self.name = name
        self.learning_rate = learning_rate
        self.base_slip = base_slip
        self.base_guess = base_guess
        self.decay_rate = decay_rate

PROFILES = {
    "Fast": LearnerProfile("Fast", 0.25, 0.05, 0.25, 0.005),
    "Average": LearnerProfile("Average", 0.15, 0.10, 0.20, 0.010),
    "Struggling": LearnerProfile("Struggling", 0.08, 0.15, 0.15, 0.020)
}

class SimulatedLearner:
    def __init__(self, profile_name: str, seed: int):
        self.profile = PROFILES[profile_name]
        self.rng = np.random.default_rng(seed)
        
        # true_mastery represents the simulated student's actual underlying ability
        # P(L) in the student's head.
        self.true_mastery = {}
        
    def _init_concept(self, concept_id: int):
        if concept_id not in self.true_mastery:
            self.true_mastery[concept_id] = 0.10  # Base starting knowledge
            
    def get_difficulty_modifiers(self, difficulty: str):
        """
        Adjusts slip and guess based on difficulty.
        Easy: Less likely to slip, more likely to guess correctly.
        Medium: Baseline.
        Hard: More likely to slip, less likely to guess correctly.
        """
        slip = self.profile.base_slip
        guess = self.profile.base_guess
        
        if difficulty == "Easy":
            slip = max(0.01, slip - 0.05)
            guess = min(0.40, guess + 0.10)
        elif difficulty == "Hard":
            slip = min(0.30, slip + 0.10)
            guess = max(0.05, guess - 0.10)
            
        return slip, guess

    def simulate_answer(self, concept_id: int, difficulty: str) -> bool:
        """
        Models the probability of answering correctly:
        P(Correct) = P(Knows) * (1 - P(Slip)) + (1 - P(Knows)) * P(Guess)
        """
        self._init_concept(concept_id)
        p_knows = self.true_mastery[concept_id]
        
        slip, guess = self.get_difficulty_modifiers(difficulty)
        
        p_correct = p_knows * (1 - slip) + (1 - p_knows) * guess
        return self.rng.random() < p_correct
        
    def update_true_mastery(self, concept_id: int):
        """
        Updates true mastery using the learner's own learning rate.
        P(L_next) = P(L) + (1 - P(L)) * learning_rate
        """
        self._init_concept(concept_id)
        current = self.true_mastery[concept_id]
        
        # Simulated actual learning taking place in their head
        next_mastery = current + (1 - current) * self.profile.learning_rate
        self.true_mastery[concept_id] = min(0.99, next_mastery)
        
    def apply_retention(self, elapsed_days: float):
        """
        Explicit exponential forgetting function.
        M(t) = M_min + (M(0) - M_min) * e^(-decay * t)
        where M_min is the baseline knowledge (0.10).
        """
        M_min = 0.10
        for concept_id, current_mastery in self.true_mastery.items():
            if current_mastery > M_min:
                retained = M_min + (current_mastery - M_min) * np.exp(-self.profile.decay_rate * elapsed_days)
                self.true_mastery[concept_id] = max(M_min, retained)

    def clone_state(self, new_seed: int):
        """
        Clones the learner to ensure paired experiments start with identical conditions.
        """
        new_learner = SimulatedLearner(self.profile.name, new_seed)
        new_learner.true_mastery = dict(self.true_mastery)
        return new_learner
