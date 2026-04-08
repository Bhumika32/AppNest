import { create } from 'zustand';
import { io } from 'socket.io-client';
import { NotificationService } from '../api/api';
import { useAuthStore } from './authStore';
import { useUserStore } from './userStore';
import { useOverlayStore } from './overlayStore';

let socket = null;

export const useNotificationStore = create((set, get) => ({
    notifications: [],
    unreadCount: 0,
    connectionStatus: 'disconnected',
    toasts: [],

    // Toast Management
    notify: (toast) => {
        const id = Math.random().toString(36).substring(2, 9);
        const newToast = { ...toast, id };

        set((state) => ({
            toasts: [...state.toasts, newToast].slice(-5) // Keep last 5 toasts
        }));

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            get().dismissToast(id);
        }, 5000);
    },

    dismissToast: (id) => {
        set((state) => ({
            toasts: state.toasts.filter(t => t.id !== id)
        }));
    },

    // Initialize WebSocket connection
    initSocket: () => {
        if (socket) return;

        const token = useAuthStore.getState().token;
        // Use environment variable or default to localhost:5000
        const socketUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';

        socket = io(socketUrl, {
            query: { token },
            transports: ['websocket'],
            reconnectionAttempts: 5
        });

        socket.on('connect', () => {
            set({ connectionStatus: 'connected' });
            console.log('Connected to Neural Link (WebSocket)');
        });

        socket.on('disconnect', () => {
            set({ connectionStatus: 'disconnected' });
        });

        socket.on('notification', (notification) => {
            // Add to local list
            set((state) => ({
                notifications: [notification, ...state.notifications].slice(0, 100),
                unreadCount: state.unreadCount + 1
            }));

            // Handle special internal events via notifications
            if (notification.type === 'credit' && notification.data?.xp) {
                useUserStore.getState().addXp(notification.data.xp);
            }
        });

        socket.on('ux_event', (event) => {
            const { type, delivery, message, title, data } = event;

            if (delivery === 'toast') {
                get().notify({
                    type: type === 'xp_awarded' ? 'xp' : (type === 'level_up' ? 'level_up' : 'info'),
                    title: title || 'Neural Update',
                    message: message || (type === 'xp_awarded' ? `+${data?.xp_awarded} XP` : ''),
                    amount: data?.xp_awarded,
                    ...data
                });

                // Keep store XP in sync
                if (type === 'xp_awarded' && data?.xp_awarded) {
                    useUserStore.getState().addXp(data.xp_awarded);
                }
            } else if (delivery === 'overlay') {
                useOverlayStore.getState().showOverlay(event);
            } else if (delivery === 'notification') {
                // Persistent notifications are already created in DB and fetched
                // But we can add it to the local list for zero-latency feel
                set((state) => ({
                    notifications: [event, ...state.notifications].slice(0, 100),
                    unreadCount: state.unreadCount + 1
                }));
            }
        });

        socket.on('connection_success', (data) => {
            console.log('Server Ack:', data.message);
        });
    },

    disconnectSocket: () => {
        if (socket) {
            socket.disconnect();
            socket = null;
            set({ connectionStatus: 'disconnected' });
        }
    },

    fetchNotifications: async () => {
        try {
            const { data } = await NotificationService.getAll();
            const notifications = data.notifications || [];
            const unreadCount = notifications.filter(n => !n.read).length;
            set({ notifications, unreadCount });
        } catch (error) {
            console.error('Failed to fetch notifications:', error);
        }
    },

    markAsRead: async (id) => {
        try {
            await NotificationService.markAsRead(id);
            set((state) => ({
                notifications: state.notifications.map(n => n.id === id ? { ...n, read: true } : n),
                unreadCount: Math.max(0, state.unreadCount - 1)
            }));
        } catch (error) {
            console.error('Failed to mark notification as read:', error);
        }
    },

    markAllAsRead: async () => {
        try {
            await NotificationService.markAllAsRead();
            set((state) => ({
                notifications: state.notifications.map(n => ({ ...n, read: true })),
                unreadCount: 0
            }));
        } catch (error) {
            console.error('Failed to mark all as read:', error);
        }
    },

    clearAll: async () => {
        try {
            await NotificationService.clearAll();
            set({ notifications: [], unreadCount: 0 });
        } catch (error) {
            console.error('Failed to clear notifications:', error);
        }
    }
}));

export default useNotificationStore;
