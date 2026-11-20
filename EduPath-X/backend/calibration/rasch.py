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
