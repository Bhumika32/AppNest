import axios from './axios';

/**
 * Notifications API Service
 * Handles all notification-related API calls
 */

const notificationsApi = {
  // Get all notifications
  getNotifications: (limit = 50, unreadOnly = false) =>
    axios.get('/notifications', {
      params: { limit, unread_only: unreadOnly },
    }),

  // Get unread count
  getUnreadCount: () =>
    axios.get('/notifications/unread'),

  // Mark single notification as read
  markAsRead: (notificationId) =>
    axios.patch(`/notifications/${notificationId}/read`),

  // Mark all notifications as read
  markAllAsRead: () =>
    axios.patch('/notifications/read-all'),

  // Delete single notification
  deleteNotification: (notificationId) =>
    axios.delete(`/notifications/${notificationId}`),

  // Clear all notifications
  clearAll: () =>
    axios.delete('/notifications/clear-all'),
};

export default notificationsApi;
