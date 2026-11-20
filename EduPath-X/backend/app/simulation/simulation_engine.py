"""
Learner Simulation Engine for EduPath-X.
Simulates day-by-day learning activity using probabilistic learner profiles.
Generates ACTUAL database events, triggering real BKT updates and state progression.
"""

import random
from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import (
    LearnerProfile, Concept, Question, QuestionAttempt, KnowledgeState,
    KnowledgeStateHistory, SimulationRun, SimulationEvent, Streak, LearningSession
)
from app.ml.bkt import bkt_engine

PROFILES = {
    "Balanced learner": {
        "description": "Consistent steady learner with average learning pace.",
        "p_learn": 0.15,
        "p_slip": 0.10,
        "p_guess": 0.20,
        "speed_factor": 1.0,
        "tree_struggle": False
    },
    "Strong learner": {
        "description": "Fast learner with high retention and quick problem solving.",
        "p_learn": 0.30,
        "p_slip": 0.05,
        "p_guess": 0.15,
        "speed_factor": 0.7,
        "tree_struggle": False
    },
    "Struggling with Trees": {
        "description": "Struggles specifically with hierarchical concepts like Trees, DFS, and BFS.",
        "p_learn": 0.12,
        "p_slip": 0.12,
        "p_guess": 0.20,
        "speed_factor": 1.3,
        "tree_struggle": True
    },
    "Inconsistent learner": {
        "description": "Variable focus, occasional lapses in study consistency.",
        "p_learn": 0.10,
        "p_slip": 0.20,
        "p_guess": 0.25,
        "speed_factor": 1.2,
        "tree_struggle": False
    }
}

