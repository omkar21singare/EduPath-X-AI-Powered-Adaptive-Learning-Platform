import json
import numpy as np
from scipy import stats
from lifelines.statistics import logrank_test
from lifelines import KaplanMeierFitter
from typing import Dict, Any

def cohens_d(x: np.ndarray, y: np.ndarray) -> float:
    diff = x - y
    std_diff = np.std(diff, ddof=1)
    if std_diff == 0:
        return 0.0
    return np.mean(diff) / std_diff

def run_statistics(results_path: str) -> Dict[str, Any]:
    with open(results_path, "r") as f:
        data = json.load(f)
        
    learners = {}
    for row in data:
        key = (row["profile"], row["arm"], row["learner_id"])
        if key not in learners:
            learners[key] = []
        learners[key].append(row)
        
    stats_data = {
        "Fast": {"Fixed_QTM": {}, "Adaptive_QTM": {}, "Fixed_FM": {}, "Adaptive_FM": {}, "Fixed_Event": {}, "Adaptive_Event": {}},
        "Average": {"Fixed_QTM": {}, "Adaptive_QTM": {}, "Fixed_FM": {}, "Adaptive_FM": {}, "Fixed_Event": {}, "Adaptive_Event": {}},
        "Struggling": {"Fixed_QTM": {}, "Adaptive_QTM": {}, "Fixed_FM": {}, "Adaptive_FM": {}, "Fixed_Event": {}, "Adaptive_Event": {}}
    }
    
    for key, interactions in learners.items():
        profile, arm, learner_id = key
        last_row = interactions[-1]
        
        # QTM time and event
        qtm_val = last_row.get("mastery_reached_at", len(interactions))
        completed = last_row.get("completed", False)
        stats_data[profile][f"{arm}_QTM"][learner_id] = qtm_val
        stats_data[profile][f"{arm}_Event"][learner_id] = 1 if completed else 0
            
        # Final Mastery
        if "final_true_masteries" in last_row:
            avg_fm = np.mean(list(last_row["final_true_masteries"].values()))
            stats_data[profile][f"{arm}_FM"][learner_id] = avg_fm

    report = {}
    kmf = KaplanMeierFitter()
    
    for profile in stats_data:
        report[profile] = {}
        
        # Paired test for Final Mastery
        fm_fixed = []
        fm_adaptive = []
        for lid in sorted(stats_data[profile]["Fixed_FM"]):
            if lid in stats_data[profile]["Adaptive_FM"]:
                fm_fixed.append(stats_data[profile]["Fixed_FM"][lid])
                fm_adaptive.append(stats_data[profile]["Adaptive_FM"][lid])
                
        if fm_fixed and fm_adaptive:
            stat, pval = stats.wilcoxon(fm_fixed, fm_adaptive)
            diffs = np.array(fm_adaptive) - np.array(fm_fixed)
            mean_diff = np.mean(diffs)
            d = cohens_d(np.array(fm_adaptive), np.array(fm_fixed))
            
            ci = (
                stats.t.interval(
                    0.95,
                    len(diffs) - 1,
                    loc=mean_diff,
                    scale=stats.sem(diffs)
                )
                if len(diffs) > 1
                else (0, 0)
            )
            
            report[profile]["Final_Mastery"] = {
                "test": "Wilcoxon Signed-Rank Test",
                "n_pairs": len(fm_fixed),
                "statistic": float(stat),
                "p_value": float(pval),
                "mean_diff_adaptive_minus_fixed": float(mean_diff),
                "cohens_d": float(d),
                "95_CI": [float(ci[0]), float(ci[1])]
            }
            
        # Survival test for QTM
        qtm_fixed = []
        ev_fixed = []
        qtm_adaptive = []
        ev_adaptive = []
        
        for lid in sorted(stats_data[profile]["Fixed_QTM"]):
            if lid in stats_data[profile]["Adaptive_QTM"]:
                qtm_fixed.append(stats_data[profile]["Fixed_QTM"][lid])
                ev_fixed.append(stats_data[profile]["Fixed_Event"][lid])
                
                qtm_adaptive.append(stats_data[profile]["Adaptive_QTM"][lid])
                ev_adaptive.append(stats_data[profile]["Adaptive_Event"][lid])
                
        if len(qtm_fixed) > 0:
            results = logrank_test(qtm_adaptive, qtm_fixed, event_observed_A=ev_adaptive, event_observed_B=ev_fixed)
            pval = results.p_value
            stat = results.test_statistic
            
            # calculate KM median
            kmf.fit(qtm_fixed, ev_fixed)
            fixed_median = kmf.median_survival_time_
            
            kmf.fit(qtm_adaptive, ev_adaptive)
            adapt_median = kmf.median_survival_time_
            
            report[profile]["Questions_To_Mastery_Survival"] = {
                "test": "Log-Rank Test",
                "reason": "Survival analysis for right-censored time-to-event data.",
                "n_pairs": len(qtm_fixed),
                "statistic": float(stat),
                "p_value": float(pval),
                "fixed_km_median": float(fixed_median) if fixed_median != np.inf else "Median QTM not reached within 50 interactions.",
                "adaptive_km_median": float(adapt_median) if adapt_median != np.inf else "Median QTM not reached within 50 interactions."
            }
            
    # Apply Holm-Bonferroni correction (6 tests)
    p_values = []
    tests_ref = []
    for profile in report:
        for metric in report[profile]:
            p = report[profile][metric]["p_value"]
            p_values.append(p)
            tests_ref.append((profile, metric))
            
    sorted_indices = np.argsort(p_values)
    m = len(p_values)
    
    alpha = 0.05
    for i, idx in enumerate(sorted_indices):
        prof, met = tests_ref[idx]
        p = p_values[idx]
        
        corrected_p = p * (m - i)
        if i > 0:
            prev_idx = sorted_indices[i-1]
            prev_prof, prev_met = tests_ref[prev_idx]
            prev_corrected = report[prev_prof][prev_met]["corrected_p_value"]
            corrected_p = max(corrected_p, prev_corrected)
            
        corrected_p = min(1.0, corrected_p)
        
        report[prof][met]["corrected_p_value"] = float(corrected_p)
        report[prof][met]["alpha"] = alpha
        report[prof][met]["is_significant_after_correction"] = bool(corrected_p < alpha)
        
    return report

if __name__ == "__main__":
    report = run_statistics("simulation/results/experiment_results.json")
    print(json.dumps(report, indent=2))
