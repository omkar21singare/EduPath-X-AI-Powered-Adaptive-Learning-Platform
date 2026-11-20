"""
Adaptive Recommendation Engine for EduPath-X.
Generates personalized actions backed by dynamic learner data rationale.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import Concept, ConceptPrerequisite, KnowledgeState, QuestionAttempt, LearnerProfile, Question, LearningGoal

class AdaptiveRecommendationEngine:
    def generate_recommendations(self, db: Session, learner_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        # Fetch all concepts and knowledge states for learner
        concepts = db.query(Concept).order_by(Concept.display_order).all()
        k_states = {
            ks.concept_id: ks for ks in db.query(KnowledgeState).filter(KnowledgeState.learner_id == learner_id).all()
        }

        # Identify which concepts have available practice questions in the question bank
        # In a real DB session, we only recommend concepts that have >= 1 question.
        # If in a lightweight mock without Question records (e.g. simulation test mock), question_concept_ids is empty so no filtering occurs.
        question_concept_ids = set()
        try:
            all_questions = db.query(Question).all()
            question_concept_ids = {q.concept_id for q in all_questions if getattr(q, 'concept_id', None) is not None}
        except Exception:
            question_concept_ids = set()

        # Build prerequisite map
        prereqs = db.query(ConceptPrerequisite).all()
        prereq_map: Dict[int, List[ConceptPrerequisite]] = {}
        for p in prereqs:
            if p.concept_id not in prereq_map:
                prereq_map[p.concept_id] = []
            prereq_map[p.concept_id].append(p)

        # Safe lookup for active learner goal (supports both real DB and mock DB)
        active_goal = None
        try:
            all_goals = db.query(LearningGoal).all()
            for g in all_goals:
                if getattr(g, 'learner_id', None) == learner_id and getattr(g, 'status', None) == 'ACTIVE':
                    active_goal = g
                    break
        except Exception:
            active_goal = None

        recommendations = []

        for concept in concepts:
            # Skip concepts that have zero practice questions available in the question bank
            if question_concept_ids and concept.id not in question_concept_ids:
                continue

            ks = k_states.get(concept.id)
            mastery = ks.mastery_probability if ks else 0.10
            total_attempts = ks.total_attempts if ks else 0
            correct_attempts = ks.correct_attempts if ks else 0

            # Calculate recent accuracy from attempts
            recent_attempts = db.query(QuestionAttempt).join(QuestionAttempt.question).filter(
                QuestionAttempt.learner_id == learner_id,
                QuestionAttempt.question.has(concept_id=concept.id)
            ).order_by(QuestionAttempt.timestamp.desc()).limit(10).all()

            recent_accuracy = (
                sum(1 for a in recent_attempts if a.is_correct) / len(recent_attempts)
            ) if recent_attempts else (correct_attempts / total_attempts if total_attempts > 0 else 0.0)

            # Check prerequisites satisfaction
            prereq_list = prereq_map.get(concept.id, [])
            all_prereqs_met = True
            prereq_details = []

            for p in prereq_list:
                # If a prerequisite concept is not in the question bank (i.e. unpracticeable foundational topic),
                # do not block practice on downstream practiceable concepts.
                if question_concept_ids and p.prerequisite_id not in question_concept_ids:
                    continue

                parent_ks = k_states.get(p.prerequisite_id)
                parent_mastery = parent_ks.mastery_probability if parent_ks else 0.10
                parent_concept = db.query(Concept).get(p.prerequisite_id)
                parent_title = parent_concept.title if parent_concept else f"Concept #{p.prerequisite_id}"

                prereq_details.append({
                    "parent_title": parent_title,
                    "parent_mastery": round(parent_mastery * 100, 1),
                    "required_mastery": round(p.minimum_mastery * 100, 1),
                    "is_met": parent_mastery >= p.minimum_mastery
                })

                if parent_mastery < p.minimum_mastery:
                    all_prereqs_met = False

            # Recommendation decision logic
            action_type = None
            reason_text = ""
            rationale_json = {}

            if not all_prereqs_met:
                # If target is locked, check if learner is trying to advance prematurely
                continue

            if mastery < 0.50:
                if total_attempts == 0 and all_prereqs_met:
                    action_type = "LEARN"
                    reason_text = f"Start learning {concept.title} because your current estimated mastery is {round(mastery * 100)}% and you have no previous attempts."
                else:
                    action_type = "REVISE"
                    reason_text = f"Revise and do easy practice for {concept.title} because your current estimated mastery is {round(mastery * 100)}%."
                rationale_json = {
                    "mastery_level": round(mastery * 100, 1),
                    "priority": "HIGH"
                }
            elif 0.50 <= mastery < 0.80:
                action_type = "PRACTICE"
                reason_text = f"Do medium practice for {concept.title} because your current estimated mastery is {round(mastery * 100)}%."
                rationale_json = {
                    "mastery_level": round(mastery * 100, 1),
                    "priority": "MEDIUM"
                }
            elif 0.80 <= mastery <= 0.90:
                action_type = "CHALLENGE"
                reason_text = f"Do harder practice for {concept.title} because your current estimated mastery is {round(mastery * 100)}%."
                rationale_json = {
                    "mastery_level": round(mastery * 100, 1),
                    "priority": "MEDIUM"
                }
            else: # mastery > 0.90
                action_type = "ADVANCE"
                reason_text = f"Consider the next concept after {concept.title} because your current estimated mastery is {round(mastery * 100)}%."
                rationale_json = {
                    "mastery_level": round(mastery * 100, 1),
                    "priority": "LOW"
                }

            if action_type:
                target_difficulty = "Medium"
                if action_type in ["LEARN", "REVISE"]:
                    target_difficulty = "Easy"
                elif action_type == "CHALLENGE":
                    target_difficulty = "Hard"
                elif action_type == "ADVANCE":
                    target_difficulty = "Advanced"

                goal_info = None
                if active_goal:
                    is_goal_concept = (getattr(active_goal, 'concept_id', None) == concept.id) or (getattr(active_goal, 'concept_id', None) is None)
                    goal_info = {
                        "id": getattr(active_goal, 'id', None),
                        "goal_name": getattr(active_goal, 'goal_name', ''),
                        "target_mastery": round((getattr(active_goal, 'target_mastery', 0.8) or 0.8) * 100, 1),
                        "is_direct_goal_concept": is_goal_concept,
                        "status": getattr(active_goal, 'status', 'ACTIVE')
                    }

                recommendations.append({
                    "concept_id": concept.id,
                    "concept_code": concept.code,
                    "concept_title": concept.title,
                    "action_type": action_type,
                    "target_difficulty": target_difficulty,
                    "current_mastery": round(mastery * 100, 1),
                    "prerequisites_met": all_prereqs_met,
                    "prerequisite_details": prereq_details,
                    "reason_text": reason_text,
                    "rationale": rationale_json,
                    "active_goal": goal_info
                })

            if len(recommendations) >= limit:
                break

        return recommendations

recommendation_engine = AdaptiveRecommendationEngine()
