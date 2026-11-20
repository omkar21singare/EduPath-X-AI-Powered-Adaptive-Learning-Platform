import pytest
from app.ml.bkt import BKTEngine

def test_bkt_correct_answer_increases_mastery():
    engine = BKTEngine()
    prior = 0.30
    _, posterior = engine.update_knowledge(prior, is_correct=True, difficulty="Medium", response_time_sec=15.0)
    assert posterior > prior, "Correct answer should strictly increase knowledge probability P(K)"

def test_bkt_incorrect_answer_decreases_mastery():
    engine = BKTEngine()
    prior = 0.60
    _, posterior = engine.update_knowledge(prior, is_correct=False, difficulty="Medium", response_time_sec=15.0)
    assert posterior < prior, "Incorrect answer should strictly decrease knowledge probability P(K)"

def test_status_mapping():
    assert BKTEngine.get_status_from_mastery(0.90, True) == "MASTERED"
    assert BKTEngine.get_status_from_mastery(0.60, True) == "IN_PROGRESS"
    assert BKTEngine.get_status_from_mastery(0.30, True) == "WEAK"
    assert BKTEngine.get_status_from_mastery(0.90, False) == "LOCKED"
