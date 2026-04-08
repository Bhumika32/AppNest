import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import AppShell from './AppShell.jsx';

// Route Guards
import ProtectedRoute from '../components/ProtectedRoute.jsx';
import AdminRoute from '../components/AdminRoute.jsx';

// ── Public Pages ─────────────────────────────────────────────
import WelcomePage from './pages/AppNestWelcome.jsx';
import LoginPage from './pages/Login.jsx';
import SignupPage from './pages/Signup.jsx';
import ForgotPassword from './pages/ForgotPassword.jsx';
import ResetPassword from './pages/ResetPassword.jsx';

// ── User Realms ──────────────────────────────────────────────
import HomePortal from '../realms/home/HomePortal.jsx';
import ArcadeRealm from '../realms/arcade/ArcadeRealm.jsx';
import ForgeRealm from '../realms/forge/ForgeRealm.jsx';
import RoastRealm from '../realms/roast/RoastRealm.jsx';
import ProfileRealm from '../realms/profile/ProfileRealm.jsx';
import Achievements from '../realms/profile/Achievements.jsx';
import Leaderboard from '../realms/social/Leaderboard.jsx';
import SocialHub from '../realms/social/SocialHub.jsx';
import ModuleLoader from '../components/Module/ModuleLoader.jsx';
import Settings from './pages/Settings.jsx';

// ── Admin Realms ─────────────────────────────────────────────
import AdminOverview from '../admin/overview/AdminOverview.jsx';
import UserManagement from '../admin/users/UserManagement.jsx';
import GameAnalytics from '../admin/games/GameAnalytics.jsx';
import ToolAnalytics from '../admin/tools/ToolAnalytics.jsx';
import RoastModeration from '../admin/roast/RoastModeration.jsx';
import PlatformAnalytics from '../admin/analytics/PlatformAnalytics.jsx';
import SystemSettings from '../admin/settings/SystemSettings.jsx';
import ModuleManager from '../admin/modules/ModuleManager.jsx';

import { useAuthStore } from '../store/authStore';

// Loading spinner used as Suspense fallback
const RealmLoading = () => (
    <div className="flex items-center justify-center h-screen bg-deep-black">
        <div className="w-12 h-12 border-4 border-neon-blue border-t-transparent rounded-full animate-spin" />
    </div>
);

const AppRouter = () => {
    const isInitializing = useAuthStore(state => state.isInitializing);

    if (isInitializing) {
        return <RealmLoading />;
    }
    return (
        <Routes>
            {/* ── Public Routes ──────────────────────────────── */}
            <Route path="/" element={<WelcomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password" element={<ResetPassword />} />

            {/* ── Settings Page (Protected) ──────────────────── */}
            <Route element={<ProtectedRoute requiredRole="user" />}>
                <Route path="/settings" element={<Settings />} />
            </Route>

            {/* ── Protected Dashboard Shell ──────────────────── */}
            <Route element={<ProtectedRoute requiredRole="user" />}>
                <Route path="/dashboard" element={<AppShell />}>

                    {/* User Realms */}
                    <Route index element={<React.Suspense fallback={<RealmLoading />}><HomePortal /></React.Suspense>} />
                    <Route path="profile" element={<ProfileRealm />} />
                    <Route path="achievements" element={<Achievements />} />
                    <Route path="games" element={<ArcadeRealm />} />
                    <Route path="tools" element={<ForgeRealm />} />
                    <Route path="roast" element={<RoastRealm />} />
                    <Route path="leaderboard" element={<Leaderboard />} />
                    <Route path="social" element={<SocialHub />} />
                    <Route path="module/:slug" element={<ModuleLoader />} />

                    {/* ── Admin Sub-Routes (guarded by AdminRoute) ── */}
                    <Route element={<AdminRoute />}>
                        <Route path="admin" element={<AdminOverview />} />
                        <Route path="admin/users" element={<UserManagement />} />
                        <Route path="admin/games" element={<GameAnalytics />} />
                        <Route path="admin/tools" element={<ToolAnalytics />} />
                        <Route path="admin/roast" element={<RoastModeration />} />
                        <Route path="admin/analytics" element={<PlatformAnalytics />} />
                        <Route path="admin/settings" element={<SystemSettings />} />
                        <Route path="admin/modules" element={<ModuleManager />} />
                    </Route>

                </Route>
            </Route>

            {/* Catch-all → home */}
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
};

export default AppRouter;

