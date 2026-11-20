import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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
