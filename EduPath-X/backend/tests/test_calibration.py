import pytest
import numpy as np
import pandas as pd
from calibration.generate_dataset import generate_true_parameters, generate_responses
from calibration.rasch import fit_rasch_jmle
from calibration.evaluate import align_parameters

def test_deterministic_generation():
    items1, learners1 = generate_true_parameters(n_learners=100, seed=42)
    items2, learners2 = generate_true_parameters(n_learners=100, seed=42)
    np.testing.assert_array_equal(items1['true_difficulty'].values, items2['true_difficulty'].values)
    
def test_response_matrix_dimensions():
    items, learners = generate_true_parameters(n_learners=100, seed=42)
    resp, prob = generate_responses(items, learners, seed=42)
    assert resp.shape == (100, 44)
    assert prob.shape == (100, 44)

def test_binary_responses():
    items, learners = generate_true_parameters(n_learners=50, seed=42)
    resp, _ = generate_responses(items, learners, seed=42)
    assert set(np.unique(resp)).issubset({0, 1})

def test_location_alignment():
    true_b = np.array([-1.0, 0.0, 1.0])
    est_b = np.array([-0.5, 0.5, 1.5])
    aligned_b, offset = align_parameters(true_b, est_b)
    np.testing.assert_allclose(aligned_b, true_b)
    assert offset == -0.5
