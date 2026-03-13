import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './layout/Sidebar/Sidebar.jsx';
import Header from './layout/Header/Header.jsx';
import Footer from './layout/Footer/Footer.jsx';
import { motion, AnimatePresence } from 'framer-motion';
import { useUserStore } from '../store/userStore.js';
import { useAdminAnalyticsStore } from '../store/adminAnalyticsStore.js';
import { useAuthStore } from '../store/authStore.js';
import { useModuleStore } from '../store/moduleStore.js';
import { useUIStore } from '../store/uiStore.js';
import { useNotificationStore } from '../store/notificationStore.js';
import ErrorBoundary from '../components/ErrorBoundary.jsx';
import ToastManager from '../components/ToastManager.jsx';
import SystemOverlayManager from '../components/SystemOverlayManager.jsx';

// ---------------------------------------------------------
// AppShell Content and Logic
// ---------------------------------------------------------
const AppShellContent = () => {
    const fetchDashboard = useUserStore(state => state.fetchDashboard);
    const level = useUserStore(state => state.level);
    const fetchStats = useAdminAnalyticsStore(state => state.fetchStats);
    const fetchModules = useModuleStore(state => state.fetchModules);
    const role = useAuthStore(state => state.role);
    const checkAndUpdateStreak = useUIStore(state => state.checkAndUpdateStreak);
    const notify = useNotificationStore(state => state.notify);
    const initSocket = useNotificationStore(state => state.initSocket);
    const disconnectSocket = useNotificationStore(state => state.disconnectSocket);

    // Track previous level to detect level-ups
    const prevLevelRef = React.useRef(level);

    // ---------------------------------------------------------
    // Streak check on mount (fires once per session login)
    // ---------------------------------------------------------
    React.useEffect(() => {
        const result = checkAndUpdateStreak();
        if (result?.isNew) {
            if (result.broken) {
                notify({
                    type: 'streak',
                    title: 'Streak Reset',
                    message: "You missed a day — but you're back! Let's rebuild that streak.",
                    streak: 1,
                });
            } else if (result.streak === 1) {
                notify({
                    type: 'streak',
                    title: 'Welcome Back!',
                    message: 'Your journey continues today.',
                    streak: 1,
                });
            } else {
                notify({
                    type: 'streak',
                    title: `${result.streak} Day Streak! 🔥`,
                    message: result.streak >= 7
                        ? "You're on fire! Keep the momentum going."
                        : 'Consistency is your superpower.',
                    streak: result.streak,
                });
            }
        }
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    // ---------------------------------------------------------
    // Level-up detector — watches userStore.level
    // ---------------------------------------------------------
    React.useEffect(() => {
        if (prevLevelRef.current !== undefined && level > prevLevelRef.current) {
            notify({
                type: 'level_up',
                title: `LEVEL UP! → LVL ${level}`,
                message: 'New abilities unlocked. The Nest grows stronger.',
            });
        }
        prevLevelRef.current = level;
    }, [level, notify]);

    // ---------------------------------------------------------
    // Initial System Sync (Mount Only)
    // ---------------------------------------------------------
    React.useEffect(() => {
        fetchDashboard();
        fetchModules();
        initSocket();
        if (role === 'admin') fetchStats();

        return () => disconnectSocket();
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    return (
        <div className="flex h-screen w-screen bg-dark-bg text-white overflow-hidden font-sans">
            {/* Background Anime/Cyberpunk Visuals */}
            <div className="fixed inset-0 pointer-events-none z-0">
                <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_50%_50%,rgba(0,243,255,0.05),transparent_70%)]" />
                <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-10" />
            </div>

            {/* Sidebar Navigation */}
            <Sidebar />

            {/* Main Container */}
            <div className="flex-1 flex flex-col relative z-10 overflow-hidden">
                <Header />

                {/* Workspace Area */}
                <main className="flex-1 overflow-y-auto overflow-x-hidden p-6 relative">
                    <ErrorBoundary>
                        <AnimatePresence mode="wait">
                            <motion.div
                                key={window.location.pathname}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                transition={{ duration: 0.3 }}
                                className="min-h-full"
                            >
                                <Outlet />
                            </motion.div>
                        </AnimatePresence>
                    </ErrorBoundary>
                </main>

                <Footer />
            </div>

            {/* Screen Overlay (Scanlines) */}
            <div className="fixed inset-0 pointer-events-none z-[100] opacity-[0.03] bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_2px,3px_100%]" />

            {/* 🔔 Toast Notification Layer */}
            <ToastManager />

            {/* 🎭 Feedback Overlay Layer (Roasts & Tips) */}
            <SystemOverlayManager />
        </div>
    );
};

const AppShell = () => (
    <AppShellContent />
);

export default AppShell;

