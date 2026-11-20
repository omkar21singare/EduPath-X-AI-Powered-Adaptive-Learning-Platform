import os

os.makedirs('calibration/results', exist_ok=True)

with open('calibration/__init__.py', 'w') as f:
    pass

with open('calibration/generate_dataset.py', 'w') as f:
    f.write('''\
import numpy as np
import pandas as pd

def generate_true_parameters(n_learners=1000, seed=42):
    rng = np.random.default_rng(seed)
    
    # 44 items distribution
    concepts = (['ARRAYS'] * 8 + 
                ['LINKED_LIST'] * 8 + 
                ['STACKS'] * 12 + 
                ['TREES'] * 8 + 
                ['GRAPHS'] * 8)
                
    item_ids = list(range(1, 45))
    
    true_b = rng.normal(0, 1, size=44)
    true_theta = rng.normal(0, 1, size=n_learners)
    
    items_df = pd.DataFrame({'item_id': item_ids, 'concept': concepts, 'true_difficulty': true_b})
    learners_df = pd.DataFrame({'learner_id': range(1, n_learners + 1), 'true_theta': true_theta})
    
    return items_df, learners_df

def generate_responses(items_df, learners_df, seed=42):
    rng = np.random.default_rng(seed)
    
    b = items_df['true_difficulty'].values
    theta = learners_df['true_theta'].values
    
    # Probability matrix: P(X=1) = 1 / (1 + exp(-(theta - b)))
    # Shape: (n_learners, n_items)
    diff = theta[:, None] - b[None, :]
    prob = 1.0 / (1.0 + np.exp(-diff))
    
    responses = (rng.random(size=prob.shape) < prob).astype(int)
    return responses, prob
''')

with open('calibration/rasch.py', 'w') as f:
    f.write('''\
import numpy as np
from scipy.optimize import minimize

def fit_rasch_jmle(responses, max_iter=100, tol=1e-4):
    n_learners, n_items = responses.shape
    
    # Initialize
    theta = np.zeros(n_learners)
    b = np.zeros(n_items)
    
    # Avoid perfect scores / zero scores which cause inf estimates
    # Clip responses slightly or just add small regularization
    # JMLE often uses small l2 penalty (ridge) to prevent drift
    
    def nll_theta(t, resp_row, current_b):
        diff = t - current_b
        p = 1.0 / (1.0 + np.exp(-diff))
        # Add slight L2 regularization to keep theta bounded
        return -np.sum(resp_row * np.log(p + 1e-10) + (1 - resp_row) * np.log(1 - p + 1e-10)) + 0.1 * t**2

    def nll_b(current_b_val, resp_col, current_theta):
        diff = current_theta - current_b_val
        p = 1.0 / (1.0 + np.exp(-diff))
        return -np.sum(resp_col * np.log(p + 1e-10) + (1 - resp_col) * np.log(1 - p + 1e-10)) + 0.1 * current_b_val**2
        
    for it in range(max_iter):
        old_theta = theta.copy()
        old_b = b.copy()
        
        # Optimize theta
        for j in range(n_learners):
            res = minimize(nll_theta, theta[j], args=(responses[j, :], b), method='L-BFGS-B')
            theta[j] = res.x[0]
            
        # Center theta to fix location (mean = 0)
        theta_mean = np.mean(theta)
        theta = theta - theta_mean
        
        # Optimize b
        for i in range(n_items):
            res = minimize(nll_b, b[i], args=(responses[:, i], theta), method='L-BFGS-B')
            b[i] = res.x[0]
            
        b_mean = np.mean(b)
        b = b - b_mean
            
        delta = np.max(np.abs(theta - old_theta)) + np.max(np.abs(b - old_b))
        if delta < tol:
            break
            
    return theta, b
''')

with open('calibration/evaluate.py', 'w') as f:
    f.write('''\
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import log_loss, brier_score_loss, roc_auc_score, accuracy_score

def align_parameters(true_params, est_params):
    # Location shift alignment:
    # Since theta - b is invariant to shift, we align the mean of estimates to the mean of true values
    offset = np.mean(true_params) - np.mean(est_params)
    aligned = est_params + offset
    return aligned, offset

def calculate_recovery_metrics(true_params, aligned_est):
    rmse = np.sqrt(np.mean((true_params - aligned_est)**2))
    mae = np.mean(np.abs(true_params - aligned_est))
    pearson_r, _ = pearsonr(true_params, aligned_est)
    spearman_r, _ = spearmanr(true_params, aligned_est)
    
    return {
        "pearson_r": float(pearson_r),
        "spearman_r": float(spearman_r),
        "rmse": float(rmse),
        "mae": float(mae)
    }

def calculate_predictive_metrics(responses, prob_pred):
    y_true = responses.flatten()
    y_prob = prob_pred.flatten()
    y_pred = (y_prob >= 0.5).astype(int)
    
    ll = log_loss(y_true, y_prob)
    bs = brier_score_loss(y_true, y_prob)
    acc = accuracy_score(y_true, y_pred)
    auc = roc_auc_score(y_true, y_prob)
    
    return {
        "log_loss": float(ll),
        "brier_score": float(bs),
        "accuracy": float(acc),
        "auc": float(auc)
    }
''')

with open('calibration/plots.py', 'w') as f:
    f.write('''\
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_recovery(true_vals, est_vals, title, xlabel, ylabel, save_path):
    plt.figure(figsize=(8, 6))
    plt.scatter(true_vals, est_vals, alpha=0.5)
    
    # Identity line
    min_val = min(np.min(true_vals), np.min(est_vals))
    max_val = max(np.max(true_vals), np.max(est_vals))
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='Identity')
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(save_path)
    plt.close()

def plot_distributions(true_b, est_b, save_path):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(true_b, label='True Difficulty', fill=True)
    sns.kdeplot(est_b, label='Estimated Difficulty', fill=True)
    plt.title('Item Difficulty Distributions')
    plt.xlabel('Difficulty')
    plt.legend()
    plt.savefig(save_path)
    plt.close()

def plot_calibration_curve(y_true, y_prob, save_path):
    from sklearn.calibration import calibration_curve
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10)
    plt.figure(figsize=(8, 6))
    plt.plot(prob_pred, prob_true, marker='o', label='Rasch Model')
    plt.plot([0, 1], [0, 1], 'r--', label='Perfectly Calibrated')
    plt.title('Calibration Curve')
    plt.xlabel('Mean Predicted Probability')
    plt.ylabel('Fraction of Positives')
    plt.legend()
    plt.savefig(save_path)
    plt.close()
''')

with open('calibration/run_calibration.py', 'w') as f:
    f.write('''\
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
''')
