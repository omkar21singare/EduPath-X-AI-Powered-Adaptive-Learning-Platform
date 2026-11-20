import json
import os
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List
from lifelines import KaplanMeierFitter

def plot_learning_curves(data: List[Dict], output_dir: str):
    curves = {"Fixed": {}, "Adaptive": {}}
    for row in data:
        arm = row["arm"]
        t = row["simulated_time"]
        tm = row["true_mastery_before"]
        if t not in curves[arm]:
            curves[arm][t] = []
        curves[arm][t].append(tm)
        
    plt.figure(figsize=(10, 6))
    for arm in ["Fixed", "Adaptive"]:
        times = sorted(curves[arm].keys())
        mean_tm = [np.mean(curves[arm][t]) for t in times]
        plt.plot(times, mean_tm, label=arm)
        
    plt.title("Fixed vs Adaptive Learning Curves")
    plt.xlabel("Simulated Interactions")
    plt.ylabel("Mean True Mastery (All Learners & Concepts)")
    plt.legend()
    plt.savefig(os.path.join(output_dir, "learning_curves.png"))
    plt.close()

def plot_survival_curves(data: List[Dict], output_dir: str):
    learners = {}
    for row in data:
        key = (row["profile"], row["arm"], row["learner_id"])
        if key not in learners:
            learners[key] = []
        learners[key].append(row)
        
    stats_data = {
        "Fast": {"Fixed_QTM": [], "Adaptive_QTM": [], "Fixed_Event": [], "Adaptive_Event": []},
        "Average": {"Fixed_QTM": [], "Adaptive_QTM": [], "Fixed_Event": [], "Adaptive_Event": []},
        "Struggling": {"Fixed_QTM": [], "Adaptive_QTM": [], "Fixed_Event": [], "Adaptive_Event": []}
    }
    
    for key, interactions in learners.items():
        profile, arm, learner_id = key
        last_row = interactions[-1]
        
        qtm_val = last_row.get("mastery_reached_at", len(interactions))
        completed = last_row.get("completed", False)
        
        stats_data[profile][f"{arm}_QTM"].append(qtm_val)
        stats_data[profile][f"{arm}_Event"].append(1 if completed else 0)
        
    kmf = KaplanMeierFitter()
    
    for profile in ["Fast", "Average", "Struggling"]:
        plt.figure(figsize=(10, 6))
        
        # Fixed
        qtm_fixed = stats_data[profile]["Fixed_QTM"]
        ev_fixed = stats_data[profile]["Fixed_Event"]
        if qtm_fixed:
            kmf.fit(qtm_fixed, ev_fixed, label="Fixed")
            kmf.plot_survival_function()
            
        # Adaptive
        qtm_adaptive = stats_data[profile]["Adaptive_QTM"]
        ev_adaptive = stats_data[profile]["Adaptive_Event"]
        if qtm_adaptive:
            kmf.fit(qtm_adaptive, ev_adaptive, label="Adaptive")
            kmf.plot_survival_function()
            
        plt.axvline(x=50, color='r', linestyle='--', label='Censoring Boundary (50)')
        plt.title(f"Probability of not yet reaching mastery: {profile}")
        plt.xlabel("Interactions")
        plt.ylabel("Probability")
        plt.legend()
        plt.savefig(os.path.join(output_dir, f"qtm_survival_{profile}.png"))
        plt.close()

def plot_bar_comparisons(data: List[Dict], output_dir: str):
    learners = {}
    for row in data:
        key = (row["profile"], row["arm"], row["learner_id"])
        if key not in learners:
            learners[key] = []
        learners[key].append(row)
        
    profiles = ["Fast", "Average", "Struggling"]
    arms = ["Fixed", "Adaptive"]
    
    fm_means = {p: {a: [] for a in arms} for p in profiles}
    
    for key, interactions in learners.items():
        profile, arm, _ = key
        last_row = interactions[-1]
        
        if "final_true_masteries" in last_row:
            fm_means[profile][arm].append(np.mean(list(last_row["final_true_masteries"].values())))
            
    # Plot Final Mastery
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(profiles))
    width = 0.35
    
    fixed_fm = [np.mean(fm_means[p]["Fixed"]) if fm_means[p]["Fixed"] else 0 for p in profiles]
    adapt_fm = [np.mean(fm_means[p]["Adaptive"]) if fm_means[p]["Adaptive"] else 0 for p in profiles]
    
    ax.bar(x - width/2, fixed_fm, width, label='Fixed')
    ax.bar(x + width/2, adapt_fm, width, label='Adaptive')
    
    ax.set_ylabel('Mean Final True Mastery')
    ax.set_title('Final Mastery by Profile')
    ax.set_xticks(x)
    ax.set_xticklabels(profiles)
    ax.legend()
    plt.savefig(os.path.join(output_dir, "final_mastery_comparison.png"))
    plt.close()

def generate_report(results_path: str, output_dir: str):
    with open(results_path, "r") as f:
        data = json.load(f)
        
    os.makedirs(output_dir, exist_ok=True)
    plot_learning_curves(data, output_dir)
    plot_bar_comparisons(data, output_dir)
    plot_survival_curves(data, output_dir)
    print(f"Generated plots in {output_dir}")

if __name__ == "__main__":
    generate_report("simulation/results/experiment_results.json", "simulation/results")
