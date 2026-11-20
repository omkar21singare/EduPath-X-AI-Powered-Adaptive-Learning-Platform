from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="student") # student, demo, admin
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("LearnerProfile", back_populates="user", uselist=False)

class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    class_name = Column(String, default="B.Tech CSE")
    semester = Column(String, default="Semester 4")
    avatar = Column(String, nullable=True)
    streak_count = Column(Integer, default=0)
    last_active_date = Column(String, nullable=True) # YYYY-MM-DD
    target_date = Column(String, default="30th June 2025")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="profile")
    goals = relationship("LearningGoal", back_populates="learner")
    knowledge_states = relationship("KnowledgeState", back_populates="learner")
    attempts = relationship("QuestionAttempt", back_populates="learner")
    sessions = relationship("LearningSession", back_populates="learner")

class LearningGoal(Base):
    __tablename__ = "learning_goals"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"))
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    goal_name = Column(String, nullable=False)
    target_mastery = Column(Float, default=0.85)
    progress_percentage = Column(Float, default=0.0)
    target_date = Column(String, nullable=True)
    status = Column(String, default="ACTIVE") # ACTIVE, COMPLETED, PAUSED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    learner = relationship("LearnerProfile", back_populates="goals")
    concept = relationship("Concept")

class Concept(Base):
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False) # e.g., 'DFS', 'BST'
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, default="Data Structures") # Basic, Linear, Trees, Graphs, Advanced
    difficulty_level = Column(String, default="Medium") # Easy, Medium, Hard
    display_order = Column(Integer, default=0)

    prerequisites = relationship("ConceptPrerequisite", foreign_keys="ConceptPrerequisite.concept_id", back_populates="concept")
    materials = relationship("LearningMaterial", back_populates="concept")
    questions = relationship("Question", back_populates="concept")

class ConceptPrerequisite(Base):
    __tablename__ = "concept_prerequisites"

    id = Column(Integer, primary_key=True, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    prerequisite_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    minimum_mastery = Column(Float, default=0.7)

    concept = relationship("Concept", foreign_keys=[concept_id], back_populates="prerequisites")
    prerequisite = relationship("Concept", foreign_keys=[prerequisite_id])

class ContentSource(Base):
    __tablename__ = "content_sources"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, nullable=False) # e.g. MIT OpenCourseWare 6.006
    official_url = Column(String, nullable=False)
    license = Column(String, default="CC BY-NC-SA 4.0")
    retrieved_at = Column(String, default="2025-01-15")
    description = Column(Text, nullable=True)
    status = Column(String, default="VERIFIED") # VERIFIED, UNVERIFIED

    materials = relationship("LearningMaterial", back_populates="source")
    questions = relationship("Question", back_populates="source")

