import apiClient from './apiClient';

export const userService = {
    getDashboardSummary: () => apiClient.get('/profile/me/dashboard-summary'),
    getProfile: () => apiClient.get('/profile/me'),
    updateProfile: (data) => apiClient.put('/profile/me', data),
    getStats: () => apiClient.get('/profile/me/stats'),
    getAchievements: () => apiClient.get('/profile/me/achievements'),
};
