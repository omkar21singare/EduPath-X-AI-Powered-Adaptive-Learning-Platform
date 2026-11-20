import axios from 'axios';
import type { 
  DashboardResponse, 
  ConceptNode, 
  LearningMaterial, 
  Question, 
  QuestionAttemptResult, 
  SimulationResult, 
  EvaluationResult, 
  AssistantResponse, 
  Recommendation,
  GoalResponse 
} from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getDashboard = async (learnerId: number = 1): Promise<DashboardResponse> => {
  const response = await api.get(`/dashboard?learner_id=${learnerId}`);
  return response.data;
};

export const getConcepts = async (learnerId: number = 1): Promise<ConceptNode[]> => {
  const response = await api.get(`/concepts?learner_id=${learnerId}`);
  return response.data;
};

export const getMaterial = async (conceptId: number): Promise<LearningMaterial> => {
  const response = await api.get(`/materials/${conceptId}`);
  return response.data;
};

export const getQuestions = async (conceptId?: number): Promise<Question[]> => {
  const url = conceptId ? `/questions?concept_id=${conceptId}` : '/questions';
  const response = await api.get(url);
  return response.data;
};

export const submitQuestion = async (
  questionId: number,
  selectedOption: string,
  responseTimeSec: number = 15.0,
  learnerId: number = 1
): Promise<QuestionAttemptResult> => {
  const response = await api.post(`/questions/submit?learner_id=${learnerId}`, {
    question_id: questionId,
    selected_option: selectedOption,
    response_time_seconds: responseTimeSec,
  });
  return response.data;
};

export const startSession = async (learnerId: number = 1) => {
  const response = await api.post(`/sessions/start?learner_id=${learnerId}`);
  return response.data;
};

export const getRecommendations = async (learnerId: number = 1): Promise<Recommendation[]> => {
  const response = await api.get(`/recommendations?learner_id=${learnerId}`);
  return response.data;
};

export const simulateDays = async (days: number, profileName: string, learnerId: number = 1): Promise<SimulationResult> => {
  const response = await api.post(`/simulation/simulate-days?learner_id=${learnerId}`, {
    days,
    profile_name: profileName,
  });
  return response.data;
};

export const resetSimulation = async (learnerId: number = 1) => {
  const response = await api.post(`/simulation/reset?learner_id=${learnerId}`);
  return response.data;
};

export const runEvaluation = async (numTrials: number = 50, days: number = 30): Promise<EvaluationResult> => {
  const response = await api.post('/evaluation/run', {
    num_trials: numTrials,
    days_to_simulate: days,
  });
  return response.data;
};

export const askAssistant = async (message: string, learnerId: number = 1): Promise<AssistantResponse> => {
  const response = await api.post(`/assistant/chat?learner_id=${learnerId}`, { message });
  return response.data;
};

export const getGoals = async (learnerId: number = 1, status?: string): Promise<GoalResponse[]> => {
  const url = status ? `/goals?learner_id=${learnerId}&status=${status}` : `/goals?learner_id=${learnerId}`;
  const response = await api.get(url);
  return response.data;
};

export const getActiveGoal = async (learnerId: number = 1): Promise<GoalResponse | null> => {
  const response = await api.get(`/goals/active?learner_id=${learnerId}`);
  return response.data;
};

export const createOrUpdateGoal = async (
  conceptId: number,
  targetMastery: number = 0.8,
  goalName?: string,
  targetDate?: string,
  learnerId: number = 1
): Promise<GoalResponse> => {
  const response = await api.post(`/goals?learner_id=${learnerId}`, {
    concept_id: conceptId,
    target_mastery: targetMastery,
    goal_name: goalName,
    target_date: targetDate,
  });
  return response.data;
};

export const submitGoalProgress = async (goalId: number): Promise<GoalResponse> => {
  const response = await api.post(`/goals/${goalId}/progress`);
  return response.data;
};

