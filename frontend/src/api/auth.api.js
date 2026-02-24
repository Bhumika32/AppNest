import api from './axios';

export const loginUser = (credentials) => api.post('/auth/login', credentials);
export const registerUser = (data) => api.post('/auth/register', data);
export const verifyOtp = (data) => api.post('/auth/verify-otp', data);
export const resendOtp = (email) => api.post('/auth/resend-otp', { email });
export const refreshAccessToken = () => api.post('/auth/refresh');
export const logoutUser = () => api.post('/auth/logout');
export const logoutAllDevices = () => api.post('/auth/logout-all');
export const getMe = () => api.get('/auth/me');
export const forgotPassword = (email) => api.post('/auth/forgot-password', { email });
export const resetPassword = (data) => api.post('/auth/reset-password', data);
