import json
import numpy as np
from typing import List, Dict, Any

def calculate_metrics(results_path: str) -> Dict[str, Any]:
    with open(results_path, "r") as f:
        data = json.load(f)
        
    learners = {}
    for row in data:
        key = (row["profile"], row["arm"], row["learner_id"])
        if key not in learners:
            learners[key] = []
        learners[key].append(row)
        
    metrics = {
        "Fast": {"Fixed": {}, "Adaptive": {}},
        "Average": {"Fixed": {}, "Adaptive": {}},
        "Struggling": {"Fixed": {}, "Adaptive": {}}
    }
    
    for p in metrics:
        for a in metrics[p]:
            metrics[p][a] = {
                "final_true_mastery": [],
                "conditional_qtm": [],
                "censored_qtm": [],
                "completed": 0,
                "censored": 0,
                "total": 0,
                "retention_drop": []
            }
            
    for key, interactions in learners.items():
        profile, arm, _ = key
        
        metrics[profile][arm]["total"] += 1
        
        last_row = interactions[-1]
        mastery_reached = last_row.get("mastery_reached", False)
        
        qtm_val = last_row.get("mastery_reached_at", len(interactions))
        metrics[profile][arm]["censored_qtm"].append(qtm_val)
        
        if mastery_reached:
            metrics[profile][arm]["completed"] += 1
            metrics[profile][arm]["conditional_qtm"].append(qtm_val)
        else:
            metrics[profile][arm]["censored"] += 1
            
        if "retention" in last_row:
            metrics[profile][arm]["retention_drop"].append(last_row["retention"]["mastery_drop"])
            
        if "final_true_masteries" in last_row:
            avg_true_mastery = np.mean(list(last_row["final_true_masteries"].values()))
            metrics[profile][arm]["final_true_mastery"].append(avg_true_mastery)
            
    report = {}
    for p in metrics:
        report[p] = {}
        for a in metrics[p]:
            arm_data = metrics[p][a]
            total = arm_data["total"]
            cond_qtm = arm_data["conditional_qtm"]
            cens_qtm = arm_data["censored_qtm"]
            ftm = arm_data["final_true_mastery"]
            
            report[p][a] = {
                "num_learners": total,
                "num_completed_events": arm_data["completed"],
                "num_censored": arm_data["censored"],
                "completion_event_rate": arm_data["completed"] / total if total > 0 else 0,
                "censoring_rate": arm_data["censored"] / total if total > 0 else 0,
                
                "conditional_qtm_mean": float(np.mean(cond_qtm)) if cond_qtm else None,
                "mean_observed_censored_time_at_50": float(np.mean(cens_qtm)) if cens_qtm else None,
                
                "mean_final_true_mastery": float(np.mean(ftm)) if ftm else None,
                "std_final_true_mastery": float(np.std(ftm)) if ftm else None,
                "mean_retention_drop": float(np.mean(arm_data["retention_drop"])) if arm_data["retention_drop"] else None
            }
            
    return report

if __name__ == "__main__":
    report = calculate_metrics("simulation/results/experiment_results.json")
    print(json.dumps(report, indent=2))
