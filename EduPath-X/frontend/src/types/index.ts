export interface KPIStats {
  overall_progress: number;
  concepts_mastered: number;
  total_concepts: number;
  current_streak: number;
  learning_time_hours: number;
  next_milestone: string;
  next_milestone_progress: number;
}

export interface ConceptNode {
  id: number;
  code: string;
  title: string;
  category: string;
  mastery_percentage: number;
  status: 'MASTERED' | 'IN_PROGRESS' | 'WEAK' | 'LOCKED' | 'NOT_STARTED';
  is_unlocked: boolean;
  prerequisites: string[];
  practice_unlocked?: boolean;
  study_available?: boolean;
  practice_available?: boolean;
  question_count?: number;
  prerequisite_details?: Array<{
    parent_id?: number;
    parent_title: string;
    parent_mastery: number;
    required_mastery: number;
    is_met: boolean;
  }>;
}

export interface Recommendation {
  concept_id: number;
  concept_code: string;
  concept_title: string;
  action_type: 'LEARN' | 'REVISE' | 'PRACTICE' | 'CHALLENGE' | 'ADVANCE';
  target_difficulty?: string;
  current_mastery?: number;
  prerequisites_met?: boolean;
  prerequisite_details?: Array<{
    parent_title: string;
    parent_mastery: number;
    required_mastery: number;
    is_met: boolean;
  }>;
  reason_text: string;
  rationale: Record<string, any>;
  active_goal?: {
    id?: number;
    goal_name: string;
    target_mastery: number;
    is_direct_goal_concept: boolean;
    status: string;
  } | null;
}

export interface RecentActivity {
  id: number;
  title: string;
  type: string;
  is_correct?: boolean;
  timestamp: string;
}

export interface PerformanceOverview {
  concept_understanding: number;
  problem_solving: number;
  speed: number;
  accuracy: number;
  consistency: number;
}

export interface GoalData {
  id?: number;
  title: string;
  concept_id?: number;
  concept_title?: string;
  target_mastery?: number;
  current_mastery?: number;
  progress_percentage: number;
  remaining_percentage_points?: number;
  target_date: string;
  status?: 'ACTIVE' | 'COMPLETED' | 'PAUSED';
}

export interface GoalResponse {
  id: number;
  learner_id: number;
  concept_id?: number;
  concept_title?: string;
  goal_name: string;
  target_mastery: number;
  current_mastery: number;
  progress_percentage: number;
  remaining_percentage_points: number;
  target_date?: string;
  status: 'ACTIVE' | 'COMPLETED' | 'PAUSED';
  created_at?: string;
  updated_at?: string;
}

export interface DashboardResponse {
  user_name: string;
  class_name: string;
  semester: string;
  kpis: KPIStats;
  knowledge_map: ConceptNode[];
  recommendations: Recommendation[];
  performance_overview: PerformanceOverview;
  recent_activity: RecentActivity[];
  goal: GoalData;
}

export interface ContentSource {
  id: number;
  source_name: string;
  official_url: string;
  license: string;
  retrieved_at: string;
  description?: string;
  status: string;
}

export interface LearningMaterial {
  id: number;
  concept_id: number;
  title: string;
  learning_objectives: string[];
  explanation: string;
  code_example?: string;
  visual_explanation?: string;
  complexity_info?: Record<string, string>;
  worked_example?: string;
  content_version: string;
  source?: ContentSource;
}

export interface Question {
  id: number;
  concept_id: number;
  question_type: string;
  question_text: string;
  options: string[];
  difficulty: string;
  estimated_time_seconds: number;
  verified_status: string;
  starter_code?: string;
  test_cases?: Array<{ input: string; expected_output: string }>;
  source?: ContentSource;
}

export interface QuestionAttemptResult {
  attempt_id: number;
  question_id: number;
  is_correct: boolean;
  correct_answer: string;
  explanation: string;
  bkt_prior: number;
  bkt_posterior: number;
  mastery_change: number;
  concept_code: string;
  code_execution_result?: {
    language: string;
    passed_all: boolean;
    total_tests: number;
    passed_tests: number;
    execution_time_ms: number;
    results: Array<{
      test_idx: number;
      passed: boolean;
      input?: string;
      expected_output: string;
      actual_output: string;
      error?: string;
    }>;
    stdout?: string;
    error?: string;
  };
  next_recommendation?: Recommendation;
}

export interface SimulationProfile {
  name: string;
  description: string;
  learning_rate: number;
  slip_rate: number;
  guess_rate: number;
}

export interface SimulationResult {
  run_id: number;
  current_day: number;
  events_processed: number;
  logs: string[];
}

export interface EvaluationResult {
  policy_fixed: {
    name: string;
    avg_days_to_mastery: number;
    avg_questions_required: number;
    retention_rate_14day: number;
    completion_rate_pct: number;
  };
  policy_adaptive: {
    name: string;
    avg_days_to_mastery: number;
    avg_questions_required: number;
    retention_rate_14day: number;
    completion_rate_pct: number;
  };
  efficiency_gain_pct: number;
  conclusion: string;
}

export interface AssistantResponse {
  reply: string;
  recommended_action?: Recommendation;
  data_sources_used: string[];
}
