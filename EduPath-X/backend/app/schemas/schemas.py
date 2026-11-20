from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Auth & User
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Optional[str] = "student"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_demo: bool

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Learner Profile
class LearnerProfileResponse(BaseModel):
    id: int
    user_id: int
    class_name: str
    semester: str
    avatar: Optional[str]
    streak_count: int
    last_active_date: Optional[str]
    target_date: str

    class Config:
        from_attributes = True

# Learner Goals
class GoalCreate(BaseModel):
    concept_id: int
    target_mastery: float = 0.80
    target_date: Optional[str] = "30th June 2025"
    goal_name: Optional[str] = None

class GoalResponse(BaseModel):
    id: int
    learner_id: int
    concept_id: Optional[int] = None
    concept_title: Optional[str] = None
    goal_name: str
    target_mastery: float
    current_mastery: float
    progress_percentage: float
    remaining_percentage_points: float
    target_date: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Concept & Prerequisites
class ConceptPrerequisiteResponse(BaseModel):
    prerequisite_id: int
    minimum_mastery: float

class ConceptResponse(BaseModel):
    id: int
    code: str
    title: str
    description: str
    category: str
    difficulty_level: str
    display_order: int
    mastery_probability: Optional[float] = 0.0
    status: Optional[str] = "LOCKED" # MASTERED, IN_PROGRESS, WEAK, LOCKED, NOT_STARTED

    class Config:
        from_attributes = True

# Content Source
class ContentSourceResponse(BaseModel):
    id: int
    source_name: str
    official_url: str
    license: str
    retrieved_at: str
    description: Optional[str]
    status: str

    class Config:
        from_attributes = True

# Learning Material
class LearningMaterialResponse(BaseModel):
    id: int
    concept_id: int
    title: str
    learning_objectives: List[str]
    explanation: str
    code_example: Optional[str]
    visual_explanation: Optional[str]
    complexity_info: Optional[Dict[str, str]]
    worked_example: Optional[str]
    content_version: str
    source: Optional[ContentSourceResponse]

    class Config:
        from_attributes = True

# Question
class QuestionResponse(BaseModel):
    id: int
    concept_id: int
    question_type: str
    question_text: str
    options: List[str]
    difficulty: str
    estimated_time_seconds: int
    verified_status: str
    source: Optional[ContentSourceResponse]

    class Config:
        from_attributes = True

class QuestionSubmit(BaseModel):
    question_id: int
    selected_option: str
    response_time_seconds: float = 15.0
    session_id: Optional[int] = None

class QuestionAttemptResult(BaseModel):
    attempt_id: int
    question_id: int
    is_correct: bool
    correct_answer: str
    explanation: str
    bkt_prior: float
    bkt_posterior: float
    mastery_change: float
    concept_code: str
    next_recommendation: Optional[Dict[str, Any]] = None

# Knowledge State
class KnowledgeStateResponse(BaseModel):
    concept_id: int
    concept_code: str
    concept_title: str
    mastery_probability: float
    status: str
    total_attempts: int
    correct_attempts: int
    last_updated: datetime

    class Config:
        from_attributes = True

class KnowledgeHistoryPoint(BaseModel):
    timestamp: str
    mastery_probability: float
    concept_code: str
    change_delta: float

# Recommendation
class RecommendationResponse(BaseModel):
    id: Optional[int] = None
    concept_id: int
    concept_code: str
    concept_title: str
    action_type: str
    target_difficulty: Optional[str] = "Medium"
    current_mastery: Optional[float] = None
    prerequisites_met: Optional[bool] = True
    prerequisite_details: Optional[List[Dict[str, Any]]] = None
    reason_text: str
    rationale: Dict[str, Any]
    status: Optional[str] = None
    active_goal: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

# Dashboard
class DashboardKPIs(BaseModel):
    overall_progress: float
    concepts_mastered: int
    total_concepts: int
    current_streak: int
    learning_time_hours: float
    next_milestone: str
    next_milestone_progress: float

class DashboardResponse(BaseModel):
    user_name: str
    class_name: str
    semester: str
    kpis: DashboardKPIs
    knowledge_map: List[Dict[str, Any]]
    recommendations: List[RecommendationResponse]
    performance_overview: Dict[str, float]
    recent_activity: List[Dict[str, Any]]
    goal: Dict[str, Any]

# Simulation
class SimulationSimulateDaysRequest(BaseModel):
    days: int = 1
    profile_name: Optional[str] = "Struggling with Trees"

class SimulationRunResponse(BaseModel):
    run_id: int
    current_day: int
    events_processed: int
    logs: List[str]

# Guided Demo
class GuidedDemoStep(BaseModel):
    step: int
    title: str
    description: str
    action: str
    learner_state: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None

# Evaluation
class EvaluationRequest(BaseModel):
    num_trials: int = 50
    days_to_simulate: int = 30

class EvaluationResponse(BaseModel):
    policy_fixed: Dict[str, Any]
    policy_adaptive: Dict[str, Any]
    efficiency_gain_pct: float
    conclusion: str

# Assistant
class AssistantQuery(BaseModel):
    message: str

class AssistantResponse(BaseModel):
    reply: str
    recommended_action: Optional[Dict[str, Any]] = None
    data_sources_used: List[str]
