/**
 * FIXED apiClient (Production-safe)
 * - Uses single axios instance ONLY
 * - Correct refresh handling
 * - Cookie always sent
 */

import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const BASE_URL = import.meta.env.VITE_API_URL || '/api';

const apiClient = axios.create({
    baseURL: BASE_URL,
    withCredentials: true, // 🔥 REQUIRED
    headers: { 'Content-Type': 'application/json' },
});

// ─────────────────────────────────────────────────────────────
// BLOCKLIST
// ─────────────────────────────────────────────────────────────
const AUTH_REFRESH_BLOCKLIST = [
    '/auth/login',
    '/auth/refresh',
    '/auth/logout',
    '/auth/register',
];

// ─────────────────────────────────────────────────────────────
// REQUEST INTERCEPTOR
// ─────────────────────────────────────────────────────────────
apiClient.interceptors.request.use(
    (config) => {
        const token = useAuthStore.getState().token;

        console.log("TOKEN DEBUG:", token);

        if (token && typeof token === 'string' && token.split('.').length === 3) {
            config.headers.Authorization = `Bearer ${token}`;
        } else {
            delete config.headers.Authorization;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

// ─────────────────────────────────────────────────────────────
// REFRESH CONTROL
// ─────────────────────────────────────────────────────────────
let refreshPromise = null;

// ─────────────────────────────────────────────────────────────
// RESPONSE INTERCEPTOR
// ─────────────────────────────────────────────────────────────
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        const isBlocklisted = AUTH_REFRESH_BLOCKLIST.some(ep =>
            originalRequest.url?.includes(ep)
        );

        if (error.response?.status === 401 && !originalRequest._retry && !isBlocklisted) {
            originalRequest._retry = true;

            try {
                if (!refreshPromise) {
                    // 🔥 USE SAME INSTANCE (CRITICAL FIX)
                    refreshPromise = apiClient.post('/auth/refresh')
                        .then(res => {
                            refreshPromise = null;
                            return res.data.access_token;
                        })
                        .catch(err => {
                            refreshPromise = null;
                            throw err;
                        });
                }

                const access_token = await refreshPromise;

                // Save token
                useAuthStore.getState().setToken(access_token);

                // Retry original request
                originalRequest.headers.Authorization = `Bearer ${access_token}`;
                return apiClient(originalRequest);

            } catch (refreshError) {
                // Logout fallback
                useAuthStore.setState({
                    user: null,
                    token: null,
                    isAuthenticated: false,
                    isInitializing: false
                });

                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default apiClient;
// /**
//  * Canonical Axios client for AppNest.
//  * Single source of truth for all API calls.
//  * Handles: JWT injection, token refresh rotation, and global error logging.
//  */
// import axios from 'axios';
// import { useAuthStore } from '../store/authStore';

// const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// const apiClient = axios.create({
//     baseURL: BASE_URL,
//     withCredentials: true, // Required for HttpOnly refresh cookie
//     headers: { 'Content-Type': 'application/json' },
// });

// // Auth endpoints that must NOT trigger refresh retry (avoid infinite loops)
// const AUTH_REFRESH_BLOCKLIST = [
//     '/auth/login', '/auth/refresh', '/auth/logout',
//     '/auth/register', '/auth/verify-otp', '/auth/resend-otp',
// ];

// // ── Request Interceptor: Inject Bearer Token ──────────────────────────────────
// apiClient.interceptors.request.use(
//     (config) => {
//         const token = useAuthStore.getState().token;
//         console.log("TOKEN DEBUG:", token);
//         // 🔥 STRICT VALIDATION (this is what you're missing)
//         if (token && typeof token === 'string' && token.split('.').length === 3) {
//             config.headers.Authorization = `Bearer ${token}`;
//         } else {
//             // 🚫 DO NOT send broken token
//             delete config.headers.Authorization;
//         }
//         return config;
//     },
//     (error) => Promise.reject(error)
// );

// // ── Single-Flight Refresh Queue ───────────────────────────────────────────────
// let refreshPromise = null;

// // ── Response Interceptor: Auto-Refresh on 401 ─────────────────────────────────
// apiClient.interceptors.response.use(
//     (response) => response,
//     async (error) => {
//         const originalRequest = error.config;
//         const isBlocklisted = AUTH_REFRESH_BLOCKLIST.some(ep => originalRequest.url?.includes(ep));

//         if (error.response?.status === 401 && !originalRequest._retry && !isBlocklisted) {
//             originalRequest._retry = true;

//             // If a refresh is already in progress, wait for it
//             if (!refreshPromise) {
//                 refreshPromise = axios.post(`${BASE_URL}/auth/refresh`, {}, { withCredentials: true })
//                     .then(res => {
//                         refreshPromise = null;
//                         return res.data.access_token;
//                     })
//                     .catch(err => {
//                         refreshPromise = null;
//                         throw err;
//                     });
//             }

//             try {
//                 const access_token = await refreshPromise;

//                 // Update memory store
//                 useAuthStore.getState().setToken(access_token);

//                 // Retry request
//                 originalRequest.headers.Authorization = `Bearer ${access_token}`;
//                 return apiClient(originalRequest);
//             } catch (refreshError) {
//                 // Refresh failed — clear auth state
//                 useAuthStore.setState({ user: null, token: null, isAuthenticated: false, isInitializing: false });
//                 return Promise.reject(refreshError);
//             }
//         }

//         if (error.response?.status === 422) {
//             console.error('[AppNest API] 422 Unprocessable Entity:', error.response.data);
//         }

//         return Promise.reject(error);
//     }
// );

// export default apiClient;
