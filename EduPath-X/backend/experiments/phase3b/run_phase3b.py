import os
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from scipy.stats import wilcoxon
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

import sys
sys.path.append('c:/Users/omkar/Documents/TY/ML LAB/CP/EduPath-X/EduPath-X/backend')

from simulation.learner import SimulatedLearner, PROFILES
from simulation.question_bank import question_bank
from simulation.fixed_policy import FixedCurriculumPolicy, CONCEPT_ORDER
from simulation.adaptive_policy import BKTAdaptivePolicy
from app.ml.bkt import bkt_engine
from app.ml.recommendation import recommendation_engine
from simulation.adaptive_policy import MockKnowledgeState, MockDB, MockConcept

def logit(p):
    p = np.clip(p, 0.01, 0.99)
    return np.log(p / (1 - p))

class Phase3BIRTAdaptivePolicy:
    def __init__(self, concept_order: List[str]):
        self.concept_order = concept_order
        self.mock_concepts = [
            MockConcept(i+1, code, code, i+1) for i, code in enumerate(self.concept_order)
        ]
        
        # Load item difficulties
        self.item_difficulties = {}
        try:
            df = pd.read_csv('calibration/results/item_parameters.csv')
            for _, row in df.iterrows():
                self.item_difficulties[row['item_id']] = row['aligned_estimated_difficulty']
        except FileNotFoundError:
            rng = np.random.default_rng(42)
            for q_id in range(1, 45):
                self.item_difficulties[q_id] = rng.normal(0, 1)

    def decide(self, estimated_masteries: Dict[str, float], total_attempts: Dict[str, int]) -> Dict[str, Any]:
        k_states = []
        for i, code in enumerate(self.concept_order):
            mastery = estimated_masteries.get(code, 0.10)
            attempts = total_attempts.get(code, 0)
            k_states.append(MockKnowledgeState(i+1, mastery, attempts, attempts))
            
        mock_db = MockDB(self.mock_concepts, k_states, [])
        recs = recommendation_engine.generate_recommendations(mock_db, learner_id=1, limit=5)
        
        top_rec = None
        for rec in recs:
            if rec["action_type"] != "ADVANCE":
                top_rec = rec
                break
                
        if not top_rec:
            return {"action_type": "COMPLETE"}
            
        concept_code = top_rec["concept_code"]
        mean_concept_mastery = np.mean(list(estimated_masteries.values()))
        theta_estimated = 0.610 * logit(mean_concept_mastery) - 0.431
        
        questions = question_bank.get_questions(concept_code)
        best_question = None
        min_gap = float('inf')
        
        for q in questions:
            b_i = self.item_difficulties.get(q['id'], 0.0)
            gap = abs(theta_estimated - b_i)
            if gap < min_gap:
                min_gap = gap
                best_question = q
                
        return {
            "action_type": top_rec["action_type"],
            "concept_code": concept_code,
            "selected_question": best_question,
            "theta_estimated": theta_estimated,
            "b_i": self.item_difficulties.get(best_question['id'], 0.0),
            "difficulty_gap": min_gap,
            "mean_concept_mastery": mean_concept_mastery
        }

