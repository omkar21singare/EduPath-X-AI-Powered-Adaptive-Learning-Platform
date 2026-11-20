import json
import os
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt

def holm_correction(p_values):
    # Sort p-values and keep track of original indices
    n = len(p_values)
    sorted_indices = np.argsort(p_values)
    sorted_p = np.array(p_values)[sorted_indices]
    
    adjusted_p = np.zeros(n)
    for i in range(n):
        adj = sorted_p[i] * (n - i)
        if i > 0:
            adj = max(adjusted_p[i-1], adj)
        adjusted_p[i] = min(adj, 1.0)
        
    # Reorder to original
    final_adj = np.zeros(n)
    for i in range(n):
        final_adj[sorted_indices[i]] = adjusted_p[i]
    return final_adj.tolist()

def main():
    with open('experiments/phase3b/results/experiment_results.json') as f:
        interactions = json.load(f)
        
    # Reconstruct trajectories
    trajectories = {}
    for inter in interactions:
        key = (inter['arm'], inter['profile'], inter['learner_id'])
        if key not in trajectories:
            trajectories[key] = []
        trajectories[key].append(inter)
        
    # Build dataframe of trajectories
    traj_records = []
    arm_questions = {'Fixed': [], 'Adaptive': [], 'IRT_Adaptive': []}
    
    for key, interactions in trajectories.items():
        arm, profile, learner_id = key
        last = interactions[-1]
        
        qtm_time = last.get('qtm_time', len(interactions))
        qtm_event = last.get('qtm_event', 0)
        
        if 'final_true_masteries' in last:
            fm = np.mean(list(last['final_true_masteries'].values()))
        else:
            fm = 0.0
            
        questions_seen = [i['question_id'] for i in interactions]
        unique_q = len(set(questions_seen))
        total_q = len(questions_seen)
        rep_rate = 1.0 - (unique_q / total_q) if total_q > 0 else 0
        
        from collections import Counter
        counts = Counter(questions_seen)
        max_rep = max(counts.values()) if counts else 0
        
        mean_gap = np.mean([i.get('difficulty_gap', 0) for i in interactions if 'difficulty_gap' in i]) if arm == 'IRT_Adaptive' else None
        
        traj_records.append({
            'arm': arm,
            'profile': profile,
            'learner_id': learner_id,
            'qtm_time': qtm_time,
            'qtm_event': qtm_event,
            'fm': fm,
            'unique_q': unique_q,
            'total_q': total_q,
            'rep_rate': rep_rate,
            'max_rep': max_rep,
            'mean_gap': mean_gap
        })
        
        arm_questions[arm].extend(questions_seen)
        
    df = pd.DataFrame(traj_records)
    
    # 3. Item Repetition Analysis
    rep_analysis = {}
    for arm in ['Fixed', 'Adaptive', 'IRT_Adaptive']:
        arm_df = df[df['arm'] == arm]
        rep_analysis[arm] = {
            'mean_unique_questions': float(arm_df['unique_q'].mean()),
            'mean_repetition_rate': float(arm_df['rep_rate'].mean()),
            'max_repetition_global': int(arm_df['max_rep'].max())
        }
        
    # Statistical Comparisons (IRT vs Adaptive)
    p_values_to_adjust = [] # QTM, FM
    
    results = {}
    # Overall 
    adapt_df = df[df['arm'] == 'Adaptive'].sort_values(['profile', 'learner_id'])
    irt_df = df[df['arm'] == 'IRT_Adaptive'].sort_values(['profile', 'learner_id'])
    
    # QTM Log-Rank
    lr_overall = logrank_test(adapt_df['qtm_time'], irt_df['qtm_time'], adapt_df['qtm_event'], irt_df['qtm_event'])
    p_values_to_adjust.append(lr_overall.p_value)
    
    # FM Wilcoxon
    diffs = irt_df['fm'].values - adapt_df['fm'].values
    mean_diff = np.mean(diffs)
    std_diff = np.std(diffs, ddof=1)
    se = std_diff / np.sqrt(len(diffs))
    w_stat, w_p = wilcoxon(diffs)
    p_values_to_adjust.append(w_p)
    d_z = mean_diff / std_diff if std_diff > 0 else 0
    
    adj_p = holm_correction(p_values_to_adjust)
    
    results['overall'] = {
        'QTM_logrank_p_raw': float(lr_overall.p_value),
        'QTM_logrank_p_holm': float(adj_p[0]),
        'FM_wilcoxon_p_raw': float(w_p),
        'FM_wilcoxon_p_holm': float(adj_p[1]),
        'FM_mean_diff': float(mean_diff),
        'FM_cohen_dz': float(d_z),
        'FM_ci_95': [float(mean_diff - 1.96*se), float(mean_diff + 1.96*se)]
    }
    
    # Profile Level
    results['profiles'] = {}
    for profile in df['profile'].unique():
        p_adapt = adapt_df[adapt_df['profile'] == profile]
        p_irt = irt_df[irt_df['profile'] == profile]
        p_fixed = df[(df['arm'] == 'Fixed') & (df['profile'] == profile)]
        
        p_diffs = p_irt['fm'].values - p_adapt['fm'].values
        p_mean = np.mean(p_diffs)
        p_std = np.std(p_diffs, ddof=1)
        p_wstat, p_wp = wilcoxon(p_diffs) if np.sum(np.abs(p_diffs)) > 0 else (0, 1.0)
        p_lr = logrank_test(p_adapt['qtm_time'], p_irt['qtm_time'], p_adapt['qtm_event'], p_irt['qtm_event'])
        
        kmf_adapt = KaplanMeierFitter()
        kmf_adapt.fit(p_adapt['qtm_time'], p_adapt['qtm_event'])
        kmf_irt = KaplanMeierFitter()
        kmf_irt.fit(p_irt['qtm_time'], p_irt['qtm_event'])
        
        results['profiles'][profile] = {
            'Adaptive_FM': float(p_adapt['fm'].mean()),
            'IRT_Adaptive_FM': float(p_irt['fm'].mean()),
            'Fixed_FM': float(p_fixed['fm'].mean()),
            'FM_diff': float(p_mean),
            'FM_cohen_dz': float(p_mean/p_std if p_std > 0 else 0),
            'FM_p': float(p_wp),
            'QTM_logrank_p': float(p_lr.p_value),
            'Adaptive_censoring_rate': float(1.0 - p_adapt['qtm_event'].mean()),
            'IRT_censoring_rate': float(1.0 - p_irt['qtm_event'].mean()),
            'Adaptive_median_QTM': float(kmf_adapt.median_survival_time_) if kmf_adapt.median_survival_time_ != np.inf else None,
            'IRT_median_QTM': float(kmf_irt.median_survival_time_) if kmf_irt.median_survival_time_ != np.inf else None
        }
        
    results['repetition'] = rep_analysis
    
    with open('experiments/phase3b/results/analysis.json', 'w') as f:
        json.dump(results, f, indent=4)
        
    # Generate Plots
    
    # 1. QTM Kaplan-Meier by profile
    plt.figure(figsize=(15, 5))
    for i, profile in enumerate(df['profile'].unique()):
        plt.subplot(1, 3, i+1)
        
        p_adapt = adapt_df[adapt_df['profile'] == profile]
        p_irt = irt_df[irt_df['profile'] == profile]
        p_fixed = df[(df['arm'] == 'Fixed') & (df['profile'] == profile)]
        
        kmf1 = KaplanMeierFitter()
        kmf1.fit(p_fixed['qtm_time'], p_fixed['qtm_event'], label='Fixed')
        kmf1.plot_survival_function()
        
        kmf2 = KaplanMeierFitter()
        kmf2.fit(p_adapt['qtm_time'], p_adapt['qtm_event'], label='Phase 2 Adaptive')
        kmf2.plot_survival_function()
        
        kmf3 = KaplanMeierFitter()
        kmf3.fit(p_irt['qtm_time'], p_irt['qtm_event'], label='IRT Adaptive')
        kmf3.plot_survival_function()
        
        plt.title(f"{profile}")
        plt.ylim(0, 1)
        
    plt.tight_layout()
    plt.savefig('experiments/phase3b/results/qtm_survival.png')
    
if __name__ == '__main__':
    main()
