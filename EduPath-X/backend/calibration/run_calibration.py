import json
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from generate_dataset import generate_true_parameters, generate_responses
from rasch import fit_rasch_jmle
from evaluate import align_parameters, calculate_recovery_metrics, calculate_predictive_metrics
from plots import plot_recovery, plot_distributions, plot_calibration_curve

def main():
    SEED = 42
    N_LEARNERS = 1000
    N_ITEMS = 44
    
    print("Generating dataset...")
    items_df, learners_df = generate_true_parameters(n_learners=N_LEARNERS, seed=SEED)
    responses, true_probs = generate_responses(items_df, learners_df, seed=SEED)
    
    # Predictive validation setup: 80% train, 20% test (random mask over matrix)
    rng = np.random.default_rng(SEED + 1)
    mask = rng.random(responses.shape) < 0.8
    train_responses = np.copy(responses)
    # We could implement missing data in JMLE, but since prompt asked for complete matrix for primary:
    # "Implement the primary calibration dataset as a fully observed matrix... Do not add artificial missingness to the primary experiment."
    # Wait, for predictive validation: "Fit the model on a training subset of responses. Evaluate predictions on held-out responses."
    # Let's do a complete fit, but for predictive validation, we can just split learners (800 train, 200 test) or hold out a subset.
    # Actually, JMLE needs all items to estimate item parameters. If we split learners into train/test, we can estimate items on train, and evaluate on test? 
    # Or just use the whole matrix for parameter recovery, and report log-loss on the whole matrix?
    # "Fit the model on a training subset of responses."
    
    # Train/Test Split (800 train, 200 test)
    train_idx = range(0, 800)
    test_idx = range(800, 1000)
    
    train_resp = responses[train_idx, :]
    
    print("Fitting Rasch model on train set...")
    theta_train, b_hat = fit_rasch_jmle(train_resp, max_iter=50)
    
    # We must align b_hat to true_b (over all items)
    true_b = items_df['true_difficulty'].values
    aligned_b, b_offset = align_parameters(true_b, b_hat)
    
    print("Fitting theta for test set (fixing b_hat)...")
    # For test set, we fix b_hat and estimate theta_test
    # This avoids leaking test responses into item parameter estimation
    from scipy.optimize import minimize
    theta_test = np.zeros(len(test_idx))
    def nll_theta(t, resp_row, current_b):
        diff = t - current_b
        p = 1.0 / (1.0 + np.exp(-diff))
        return -np.sum(resp_row * np.log(p + 1e-10) + (1 - resp_row) * np.log(1 - p + 1e-10)) + 0.1 * t**2
        
    for i, j in enumerate(test_idx):
        res = minimize(nll_theta, theta_test[i], args=(responses[j, :], b_hat), method='L-BFGS-B')
        theta_test[i] = res.x[0]
        
    # Combine theta back for overall ability recovery
    theta_hat = np.concatenate([theta_train, theta_test])
    true_theta = learners_df['true_theta'].values
    # Align theta_hat
    aligned_theta, theta_offset = align_parameters(true_theta, theta_hat)
    
    # Metrics
    item_rec = calculate_recovery_metrics(true_b, aligned_b)
    abil_rec = calculate_recovery_metrics(true_theta, aligned_theta)
    
    # Predictive metrics on test set
    test_resp = responses[test_idx, :]
    diff_test = theta_test[:, None] - b_hat[None, :]
    prob_pred_test = 1.0 / (1.0 + np.exp(-diff_test))
    pred_metrics = calculate_predictive_metrics(test_resp, prob_pred_test)
    
    results = {
        "experiment": {
            "name": "Rasch_1PL_Validation",
            "seed": SEED,
            "n_learners": N_LEARNERS,
            "n_items": N_ITEMS,
            "model": "Rasch/1PL",
            "exposure": "complete"
        },
        "item_recovery": item_rec,
        "ability_recovery": abil_rec,
        "prediction": pred_metrics,
        "identification": {
            "alignment_method": "Mean shift matching true mean",
            "offset": b_offset
        }
    }
    
    with open('calibration/results/calibration_results.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    # CSVs
    items_df['estimated_difficulty'] = b_hat
    items_df['aligned_estimated_difficulty'] = aligned_b
    items_df['difficulty_error'] = aligned_b - true_b
    items_df.to_csv('calibration/results/item_parameters.csv', index=False)
    
    learners_df['estimated_theta'] = theta_hat
    learners_df['aligned_estimated_theta'] = aligned_theta
    learners_df['ability_error'] = aligned_theta - true_theta
    learners_df.to_csv('calibration/results/learner_parameters.csv', index=False)
    
    # Plots
    plot_recovery(true_b, aligned_b, "True vs Estimated Item Difficulty", "True b", "Aligned Estimated b", "calibration/results/true_vs_estimated_item_difficulty.png")
    plot_recovery(true_theta, aligned_theta, "True vs Estimated Learner Ability", "True theta", "Aligned Estimated theta", "calibration/results/true_vs_estimated_learner_ability.png")
    plot_distributions(true_b, aligned_b, "calibration/results/item_difficulty_distribution.png")
    plot_calibration_curve(test_resp.flatten(), prob_pred_test.flatten(), "calibration/results/calibration_curve.png")
    
    print("Calibration complete.")

if __name__ == '__main__':
    main()