class LearningMaterial(Base):
    __tablename__ = "learning_materials"

    id = Column(Integer, primary_key=True, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    title = Column(String, nullable=False)
    learning_objectives = Column(JSON, nullable=False) # List of strings
    explanation = Column(Text, nullable=False)
    code_example = Column(Text, nullable=True)
    visual_explanation = Column(Text, nullable=True)
    complexity_info = Column(JSON, nullable=True) # {"time": "O(V+E)", "space": "O(V)"}
    worked_example = Column(Text, nullable=True)
    content_version = Column(String, default="1.0.0")
    source_id = Column(Integer, ForeignKey("content_sources.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    concept = relationship("Concept", back_populates="materials")
    source = relationship("ContentSource", back_populates="materials")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    question_type = Column(String, nullable=False) # MCQ, Code tracing, Complexity analysis, Debugging, Conceptual
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False) # List of option strings
    correct_answer = Column(String, nullable=False)
    explanation = Column(Text, nullable=False)
    difficulty = Column(String, default="Medium") # Easy, Medium, Hard
    estimated_time_seconds = Column(Integer, default=60)
    verified_status = Column(String, default="VERIFIED")
    starter_code = Column(Text, nullable=True)
    test_cases = Column(JSON, nullable=True) # list of {input: str, expected_output: str}
    calibrated_slip = Column(Float, nullable=True)
    calibrated_guess = Column(Float, nullable=True)
    calibrated_difficulty = Column(Float, nullable=True) # Continuous Rasch b parameter
    source_id = Column(Integer, ForeignKey("content_sources.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    concept = relationship("Concept", back_populates="questions")
    source = relationship("ContentSource", back_populates="questions")

class QuestionAttempt(Base):
    __tablename__ = "question_attempts"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("learning_sessions.id"), nullable=True)
    selected_option = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    response_time_seconds = Column(Float, default=15.0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    bkt_prior = Column(Float, nullable=False)
    bkt_posterior = Column(Float, nullable=False)

    learner = relationship("LearnerProfile", back_populates="attempts")
    question = relationship("Question")

class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"), nullable=False)
    session_type = Column(String, default="ADAPTIVE") # ADAPTIVE, REVISION, PRACTICE, ASSESSMENT
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    items_completed = Column(Integer, default=0)
    total_time_seconds = Column(Integer, default=0)

    learner = relationship("LearnerProfile", back_populates="sessions")

class KnowledgeState(Base):
    __tablename__ = "knowledge_states"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    mastery_probability = Column(Float, default=0.1) # P(K_c)
    last_updated = Column(DateTime, default=datetime.utcnow)
    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    decay_factor = Column(Float, default=0.0)

    learner = relationship("LearnerProfile", back_populates="knowledge_states")
    concept = relationship("Concept")

class KnowledgeStateHistory(Base):
    __tablename__ = "knowledge_state_history"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    mastery_probability = Column(Float, nullable=False)
    evidence_type = Column(String, default="QUESTION_ATTEMPT") # QUESTION_ATTEMPT, RETENTION_DECAY, SIMULATION
    session_id = Column(Integer, nullable=True)
    change_delta = Column(Float, default=0.0)

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    action_type = Column(String, nullable=False) # LEARN, REVISE, PRACTICE, CHALLENGE, ADVANCE
    reason_text = Column(Text, nullable=False)
    rationale_json = Column(JSON, nullable=False) # {"recent_accuracy": 0.54, "attempts": 7, "prereq_mastery": 0.82}
    status = Column(String, default="PENDING") # PENDING, ACCEPTED, DISMISSED
    created_at = Column(DateTime, default=datetime.utcnow)

    concept = relationship("Concept")

class RecommendationEvent(Base):
    __tablename__ = "recommendation_events"

    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=False)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"), nullable=False)
    action_taken = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class LearningActivity(Base):
    __tablename__ = "learning_activities"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("learning_sessions.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    activity_type = Column(String, nullable=False) # READING, QUIZ, REVISION
    duration_seconds = Column(Integer, default=60)
    timestamp = Column(DateTime, default=datetime.utcnow)

class MistakePattern(Base):
    __tablename__ = "mistake_patterns"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    mistake_category = Column(String, nullable=False) # e.g. "Traversal order confusion", "Off-by-one index error"
    frequency = Column(Integer, default=1)
    last_occurred = Column(DateTime, default=datetime.utcnow)

class Streak(Base):
    __tablename__ = "streaks"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"), nullable=False)
    date = Column(String, nullable=False) # YYYY-MM-DD
    minimum_activity_completed = Column(Boolean, default=True)

class ProgressSnapshot(Base):
    __tablename__ = "progress_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"), nullable=False)
    date = Column(String, nullable=False) # YYYY-MM-DD
    overall_mastery = Column(Float, default=0.0)
    concepts_mastered = Column(Integer, default=0)
    total_time_spent = Column(Float, default=0.0)

class SimulationProfile(Base):
    __tablename__ = "simulation_profiles"

    id = Column(Integer, primary_key=True, index=True)
    profile_name = Column(String, unique=True, nullable=False) # Balanced, Strong, Struggling with Trees, Inconsistent
    description = Column(Text, nullable=False)
    learning_rate = Column(Float, default=0.15)
    slip_rate = Column(Float, default=0.10)
    guess_rate = Column(Float, default=0.20)
    response_time_factor = Column(Float, default=1.0)
    consistency_score = Column(Float, default=0.8)

class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"), nullable=False)
    profile_name = Column(String, nullable=False)
    current_simulated_day = Column(Integer, default=1)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

class SimulationEvent(Base):
    __tablename__ = "simulation_events"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("simulation_runs.id"), nullable=False)
    simulated_day = Column(Integer, nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    event_type = Column(String, nullable=False)
    details_json = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date_run = Column(DateTime, default=datetime.utcnow)
    policy_a_name = Column(String, default="Fixed Linear Curriculum")
    policy_b_name = Column(String, default="EduPath-X Adaptive Engine")
    num_simulations = Column(Integer, default=100)
    results_json = Column(JSON, nullable=False)
