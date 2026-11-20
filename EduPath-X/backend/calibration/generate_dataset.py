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
