import apiClient from './apiClient';

export const adminService = {
    getOverview: () => apiClient.get('/admin/analytics/overview'),
    getGrowth: () => apiClient.get('/admin/analytics/users'),
    getGamePopularity: () => apiClient.get('/admin/analytics/games'),
    getToolUsage: () => apiClient.get('/admin/analytics/tools'),
};
