from typing import Dict, Any, List
import importlib
from app.ml.recommendation import recommendation_engine

# Mocking the required models and DB session to use the actual production policy
class MockConcept:
    def __init__(self, id, code, title, display_order):
        self.id = id
        self.code = code
        self.title = title
        self.display_order = display_order

class MockKnowledgeState:
    def __init__(self, concept_id, mastery, total_attempts, correct_attempts):
        self.concept_id = concept_id
        self.mastery_probability = mastery
        self.total_attempts = total_attempts
        self.correct_attempts = correct_attempts

class MockPrereq:
    def __init__(self, concept_id, prereq_id, min_mastery):
        self.concept_id = concept_id
        self.prerequisite_id = prereq_id
        self.minimum_mastery = min_mastery

class MockQuery:
    def __init__(self, results):
        self.results = results
    
    def all(self):
        return self.results
        
    def order_by(self, field):
        return self
        
    def filter(self, *args, **kwargs):
        return self
        
    def join(self, *args, **kwargs):
        return self
        
    def limit(self, limit):
        return self
        
    def get(self, id):
        for r in self.results:
            if getattr(r, 'id', None) == id:
                return r
        return None

class MockDB:
    def __init__(self, concepts, k_states, prereqs):
        self.concepts = concepts
        self.k_states = k_states
        self.prereqs = prereqs
        
    def query(self, model):
        # Extremely simplified mock tailored to recommendation.py's specific queries
        if model.__name__ == 'Concept':
            return MockQuery(self.concepts)
        elif model.__name__ == 'KnowledgeState':
            return MockQuery(self.k_states)
        elif model.__name__ == 'ConceptPrerequisite':
            return MockQuery(self.prereqs)
        elif model.__name__ == 'QuestionAttempt':
            return MockQuery([])
        return MockQuery([])

class BKTAdaptivePolicy:
    def __init__(self, concept_order: List[str]):
        self.concept_order = ["ARRAYS", "LINKED_LIST", "STACKS", "TREES", "GRAPHS"]
        # Build mock concepts
        self.mock_concepts = [
            MockConcept(i+1, code, code, i+1) for i, code in enumerate(self.concept_order)
        ]
        
    def decide(self, estimated_masteries: Dict[str, float], total_attempts: Dict[str, int]) -> Dict[str, Any]:
        """
        Uses the actual production policy by mocking its DB dependencies.
        """
        # Build mock knowledge states
        k_states = []
        for i, code in enumerate(self.concept_order):
            mastery = estimated_masteries.get(code, 0.10)
            attempts = total_attempts.get(code, 0)
            k_states.append(MockKnowledgeState(i+1, mastery, attempts, attempts))
            
        mock_db = MockDB(self.mock_concepts, k_states, [])
        
        # Use actual production policy
        recs = recommendation_engine.generate_recommendations(mock_db, learner_id=1, limit=1)
        
        if not recs:
            return {"action_type": "COMPLETE", "concept_code": None, "difficulty": None}
            
        top_rec = recs[0]
        action = top_rec["action_type"]
        
        if action == "ADVANCE":
            # Policy says to advance, we should simulate finding the next unmastered concept
            # recommendation_engine returns ADVANCE when > 0.90
            # So if it's ADVANCE, it means all remaining might be ADVANCE, or we need to skip it.
            # Wait, in the production app, ADVANCE just tells the user to move on.
            # For the simulation, we'll try to find the first recommendation that is NOT ADVANCE.
            recs = recommendation_engine.generate_recommendations(mock_db, learner_id=1, limit=5)
            top_rec = None
            for rec in recs:
                if rec["action_type"] != "ADVANCE":
                    top_rec = rec
                    break
            if not top_rec:
                return {"action_type": "COMPLETE", "concept_code": None, "difficulty": None}
            action = top_rec["action_type"]
            
        difficulty = "Easy"
        if action == "PRACTICE":
            difficulty = "Medium"
        elif action == "CHALLENGE":
            difficulty = "Hard"
            
        return {
            "action_type": action,
            "concept_code": top_rec["concept_code"],
            "difficulty": difficulty
        }
