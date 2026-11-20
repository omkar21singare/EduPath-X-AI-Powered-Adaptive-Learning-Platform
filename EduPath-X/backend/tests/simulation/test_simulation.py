import pytest
import numpy as np
import os
import json
from simulation.learner import SimulatedLearner, PROFILES
from simulation.fixed_policy import FixedCurriculumPolicy
from simulation.metrics import calculate_metrics

def test_deterministic_learner():
    l1 = SimulatedLearner("Fast", seed=42)
    l2 = SimulatedLearner("Fast", seed=42)
    
    assert l1.simulate_answer("ARRAYS", "Medium") == l2.simulate_answer("ARRAYS", "Medium")
    
    l1.update_true_mastery("ARRAYS")
    l2.update_true_mastery("ARRAYS")
    assert l1.true_mastery["ARRAYS"] == l2.true_mastery["ARRAYS"]

def test_learner_profile_differences():
    fast = SimulatedLearner("Fast", seed=42)
    slow = SimulatedLearner("Struggling", seed=42)
    
    fast._init_concept("ARRAYS")
    slow._init_concept("ARRAYS")
    
    fast.update_true_mastery("ARRAYS")
    slow.update_true_mastery("ARRAYS")
    
    assert fast.true_mastery["ARRAYS"] > slow.true_mastery["ARRAYS"]

def test_difficulty_effects():
    learner = SimulatedLearner("Average", seed=42)
    
    slip_easy, guess_easy = learner.get_difficulty_modifiers("Easy")
    slip_hard, guess_hard = learner.get_difficulty_modifiers("Hard")
    
    assert slip_easy < slip_hard
    assert guess_easy > guess_hard

def test_retention_formula():
    learner = SimulatedLearner("Average", seed=42)
    learner._init_concept("ARRAYS")
    learner.true_mastery["ARRAYS"] = 0.90
    
    learner.apply_retention(10.0) # 10 days
    assert 0.10 < learner.true_mastery["ARRAYS"] < 0.90

def test_fixed_policy_independence():
    policy = FixedCurriculumPolicy(questions_per_concept=2)
    history = []
    
    # Regardless of what is in history, the 3rd question should jump to the next concept
    a1 = policy.decide(history)
    history.append({"correct": True})
    a2 = policy.decide(history)
    history.append({"correct": False})
    
    a3 = policy.decide(history)
    
    assert a1["concept_code"] == a2["concept_code"]
    assert a1["concept_code"] != a3["concept_code"]

def test_metric_calculations(tmp_path):
    mock_data = [
        {"learner_id": 1, "profile": "Fast", "arm": "Fixed", "mastery_reached": True, "mastery_reached_at": 20, "final_true_masteries": {"A": 0.95}}
    ]
    file_path = tmp_path / "mock.json"
    with open(file_path, "w") as f:
        json.dump(mock_data, f)
        
    metrics = calculate_metrics(str(file_path))
    assert metrics["Fast"]["Fixed"]["completion_event_rate"] == 1.0
    assert metrics["Fast"]["Fixed"]["mean_final_true_mastery"] == 0.95
