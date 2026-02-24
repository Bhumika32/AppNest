/**
 * High-level service modules.
 * All requests go through the canonical api/axios.js client.
 */
import api from '../api/axios';

export const AnalyticsService = {
    getOverview: () => api.get('/admin/analytics/overview'),
    getUserStats: () => api.get('/admin/analytics/users'),
    getEngagement: () => api.get('/admin/analytics/engagement'),
};

export const UserService = {
    getProfile: () => api.get('/profile'),
    updateProfile: (data) => api.put('/profile', data),
    uploadAvatar: (data) => api.post('/profile/avatar', data),
};

export const GameService = {
    getGames: () => api.get('/games'),
    getLeaderboard: (id) => api.get(`/games/${id}/leaderboard`),
};

export const ModuleService = {
    getAll: (type) => api.get('/modules', { params: { type } }),
    getBySlug: (slug) => api.get(`/modules/${slug}`),
    trackStart: (moduleId) => api.post('/modules/analytics/start', { module_id: moduleId }),
    trackEnd: (entryId, duration) => api.post('/modules/analytics/end', { entry_id: entryId, duration }),
};

// Default export for any legacy code that does: import api from '../services/api'
export { api as default };
