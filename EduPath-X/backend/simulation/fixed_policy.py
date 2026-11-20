from typing import Dict, Any

# Since app.config.CONCEPT_ORDER might not exist or be accessible, we'll derive it from the ones we have questions for
CONCEPT_ORDER = ["ARRAYS", "LINKED_LIST", "STACKS", "TREES", "GRAPHS"]

class FixedCurriculumPolicy:
    def __init__(self, questions_per_concept: int = 10):
        self.questions_per_concept = questions_per_concept
        # A simple difficulty progression: Easy -> Medium -> Hard
        self.difficulty_pattern = ["Easy", "Easy", "Medium", "Medium", "Medium", "Hard", "Hard", "Hard", "Hard", "Hard"]

    def decide(self, interaction_history: list) -> Dict[str, Any]:
        """
        Determines the next action purely based on the number of interactions so far.
        NEVER changes based on correctness or mastery.
        """
        total_answered = len(interaction_history)
        
        concept_idx = total_answered // self.questions_per_concept
        if concept_idx >= len(CONCEPT_ORDER):
            return {"action_type": "COMPLETE", "concept_code": None, "difficulty": None}
            
        concept_code = CONCEPT_ORDER[concept_idx]
        
        q_idx_in_concept = total_answered % self.questions_per_concept
        difficulty = self.difficulty_pattern[min(q_idx_in_concept, len(self.difficulty_pattern) - 1)]
        
        return {
            "action_type": "PRACTICE",
            "concept_code": concept_code,
            "difficulty": difficulty
        }
