import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.database.session import SessionLocal, engine
from app.models.models import User, LearnerProfile, Question, KnowledgeState, Concept
from app.ml.bkt import bkt_engine
from app.ml.recommendation import recommendation_engine
from app.database.base import Base
from app.database.seed_data import seed_database
import random

def run_demo():
    print("\n" + "="*50)
    print("EDUPATH-X: ADAPTIVE LEARNING DEMONSTRATION")
    print("="*50 + "\n")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Ensure seed data is present
    seed_database(db)

    # 1. Create a fresh demo student
    student_email = f"demo_{random.randint(1000,9999)}@example.com"
    demo_user = User(
        email=student_email,
        password_hash="fake",
        full_name="Demo Student",
        role="student",
        is_demo=True
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)

    profile = LearnerProfile(user_id=demo_user.id)
    db.add(profile)
    db.commit()
    db.refresh(profile)

    student_id = profile.id
    print(f"Created Student: {demo_user.full_name} (ID: {student_id})")
    print("Starting with neutral/low mastery for all concepts.\n")

    # Give initial mastery to ALG_THINK and COMP_ANALYSIS so we hit ARRAYS
    for code in ["ALG_THINK", "COMP_ANALYSIS"]:
        c = db.query(Concept).filter(Concept.code == code).first()
        ks = KnowledgeState(learner_id=student_id, concept_id=c.id, mastery_probability=0.95, total_attempts=5, correct_attempts=5)
        db.add(ks)
    db.commit()

    # Let student answer 10 questions adaptively
    for i in range(1, 11):
        print(f"--- ATTEMPT {i} ---")
        
        # A. Next Recommendation & Next Question
        recs = recommendation_engine.generate_recommendations(db, student_id, limit=3)
        if not recs:
            print("No recommendations available.")
            break
            
        top_rec = None
        for rec in recs:
            if rec["action_type"] != "ADVANCE":
                top_rec = rec
                break
                
        if not top_rec:
            print("All recommended concepts are Mastered (ADVANCE). No more questions.")
            break
            
        concept_id = top_rec["concept_id"]
        action = top_rec["action_type"]
        concept_title = top_rec["concept_title"]
        reason = top_rec["reason_text"]
        
        diff_target = "Medium"
        if action in ["LEARN", "REVISE"]:
            diff_target = "Easy"
        elif action == "CHALLENGE":
            diff_target = "Hard"
            
        q = db.query(Question).filter(Question.concept_id == concept_id, Question.difficulty == diff_target).first()
        if not q:
            print(f"Could not find a question for concept {top_rec.get('concept_code')} ({concept_title}). Advancing...")
            
            # Give mastery to this concept so we can move on
            c = db.query(Concept).filter(Concept.id == concept_id).first()
            ks = KnowledgeState(learner_id=student_id, concept_id=c.id, mastery_probability=0.95, total_attempts=5, correct_attempts=5)
            db.add(ks)
            db.commit()
            
            continue
            
        print(f"RECOMMENDATION: {action} on {concept_title}")
        print(f"EXPLANATION: {reason}")
        print(f"SELECTED QUESTION (ID {q.id}): {q.question_text}")
        print(f"DIFFICULTY: {q.difficulty}")

        # B. Simulate Answer (70% chance correct if they have some knowledge, let's just make it 60% chance to simulate a struggling student who learns)
        is_correct = random.random() < 0.60
        
        print(f"STUDENT ANSWER: {'CORRECT' if is_correct else 'INCORRECT'}")
        
        # C. BKT Update
        ks = db.query(KnowledgeState).filter(
            KnowledgeState.learner_id == student_id,
            KnowledgeState.concept_id == q.concept_id
        ).first()

        if not ks:
            ks = KnowledgeState(learner_id=student_id, concept_id=q.concept_id, mastery_probability=0.10)
            db.add(ks)
            db.flush()

        prior_p = ks.mastery_probability
        prior, posterior = bkt_engine.update_knowledge(
            current_p_know=prior_p,
            is_correct=is_correct,
            difficulty=q.difficulty,
            response_time_sec=15.0
        )
        
        # D. Update Mastery
        ks.mastery_probability = posterior
        ks.total_attempts += 1
        if is_correct:
            ks.correct_attempts += 1
        db.commit()
        
        print(f"BKT UPDATE: P(L) updated from {prior:.3f} to {posterior:.3f} (Delta: {posterior-prior:+.3f})\n")

    db.close()
    print("="*50)
    print("DEMONSTRATION COMPLETE")
    print("="*50)

if __name__ == "__main__":
    run_demo()
