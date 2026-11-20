import pytest
import numpy as np
from simulation.experiment import ExperimentRunner
import json
import os

def test_full_experiment_reproducibility(tmp_path):
    # Run first time
    out1 = tmp_path / "run1"
    runner1 = ExperimentRunner(output_dir=str(out1))
    runner1.run_experiment(num_learners=50)
    
    # Run second time
    out2 = tmp_path / "run2"
    runner2 = ExperimentRunner(output_dir=str(out2))
    runner2.run_experiment(num_learners=50)
    
    from simulation.metrics import calculate_metrics
    metrics1 = calculate_metrics(str(out1 / "experiment_results.json"))
    metrics2 = calculate_metrics(str(out2 / "experiment_results.json"))
    
    for p in metrics1:
        for a in metrics1[p]:
            for k in metrics1[p][a]:
                val1 = metrics1[p][a][k]
                val2 = metrics2[p][a][k]
                if val1 is not None and val2 is not None:
                    assert np.isclose(val1, val2), f"Mismatch in {p} {a} {k}: {val1} != {val2}"
                else:
                    assert val1 == val2
