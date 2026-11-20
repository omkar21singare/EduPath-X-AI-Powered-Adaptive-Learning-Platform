import json
import os
from typing import List, Dict, Any
from simulation.learner import SimulatedLearner, PROFILES
from simulation.question_bank import question_bank
from simulation.fixed_policy import FixedCurriculumPolicy, CONCEPT_ORDER
from simulation.adaptive_policy import BKTAdaptivePolicy
from app.ml.bkt import bkt_engine

class ExperimentRunner:
    def __init__(self, output_dir: str = "simulation/results/"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.fixed_policy = FixedCurriculumPolicy()
        self.adaptive_policy = BKTAdaptivePolicy(CONCEPT_ORDER)
        self.max_interactions = 50
        
    def run_experiment(self, num_learners: int = 50):
        all_results = []
        
        for profile_name in PROFILES.keys():
            print(f"Running experiments for profile: {profile_name}")
            for learner_idx in range(num_learners):
                seed = hash(f"{profile_name}_{learner_idx}") % (2**32)
                
                # Create base learner
                base_learner = SimulatedLearner(profile_name, seed)
                
                # Clone for both arms
                fixed_learner = base_learner.clone_state(seed)
                adaptive_learner = base_learner.clone_state(seed)
                
                # Run arms
                fixed_results = self.run_arm(fixed_learner, "Fixed", learner_idx)
                adaptive_results = self.run_arm(adaptive_learner, "Adaptive", learner_idx)
                
                all_results.extend(fixed_results)
                all_results.extend(adaptive_results)
                
        # Save results
        out_path = os.path.join(self.output_dir, "experiment_results.json")
        with open(out_path, "w") as f:
            json.dump(all_results, f, indent=2)
        print(f"Saved results to {out_path}")
            
    def run_arm(self, learner: SimulatedLearner, arm_type: str, learner_id: int) -> List[Dict[str, Any]]:
        interactions = []
        
        estimated_masteries = {c: 0.10 for c in CONCEPT_ORDER}
        total_attempts = {c: 0 for c in CONCEPT_ORDER}
        
        completed = False
        
        mastery_reached_at = None
        
        for step in range(self.max_interactions):
            # Check stopping condition: all concepts >= 0.90
            mastery_achieved = all(m >= 0.90 for m in estimated_masteries.values())
            
            if mastery_achieved and mastery_reached_at is None:
                mastery_reached_at = step
                
            if arm_type == "Adaptive" and mastery_achieved:
                completed = True
                break
            if arm_type == "Fixed":
                action = self.fixed_policy.decide(interactions)
            else:
                action = self.adaptive_policy.decide(estimated_masteries, total_attempts)
                
            if action["action_type"] == "COMPLETE":
                completed = True
                break
                
            concept = action["concept_code"]
            difficulty = action["difficulty"]
            
            # Select question
            questions = question_bank.get_questions(concept, difficulty)
            if not questions:
                # Fallback to any difficulty
                questions = question_bank.get_questions(concept)
            
            # If still no questions, skip (should not happen with our seed data)
            if not questions:
                # print(f"Warning: No questions for {concept}")
                # Force mastery to advance
                estimated_masteries[concept] = 0.99
                continue
                
            # Pick a question pseudo-randomly based on step
            q = questions[step % len(questions)]
            
            # Simulate answer
            is_correct = learner.simulate_answer(concept, difficulty)
            
            # BKT Update
            prior = estimated_masteries[concept]
            # using the live app's bkt engine
            _, posterior = bkt_engine.update_knowledge(
                current_p_know=prior,
                is_correct=is_correct,
                difficulty=difficulty,
                response_time_sec=15.0
            )
            
            # Record
            interactions.append({
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
            })
            
            # Update state
            estimated_masteries[concept] = posterior
            total_attempts[concept] += 1
            learner.update_true_mastery(concept)
            
        # Mark completion status on the last interaction
        if interactions:
            # For Adaptive, completed means it reached mastery before cap.
            # For Fixed, completed means it reached mastery at any point before cap/sequence end.
            interactions[-1]["mastery_reached"] = (mastery_reached_at is not None)
            interactions[-1]["mastery_reached_at"] = mastery_reached_at if mastery_reached_at is not None else len(interactions)
            interactions[-1]["completed"] = interactions[-1]["mastery_reached"]
            interactions[-1]["final_masteries"] = estimated_masteries
            interactions[-1]["final_true_masteries"] = learner.true_mastery
            
            # Retention Simulation
            pre_retention_avg = sum(learner.true_mastery.values()) / len(learner.true_mastery)
            learner.apply_retention(7.0)
            post_retention_avg = sum(learner.true_mastery.values()) / len(learner.true_mastery)
            
            interactions[-1]["retention"] = {
                "gap_days": 7.0,
                "pre_retention_mastery": pre_retention_avg,
                "post_retention_mastery": post_retention_avg,
                "mastery_drop": pre_retention_avg - post_retention_avg
            }
            
        return interactions

if __name__ == "__main__":
    runner = ExperimentRunner()
    runner.run_experiment(50)
