/**
 * ProtectedRoute.jsx
 * 
 * Wraps routes that require authentication.
 * Redirects unauthenticated users to login.
 */

import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../store/authStore.js';

const ProtectedRoute = ({ requiredRole = 'user' }) => {
    const { isAuthenticated, role, isInitializing } = useAuthStore();

    // Show loading while checking auth
    if (isInitializing) {
        return (
            <div className="flex items-center justify-center h-screen bg-deep-space">
                <div className="w-16 h-16 border-4 border-neon-blue border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    if (!isAuthenticated) {
        console.warn('[ProtectedRoute] User not authenticated, redirecting to /login');
        return <Navigate to="/login" replace />;
    }

    if (requiredRole === 'admin' && role !== 'admin') {
        console.warn(`[ProtectedRoute] User role "${role}" does not have admin access`);
        return <Navigate to="/dashboard" replace />;
    }

    return <Outlet />;
};

export default ProtectedRoute;
