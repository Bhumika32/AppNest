/**
 * notificationStore.js
 * Powers the XP toast, streak, level-up, and achievement notification system.
 * Toast types: 'xp' | 'level_up' | 'streak' | 'achievement' | 'info' | 'error'
 */
import { create } from 'zustand';
import notificationsApi from '../api/notificationsApi';

// Toast auto-dismiss durations (ms)
const DURATION = {
    xp: 3500,
    level_up: 6000,
    streak: 4500,
    achievement: 5000,
    info: 3000,
    error: 4000,
};

export const useNotificationStore = create((set, get) => ({
    toasts: [],        // Active on-screen toasts (auto-dismissed)
    notifications: [], // Persistent notification bell list

    /**
     * Primary entry point. Usage:
     *   useNotificationStore.getState().notify({ type: 'xp', message: '+50 XP!', amount: 50 })
     */
    notify: (notification) => {
        const id = Date.now() + Math.random();
        const duration = notification.duration ?? DURATION[notification.type] ?? 3500;
        const toast = { id, seen: false, timestamp: new Date(), ...notification };

        set((state) => ({
            toasts: [...state.toasts, toast],
            notifications: [toast, ...state.notifications].slice(0, 50), // keep last 50
        }));

        // Auto-dismiss toast
        setTimeout(() => {
            set((state) => ({ toasts: state.toasts.filter(t => t.id !== id) }));
        }, duration);
    },

    dismissToast: (id) => set((state) => ({ toasts: state.toasts.filter(t => t.id !== id) })),

    // Mark single notification as read (persist to backend when possible)
    markAsRead: async (id) => {
        try {
            // attempt backend update
            await notificationsApi.markAsRead(id);
        } catch (e) {
            // ignore network errors — still update UI optimistically
            console.warn('markAsRead failed:', e);
        }
        set((state) => ({
            notifications: state.notifications.map(n => n.id === id ? { ...n, seen: true } : n)
        }));
    },

    // Mark all as read (backend + local)
    markAllAsRead: async () => {
        try {
            await notificationsApi.markAllAsRead();
        } catch (e) {
            console.warn('markAllAsRead failed:', e);
        }
        set((state) => ({
            notifications: state.notifications.map(n => ({ ...n, seen: true }))
        }));
    },

    // Clear all notifications (delete on backend and locally)
    clearAll: async () => {
        try {
            await notificationsApi.clearAll();
        } catch (e) {
            console.warn('clearAll failed:', e);
        }
        set({ notifications: [] });
    },

    // Set notifications directly (used when loading from backend)
    setNotifications: (items) => set({ notifications: items.slice(0, 200) }),

    // Fetch notifications from backend and populate store
    fetchNotifications: async (limit = 50, unreadOnly = false) => {
        try {
            const resp = await notificationsApi.getNotifications(limit, unreadOnly);
            const data = resp.data || {};
            const list = (data.notifications || []).map((n) => ({
                id: n.id,
                seen: !!n.read,
                timestamp: n.created_at || n.createdAt || n.timestamp,
                title: n.title,
                message: n.message,
                type: n.type || 'info',
                data: n.data || {},
            }));
            set({ notifications: list });
        } catch (e) {
            console.warn('Failed to fetch notifications:', e);
        }
    },

    // Computed helper — use as: useNotificationStore(state => state.unreadCount())
    unreadCount: () => {
        return useNotificationStore.getState().notifications.filter(n => !n.seen).length;
    },

    // ── Legacy compat ─────────────────────────────────────
    addNotification: (notification) => get().notify(notification),
}));


