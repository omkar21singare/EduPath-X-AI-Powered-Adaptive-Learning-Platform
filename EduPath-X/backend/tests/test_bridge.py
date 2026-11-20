import pytest
import numpy as np
import pandas as pd

import sys
sys.path.append('c:/Users/omkar/Documents/TY/ML LAB/CP/EduPath-X/EduPath-X/backend')
from app.ml.bkt import BKTEngine
from create_bridge import logit

def test_logit_boundary():
    assert np.isclose(logit(0.0), np.log(0.01/0.99))
    assert np.isclose(logit(1.0), np.log(0.99/0.01))
    assert np.isclose(logit(0.5), 0.0)

def test_bkt_processing():
    bkt = BKTEngine()
    prior, post = bkt.update_knowledge(0.1, True, "Medium")
    assert post > 0.1
    prior, post2 = bkt.update_knowledge(0.1, False, "Medium")
    assert post2 > 0.0 # Just assert it works

def test_deterministic_generation():
    rng1 = np.random.default_rng(42)
    rng2 = np.random.default_rng(42)
    assert rng1.random() == rng2.random()
