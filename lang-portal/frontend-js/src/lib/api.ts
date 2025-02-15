import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000/api',
});

export const getDashboardLastStudySession = () =>
  api.get('/dashboard/last_study_session');

export const getDashboardStudyProgress = () =>
  api.get('/dashboard/study_progress');

export const getDashboardQuickStats = () =>
  api.get('/dashboard/quick_stats');

export const getStudyActivities = () =>
  api.get('/study_activities');

export const getStudyActivity = (id: string) =>
  api.get(`/study_activities/${id}`);

export const getStudyActivitySessions = (id: string) =>
  api.get(`/study_activities/${id}/study_sessions`);

export const createStudyActivity = (data: any) =>
  api.post('/study_activities', data);

export const getWords = (page = 1) =>
  api.get('/words', { params: { page } });

export const getWord = (id: string) =>
  api.get(`/words/${id}`);

export const getGroups = (page = 1) =>
  api.get('/groups', { params: { page } });

export const getGroup = (id: string) =>
  api.get(`/groups/${id}`);

export const getGroupWords = (id: string, page = 1) =>
  api.get(`/groups/${id}/words`, { params: { page } });

export const getGroupStudySessions = (id: string, page = 1) =>
  api.get(`/groups/${id}/study_sessions`, { params: { page } });

export const getStudySessions = (page = 1) =>
  api.get('/study_sessions', { params: { page } });

export const getStudySession = (id: string) =>
  api.get(`/study_sessions/${id}`);

export const getStudySessionWords = (id: string, page = 1) =>
  api.get(`/study_sessions/${id}/words`, { params: { page } });

export const resetHistory = () =>
  api.post('/reset_history');

export const fullReset = () =>
  api.post('/full_reset');