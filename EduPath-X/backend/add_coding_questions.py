from app.database.session import SessionLocal
from app.models.models import Question, Concept

def add_coding_questions():
    db = SessionLocal()
    coding_q = db.query(Question).filter(Question.question_type == 'CODING').first()
    print('Coding questions existing:', coding_q is not None)
    if not coding_q:
        c_arr = db.query(Concept).filter(Concept.code == 'ARRAYS').first()
        if c_arr:
            q1 = Question(
                concept_id=c_arr.id,
                question_type='CODING',
                question_text='Implement a function `two_sum(nums, target)` that returns the indices of the two numbers such that they add up to target as a list [i, j]. Assume exactly one solution exists.',
                options=['def two_sum(nums, target): pass'],
                correct_answer='def two_sum(nums, target): return [0, 1]',
                explanation='Use a hash map to record seen numbers and their indices in O(N) time.',
                difficulty='Medium',
                estimated_time_seconds=120,
                verified_status='VERIFIED',
                starter_code='def two_sum(nums, target):\n    # Write your solution here\n    seen = {}\n    for i, n in enumerate(nums):\n        diff = target - n\n        if diff in seen:\n            return [seen[diff], i]\n        seen[n] = i\n    return []',
                test_cases=[
                    {'input': 'two_sum([2, 7, 11, 15], 9)', 'expected_output': '[0, 1]'},
                    {'input': 'two_sum([3, 2, 4], 6)', 'expected_output': '[1, 2]'},
                    {'input': 'two_sum([3, 3], 6)', 'expected_output': '[0, 1]'}
                ],
                calibrated_slip=0.08,
                calibrated_guess=0.10,
                calibrated_difficulty=0.25
            )
            db.add(q1)

        c_stack = db.query(Concept).filter(Concept.code == 'STACKS').first()
        if c_stack:
            q2 = Question(
                concept_id=c_stack.id,
                question_type='CODING',
                question_text='Implement a function `is_valid_parentheses(s: str) -> bool` that determines if the input string containing brackets ()[]{} is valid.',
                options=['def is_valid_parentheses(s): pass'],
                correct_answer='True',
                explanation='Use a stack to match corresponding opening and closing brackets in LIFO order.',
                difficulty='Medium',
                estimated_time_seconds=120,
                verified_status='VERIFIED',
                starter_code='def is_valid_parentheses(s):\n    stack = []\n    mapping = {")": "(", "}": "{", "]": "["}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else "#"\n            if mapping[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack',
                test_cases=[
                    {'input': 'is_valid_parentheses("()")', 'expected_output': 'True'},
                    {'input': 'is_valid_parentheses("()[]{}")', 'expected_output': 'True'},
                    {'input': 'is_valid_parentheses("(]")', 'expected_output': 'False'},
                    {'input': 'is_valid_parentheses("([)]")', 'expected_output': 'False'}
                ],
                calibrated_slip=0.06,
                calibrated_guess=0.08,
                calibrated_difficulty=0.35
            )
            db.add(q2)

        db.commit()
        print('Added coding questions with test suites successfully.')
    db.close()

if __name__ == '__main__':
    add_coding_questions()