class ExperimentRunner3B:
    def __init__(self, output_dir: str = "experiments/phase3b/results/"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.fixed_policy = FixedCurriculumPolicy()
        self.adaptive_policy = BKTAdaptivePolicy(CONCEPT_ORDER)
        self.irt_policy = Phase3BIRTAdaptivePolicy(CONCEPT_ORDER)
        self.max_interactions = 50
        
    def run_experiment(self, num_learners: int = 50):
        all_results = []
        
        for profile_name in PROFILES.keys():
            for learner_idx in range(num_learners):
                seed = hash(f"{profile_name}_{learner_idx}") % (2**32)
                
                base_learner = SimulatedLearner(profile_name, seed)
                fixed_learner = base_learner.clone_state(seed)
                adaptive_learner = base_learner.clone_state(seed)
                irt_learner = base_learner.clone_state(seed)
                
                fixed_results = self.run_arm(fixed_learner, "Fixed", learner_idx)
                adaptive_results = self.run_arm(adaptive_learner, "Adaptive", learner_idx)
                irt_results = self.run_arm(irt_learner, "IRT_Adaptive", learner_idx)
                
                all_results.extend(fixed_results)
                all_results.extend(adaptive_results)
                all_results.extend(irt_results)
                
        out_path = os.path.join(self.output_dir, "experiment_results.json")
        with open(out_path, "w") as f:
            json.dump(all_results, f, indent=2)
            
        self.run_statistics(all_results)
            
    def run_arm(self, learner: SimulatedLearner, arm_type: str, learner_id: int) -> List[Dict[str, Any]]:
        interactions = []
        estimated_masteries = {c: 0.10 for c in CONCEPT_ORDER}
        total_attempts = {c: 0 for c in CONCEPT_ORDER}
        mastery_reached_at = None
        
        for step in range(self.max_interactions):
            mastery_achieved = all(m >= 0.90 for m in estimated_masteries.values())
            
            if mastery_achieved and mastery_reached_at is None:
                mastery_reached_at = step
                
            if arm_type in ["Adaptive", "IRT_Adaptive"] and mastery_achieved:
                break
                
            if arm_type == "Fixed":
                action = self.fixed_policy.decide(interactions)
            elif arm_type == "Adaptive":
                action = self.adaptive_policy.decide(estimated_masteries, total_attempts)
            else:
                action = self.irt_policy.decide(estimated_masteries, total_attempts)
                
            if action.get("action_type") == "COMPLETE":
                break
                
            concept = action.get("concept_code")
            
            if arm_type == "IRT_Adaptive":
                q = action["selected_question"]
                difficulty = q["difficulty"]
            else:
                difficulty = action.get("difficulty", "Medium")
                questions = question_bank.get_questions(concept, difficulty)
                if not questions:
                    questions = question_bank.get_questions(concept)
                if not questions:
                    estimated_masteries[concept] = 0.99
                    continue
                q = questions[step % len(questions)]
                
            is_correct = learner.simulate_answer(concept, difficulty)
            prior = estimated_masteries[concept]
            
            _, posterior = bkt_engine.update_knowledge(
                current_p_know=prior,
                is_correct=is_correct,
                difficulty=difficulty,
                response_time_sec=15.0
            )
            
            record = {
                "learner_id": learner_id,
                "profile": learner.profile.name,
                "arm": arm_type,
                "concept": concept,
                "question_id": q["id"],
                "difficulty": difficulty,
                "correctness": is_correct,
                "bkt_mastery_before": prior,
                "bkt_mastery_after": posterior,
                "simulated_time": step,
                "true_mastery_before": learner.true_mastery[concept]
            }
            
            if arm_type == "IRT_Adaptive":
                record["theta_estimated"] = action["theta_estimated"]
                record["b_i"] = action["b_i"]
                record["difficulty_gap"] = action["difficulty_gap"]
                record["mean_concept_mastery"] = action["mean_concept_mastery"]
                
            interactions.append(record)
            estimated_masteries[concept] = posterior
            total_attempts[concept] += 1
            learner.update_true_mastery(concept)
            
        if interactions:
            interactions[-1]["qtm_event"] = 1 if (mastery_reached_at is not None) else 0
            interactions[-1]["qtm_time"] = mastery_reached_at if (mastery_reached_at is not None) else len(interactions)
            interactions[-1]["final_true_masteries"] = learner.true_mastery
            
        return interactions

    def run_statistics(self, results):
        df = pd.DataFrame([r for r in results if 'qtm_time' in r])
        
        df['fm'] = df['final_true_masteries'].apply(lambda x: np.mean(list(x.values())))
        
        adapt_df = df[df['arm'] == 'Adaptive'].sort_values(['profile', 'learner_id'])
        irt_df = df[df['arm'] == 'IRT_Adaptive'].sort_values(['profile', 'learner_id'])
        
        diffs = irt_df['fm'].values - adapt_df['fm'].values
        mean_diff = np.mean(diffs)
        std_diff = np.std(diffs, ddof=1)
        n = len(diffs)
        d_z = mean_diff / std_diff if std_diff > 0 else 0
        se = std_diff / np.sqrt(n)
        ci_lower = mean_diff - 1.96 * se
        ci_upper = mean_diff + 1.96 * se
        
        w_stat, w_p = wilcoxon(diffs)
        
        kmf_adapt = KaplanMeierFitter()
        kmf_irt = KaplanMeierFitter()
        
        kmf_adapt.fit(adapt_df['qtm_time'], event_observed=adapt_df['qtm_event'], label='Adaptive')
        kmf_irt.fit(irt_df['qtm_time'], event_observed=irt_df['qtm_event'], label='IRT Adaptive')
        
        lr_result = logrank_test(adapt_df['qtm_time'], irt_df['qtm_time'], 
                                 adapt_df['qtm_event'], irt_df['qtm_event'])
        
        stats = {
            "hypothesis_family": ["FM_IRT_vs_Adaptive", "QTM_IRT_vs_Adaptive"],
            "final_true_mastery": {
                "mean_diff": float(mean_diff),
                "ci_95": [float(ci_lower), float(ci_upper)],
                "cohen_dz": float(d_z),
                "wilcoxon_stat": float(w_stat),
                "wilcoxon_p": float(w_p)
            },
            "qtm_survival": {
                "logrank_stat": float(lr_result.test_statistic),
                "logrank_p": float(lr_result.p_value)
            }
        }
        
        with open(os.path.join(self.output_dir, "stats.json"), "w") as f:
            json.dump(stats, f, indent=2)

if __name__ == "__main__":
    runner = ExperimentRunner3B()
    runner.run_experiment(50)
