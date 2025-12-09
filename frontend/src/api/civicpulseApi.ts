import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const civicPulseApi = {
  // Health check
  health: () => api.get('/health'),

  // Reports
  submitReport: (data: { tenant_id: number; description: string; location?: string }) =>
    api.post('/reports/', data),
  
  getReport: (reportId: number) => api.get(`/reports/${reportId}`),
  
  listReports: (tenantId?: number, skip = 0, limit = 100) =>
    api.get('/reports/', { params: { tenant_id: tenantId, skip, limit } }),

  // Issues
  listIssues: (tenantId?: number, status?: string) =>
    api.get('/issues/', { params: { tenant_id: tenantId, status } }),
  
  getIssue: (issueId: number) => api.get(`/issues/${issueId}`),
  
  updateIssue: (issueId: number, data: any) => api.patch(`/issues/${issueId}`, data),

  // Scores
  getTenantScores: (tenantId: number) => api.get(`/scores/tenant/${tenantId}`),
  
  getAreaScores: (areaId: number) => api.get(`/scores/area/${areaId}`),
  
  getLeaderboard: (tenantId?: number) =>
    api.get('/scores/leaderboard', { params: { tenant_id: tenantId } }),
}

export default api
