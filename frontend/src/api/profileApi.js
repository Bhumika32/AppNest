import axios from './axios';

/**
 * Profile API Service
 * Handles all user profile-related API calls
 */

const profileApi = {
  // Profile
  getMyProfile: () =>
    axios.get('/profile/me'),

  updateMyProfile: (firstName, lastName, bio, avatarUrl) =>
    axios.put('/profile/me', {
      first_name: firstName,
      last_name: lastName,
      bio,
      avatar_url: avatarUrl,
    }),

  // Alias for consistency
  updateProfile: (data) =>
    axios.put('/profile/me', {
      first_name: data.first_name,
      last_name: data.last_name,
      bio: data.bio,
      avatar_url: data.avatar_url,
    }),

  // Statistics
  getUserStatistics: () =>
    axios.get('/profile/me/stats'),

  // Achievements
  getUserAchievements: () =>
    axios.get('/profile/me/achievements'),

  // Dashboard Summary
  getDashboardSummary: () =>
    axios.get('/profile/me/dashboard-summary'),
};

export default profileApi;
