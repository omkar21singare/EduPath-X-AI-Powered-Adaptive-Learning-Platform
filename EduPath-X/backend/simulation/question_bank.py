import os
import re
from typing import List, Dict

# We need to extract the question tuples from seed_data.py without modifying it,
# as it's defined inside the seed_database function.
import app.database.seed_data as seed_data_module

class QuestionBank:
    def __init__(self):
        self.questions = []
        self._load_questions()
        
    def _load_questions(self):
        file_path = seed_data_module.__file__
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Extract the questions_data list using a targeted regex or just executing the string
        match = re.search(r'questions_data = \[(.*?)\]\n', content, re.DOTALL)
        if match:
            list_str = "[" + match.group(1) + "]"
            # Safe eval because we control the source
            raw_questions = eval(list_str)
            
            # Map them into a generic structure (id, concept, difficulty)
            for idx, q_tuple in enumerate(raw_questions):
                self.questions.append({
                    "id": idx + 1,
                    "concept": q_tuple[0],
                    "type": q_tuple[1],
                    "text": q_tuple[2],
                    "options": q_tuple[3],
                    "answer": q_tuple[4],
                    "explanation": q_tuple[5],
                    "difficulty": q_tuple[6],
                    "time": q_tuple[7]
                })

    def get_questions(self, concept: str = None, difficulty: str = None) -> List[Dict]:
        filtered = self.questions
        if concept:
            filtered = [q for q in filtered if q["concept"] == concept]
        if difficulty:
            filtered = [q for q in filtered if q["difficulty"] == difficulty]
        return filtered
        
question_bank = QuestionBank()
