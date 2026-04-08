/**
 * High-level service modules.
 * All requests go through the canonical api/axios.js client.
 */
import api from './apiClient';

export const AuthService = {
    login: (credentials) => api.post('/auth/login', credentials),
    register: (data) => api.post('/auth/register', data),
    verifyOtp: (data) => api.post('/auth/verify-otp', data),
    resendOtp: (email) => api.post('/auth/resend-otp', { email }),
    refresh: () => api.post('/auth/refresh'),
    logout: () => api.post('/auth/logout'),
    getMe: () => api.get('/auth/me'),
    forgotPassword: (email) => api.post('/auth/forgot-password', { email }),
    resetPassword: (data) => api.post('/auth/reset-password', data),
};

export const NotificationService = {
    getAll: (limit = 50, unreadOnly = false) =>
        api.get('/notifications', { params: { limit, unread_only: unreadOnly } }),
    getUnreadCount: () => api.get('/notifications/unread'),
    markAsRead: (id) => api.patch(`/notifications/${id}/read`),
    markAllAsRead: () => api.patch('/notifications/read-all'),
    delete: (id) => api.delete(`/notifications/${id}`),
    clearAll: () => api.delete('/notifications/clear-all'),
};

export const RoastService = {
    getNormal: () => api.get('/roast/normal'),
    getPersonal: (name) => api.post('/roast/personal', { name }),
    getUltra: () => api.get('/roast/ultra'),
    getGame: (gameName) => api.get(`/roast/game/${gameName}`),
    getTool: (toolName) => api.get(`/roast/tool/${toolName}`),
    getRandom: () => api.get('/roast/random'),
};

export const AnalyticsService = {
    getOverview: () => api.get('/admin/analytics/overview'),
    getUserStats: () => api.get('/admin/analytics/users'),
    getEngagement: () => api.get('/admin/analytics/engagement'),
};

export const UserService = {
    getProfile: () => api.get('/profile/me'),
    updateProfile: (data) => api.put('/profile/me', data),
    getStats: () => api.get('/profile/me/stats'),
    getAchievements: () => api.get('/profile/me/achievements'),
    getDashboardSummary: () => api.get('/profile/me/dashboard-summary'),
};

export const GameService = {
    getGames: () => api.get('/modules', { params: { type: 'game' } }),
    getLeaderboard: (slug) => api.get(`/modules/${slug}/leaderboard`),
};

export const ModuleService = {
    getAll: (type) => api.get('/modules', { params: { type } }),
    getBySlug: (slug) => api.get(`/modules/${slug}`),
    trackStart: (moduleId) => api.post('/modules/analytics/start', { module_id: moduleId }),
    trackEnd: (entryId, duration) => api.post('/modules/analytics/end', { entry_id: entryId, duration }),
    getGlobalLeaderboard: (limit = 10) => api.get('/modules/leaderboard', { params: { limit } }),
};

// Default export for any legacy code that does: import api from '../api/api'
export { api as default };
