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

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach Authorization Bearer token dynamically if stored
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getStoredLearnerId = (): number => {
  const storedId = localStorage.getItem('learner_id');
  if (storedId) {
    const parsed = parseInt(storedId, 10);
    if (!isNaN(parsed) && parsed > 0) return parsed;
  }
  return 1;
};

export const setAuthSession = (token: string, learnerId: number, user: any) => {
  localStorage.setItem('token', token);
  localStorage.setItem('learner_id', String(learnerId));
  localStorage.setItem('user', JSON.stringify(user));
};

export const clearAuthSession = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('learner_id');
  localStorage.removeItem('user');
};

export const loginUser = async (email: string, password: string) => {
  const res = await api.post('/auth/login', { email, password });
  if (res.data.access_token) {
    setAuthSession(res.data.access_token, res.data.user.id, res.data.user);
  }
  return res.data;
};

export const demoLoginUser = async () => {
  const res = await api.post('/auth/demo-login');
  if (res.data.access_token) {
    setAuthSession(res.data.access_token, res.data.user.id, res.data.user);
  }
  return res.data;
};

export const registerUser = async (email: string, password: string, fullName: string) => {
  const res = await api.post('/auth/register', { email, password, full_name: fullName });
  if (res.data.access_token) {
    setAuthSession(res.data.access_token, res.data.user.id, res.data.user);
  }
  return res.data;
};

export const getDashboard = async (learnerId?: number): Promise<DashboardResponse> => {
  const lid = learnerId ?? getStoredLearnerId();
  const response = await api.get(`/dashboard?learner_id=${lid}`);
  return response.data;
};

export const getConcepts = async (learnerId?: number): Promise<ConceptNode[]> => {
  const lid = learnerId ?? getStoredLearnerId();
  const response = await api.get(`/concepts?learner_id=${lid}`);
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
  learnerId?: number,
  submittedCode?: string
): Promise<QuestionAttemptResult> => {
  const lid = learnerId ?? getStoredLearnerId();
  const response = await api.post(`/questions/submit?learner_id=${lid}`, {
    question_id: questionId,
    selected_option: selectedOption,
    submitted_code: submittedCode,
    response_time_seconds: responseTimeSec,
  });
  return response.data;
};

export const startSession = async (learnerId?: number) => {
  const lid = learnerId ?? getStoredLearnerId();
  const response = await api.post(`/sessions/start?learner_id=${lid}`);
  return response.data;
};

export const getRecommendations = async (learnerId?: number): Promise<Recommendation[]> => {
  const lid = learnerId ?? getStoredLearnerId();
  const response = await api.get(`/recommendations?learner_id=${lid}`);
  return response.data;
};

export const simulateDays = async (days: number, profileName: string, learnerId?: number): Promise<SimulationResult> => {
  const lid = learnerId ?? getStoredLearnerId();
  const response = await api.post(`/simulation/simulate-days?learner_id=${lid}`, {
    days,
    profile_name: profileName,
  });
  return response.data;
};

export const resetSimulation = async (learnerId?: number) => {
  const lid = learnerId ?? getStoredLearnerId();
  const response = await api.post(`/simulation/reset?learner_id=${lid}`);
  return response.data;
};

export const runEvaluation = async (numTrials: number = 50, days: number = 30): Promise<EvaluationResult> => {
  const response = await api.post('/evaluation/run', {
    num_trials: numTrials,
    days_to_simulate: days,
  });
  return response.data;
};

export const askAssistant = async (message: string, learnerId?: number): Promise<AssistantResponse> => {
  const lid = learnerId ?? getStoredLearnerId();
  const response = await api.post(`/assistant/chat?learner_id=${lid}`, { message });
  return response.data;
};

export const getGoals = async (learnerId?: number, status?: string): Promise<GoalResponse[]> => {
  const lid = learnerId ?? getStoredLearnerId();
  const url = status ? `/goals?learner_id=${lid}&status=${status}` : `/goals?learner_id=${lid}`;
  const response = await api.get(url);
  return response.data;
};

export const getActiveGoal = async (learnerId?: number): Promise<GoalResponse | null> => {
  const lid = learnerId ?? getStoredLearnerId();
  const response = await api.get(`/goals/active?learner_id=${lid}`);
  return response.data;
};

export const createOrUpdateGoal = async (
  conceptId: number,
  targetMastery: number = 0.8,
  goalName?: string,
  targetDate?: string,
  learnerId?: number
): Promise<GoalResponse> => {
  const lid = learnerId ?? getStoredLearnerId();
  const response = await api.post(`/goals?learner_id=${lid}`, {
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
