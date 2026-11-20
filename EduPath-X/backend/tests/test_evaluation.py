from app.evaluation.evaluator import evaluator

def test_evaluator_runs_without_errors():
    res = evaluator.run_evaluation(num_trials=10, days_to_simulate=15)
    assert "policy_fixed" in res
    assert "policy_adaptive" in res
    assert "efficiency_gain_pct" in res
    assert res["policy_adaptive"]["avg_questions_required"] > 0