class SimulationEngine:
    def simulate_days(self, db: Session, learner_id: int, profile_name: str, days: int) -> Dict[str, Any]:
        profile = PROFILES.get(profile_name, PROFILES["Balanced learner"])
        learner = db.query(LearnerProfile).get(learner_id)
        if not learner:
            raise ValueError(f"Learner ID {learner_id} not found")

        # Find or create simulation run
        sim_run = db.query(SimulationRun).filter(SimulationRun.learner_id == learner_id).first()
        if not sim_run:
            sim_run = SimulationRun(
                learner_id=learner_id,
                profile_name=profile_name,
                current_simulated_day=1
            )
            db.add(sim_run)
            db.flush()

        start_day = sim_run.current_simulated_day
        end_day = start_day + days - 1
        events_processed = 0
        log_messages = []

        concepts = db.query(Concept).order_by(Concept.display_order).all()

        for day in range(start_day, end_day + 1):
            log_messages.append(f"--- Simulating Day {day} ({profile_name}) ---")
            
            # Decide session activities for the day (e.g. 3-5 questions)
            session = LearningSession(
                learner_id=learner_id,
                session_type="SIMULATION_SESSION",
                started_at=datetime.utcnow() - timedelta(days=(30 - day)),
                ended_at=datetime.utcnow() - timedelta(days=(30 - day)) + timedelta(minutes=15)
            )
            db.add(session)
            db.flush()

            # Choose active concepts based on prerequisite availability & learner state
            k_states = {
                ks.concept_id: ks for ks in db.query(KnowledgeState).filter(KnowledgeState.learner_id == learner_id).all()
            }

            # Select target concept for day
            candidate_concepts = []
            for c in concepts:
                ks = k_states.get(c.id)
                mastery = ks.mastery_probability if ks else 0.10
                if mastery < 0.85: # Concept not yet fully mastered
                    candidate_concepts.append((c, mastery))

            if not candidate_concepts:
                # All mastered! Pick random concept for review
                candidate_concepts = [(c, 0.9) for c in concepts]

            # Pick top candidate concept
            target_concept, current_mastery = candidate_concepts[0]
            questions = db.query(Question).filter(Question.concept_id == target_concept.id).all()

            if not questions:
                continue

            # Attempt 3-4 questions in target concept
            num_attempts = random.randint(3, 4)
            for _ in range(num_attempts):
                q = random.choice(questions)
                
                # Probabilistic correctness determination based on profile & current mastery
                is_tree_concept = target_concept.code in ["BST", "TREES", "DFS", "BFS", "AVL"]
                effective_mastery = current_mastery

                if profile["tree_struggle"] and is_tree_concept:
                    effective_mastery = max(0.1, effective_mastery * 0.5)

                p_correct = effective_mastery * (1.0 - profile["p_slip"]) + (1.0 - effective_mastery) * profile["p_guess"]
                is_correct = random.random() < p_correct
                
                selected_option = q.correct_answer if is_correct else q.options[0]
                resp_time = random.uniform(10.0, 45.0) * profile["speed_factor"]

                # Update BKT
                prior, posterior = bkt_engine.update_knowledge(
                    current_p_know=current_mastery,
                    is_correct=is_correct,
                    difficulty=q.difficulty,
                    response_time_sec=resp_time
                )

                # Persist Attempt
                attempt = QuestionAttempt(
                    learner_id=learner_id,
                    question_id=q.id,
                    session_id=session.id,
                    selected_option=selected_option,
                    is_correct=is_correct,
                    response_time_seconds=resp_time,
                    bkt_prior=prior,
                    bkt_posterior=posterior,
                    timestamp=datetime.utcnow() - timedelta(days=(30 - day))
                )
                db.add(attempt)

                # Update KnowledgeState
                ks = k_states.get(target_concept.id)
                if not ks:
                    ks = KnowledgeState(learner_id=learner_id, concept_id=target_concept.id)
                    db.add(ks)
                    k_states[target_concept.id] = ks

                ks.mastery_probability = posterior
                ks.total_attempts += 1
                if is_correct:
                    ks.correct_attempts += 1
                ks.last_updated = datetime.utcnow() - timedelta(days=(30 - day))

                # Update history log
                history = KnowledgeStateHistory(
                    learner_id=learner_id,
                    concept_id=target_concept.id,
                    timestamp=datetime.utcnow() - timedelta(days=(30 - day)),
                    mastery_probability=posterior,
                    evidence_type="SIMULATION_ATTEMPT",
                    session_id=session.id,
                    change_delta=posterior - prior
                )
                db.add(history)

                current_mastery = posterior
                events_processed += 1

            # Log streak for day
            streak_date = (datetime.utcnow() - timedelta(days=(30 - day))).strftime("%Y-%m-%d")
            existing_streak = db.query(Streak).filter(Streak.learner_id == learner_id, Streak.date == streak_date).first()
            if not existing_streak:
                db.add(Streak(learner_id=learner_id, date=streak_date, minimum_activity_completed=True))

            log_messages.append(
                f"Day {day}: Completed {num_attempts} questions on {target_concept.title}. Mastery updated: {round(prior*100)}% -> {round(current_mastery*100)}%."
            )

        sim_run.current_simulated_day = end_day + 1
        db.commit()

        # Recalculate streak count for profile
        streaks = db.query(Streak).filter(Streak.learner_id == learner_id).all()
        learner.streak_count = len(streaks)
        db.commit()

        return {
            "run_id": sim_run.id,
            "current_day": sim_run.current_simulated_day - 1,
            "events_processed": events_processed,
            "logs": log_messages
        }

    def reset_simulation(self, db: Session, learner_id: int):
        """Resets all simulation runs & knowledge states for learner."""
        db.query(QuestionAttempt).filter(QuestionAttempt.learner_id == learner_id).delete()
        db.query(KnowledgeStateHistory).filter(KnowledgeStateHistory.learner_id == learner_id).delete()
        db.query(Streak).filter(Streak.learner_id == learner_id).delete()
        db.query(SimulationRun).filter(SimulationRun.learner_id == learner_id).delete()
        
        # Reset knowledge states to initial baseline
        k_states = db.query(KnowledgeState).filter(KnowledgeState.learner_id == learner_id).all()
        for ks in k_states:
            ks.mastery_probability = 0.10
            ks.total_attempts = 0
            ks.correct_attempts = 0

        learner = db.query(LearnerProfile).get(learner_id)
        if learner:
            learner.streak_count = 0

        db.commit()
        return {"status": "SUCCESS", "message": "Simulation environment reset to Day 1 baseline."}

simulation_engine = SimulationEngine()
