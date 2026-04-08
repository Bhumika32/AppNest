import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../store/authStore.js';

const AdminRoute = () => {
    const { isAuthenticated, role, isInitializing } = useAuthStore();

    if (isInitializing) {
        return (
            <div className="flex items-center justify-center h-screen bg-dark-bg">
                <div className="w-16 h-16 border-4 border-neon-pink border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    if (!isAuthenticated) {
        console.warn('[AdminRoute] User not authenticated, redirecting to /login');
        return <Navigate to="/login" replace />;
    }

    if (role !== 'admin') {
        console.warn(`[AdminRoute] User role "${role}" is not admin, redirecting to /dashboard`);
        return <Navigate to="/dashboard" replace />;
    }

    return <Outlet />;
};

export default AdminRoute;
