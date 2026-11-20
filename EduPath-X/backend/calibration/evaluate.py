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
