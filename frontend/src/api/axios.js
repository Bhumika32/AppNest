/**
 * Canonical Axios client for AppNest.
 * Single source of truth for all API calls.
 * Handles: JWT injection, token refresh rotation, and global error logging.
 */
import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
    baseURL: BASE_URL,
    withCredentials: true, // Required for HttpOnly refresh cookie
    headers: { 'Content-Type': 'application/json' },
});

// Auth endpoints that must NOT trigger refresh retry (avoid infinite loops)
const AUTH_REFRESH_BLOCKLIST = [
    '/auth/login', '/auth/refresh', '/auth/logout',
    '/auth/register', '/auth/verify-otp', '/auth/resend-otp',
];

// ── Request Interceptor: Inject Bearer Token ──────────────────────────────────
api.interceptors.request.use(
    (config) => {
        const token = useAuthStore.getState().token;
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// ── Response Interceptor: Auto-Refresh on 401 ─────────────────────────────────
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        const isBlocklisted = AUTH_REFRESH_BLOCKLIST.some(ep => originalRequest.url?.includes(ep));

        if (error.response?.status === 401 && !originalRequest._retry && !isBlocklisted) {
            originalRequest._retry = true;
            try {
                // Use raw axios to bypass this interceptor for the refresh call itself
                const { data } = await axios.post(`${BASE_URL}/auth/refresh`, {}, { withCredentials: true });
                useAuthStore.getState().setToken(data.access_token);
                originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
                return api(originalRequest);
            } catch (refreshError) {
                // Refresh failed — clear auth state
                useAuthStore.setState({ user: null, token: null, isAuthenticated: false, isInitializing: false });
                return Promise.reject(refreshError);
            }
        }

        if (error.response?.status === 422) {
            console.error('[AppNest API] 422 Unprocessable Entity:', error.response.data);
        }

        return Promise.reject(error);
    }
);

export default api;

