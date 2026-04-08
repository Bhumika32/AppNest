/**
 * ToastManager.jsx
 * Renders floating XP/streak/level-up toasts anchored to the bottom-right of the screen.
 * Listens to useNotificationStore.toasts and animates each one in/out.
 *
 * Usage: Drop <ToastManager /> anywhere inside AppShell (outside overflow-hidden containers).
 */
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Flame, Trophy, Star, Info, AlertCircle, X } from 'lucide-react';
import { useNotificationStore } from '../store/notificationStore';

const TOAST_CONFIG = {
    xp: {
        icon: Zap,
        bg: 'bg-neon-blue/20 border-neon-blue/40',
        text: 'text-neon-blue',
        glow: 'shadow-[0_0_20px_rgba(0,243,255,0.25)]',
    },
    level_up: {
        icon: Star,
        bg: 'bg-yellow-500/20 border-yellow-500/40',
        text: 'text-yellow-400',
        glow: 'shadow-[0_0_30px_rgba(234,179,8,0.4)]',
    },
    streak: {
        icon: Flame,
        bg: 'bg-orange-500/20 border-orange-500/40',
        text: 'text-orange-400',
        glow: 'shadow-[0_0_20px_rgba(249,115,22,0.3)]',
    },
    achievement: {
        icon: Trophy,
        bg: 'bg-neon-pink/20 border-neon-pink/40',
        text: 'text-neon-pink',
        glow: 'shadow-[0_0_20px_rgba(255,0,128,0.25)]',
    },
    info: {
        icon: Info,
        bg: 'bg-white/10 border-white/20',
        text: 'text-white',
        glow: '',
    },
    error: {
        icon: AlertCircle,
        bg: 'bg-red-500/20 border-red-500/40',
        text: 'text-red-400',
        glow: '',
    },
};

const Toast = ({ toast }) => {
    const { dismissToast } = useNotificationStore();
    const cfg = TOAST_CONFIG[toast.type] ?? TOAST_CONFIG.info;
    const Icon = cfg.icon;

    return (
        <motion.div
            layout
            initial={{ opacity: 0, x: 80, scale: 0.9 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: 80, scale: 0.9 }}
            transition={{ type: 'spring', stiffness: 300, damping: 25 }}
            className={`relative flex items-start gap-3 px-4 py-3 rounded-xl border backdrop-blur-md max-w-xs w-full
                ${cfg.bg} ${cfg.glow}`}
        >
            {/* Icon */}
            <div className={`flex-shrink-0 mt-0.5 ${cfg.text}`}>
                <Icon size={18} />
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0">
                {toast.title && (
                    <p className={`text-sm font-bold leading-tight ${cfg.text}`}>{toast.title}</p>
                )}
                <p className="text-xs text-gray-300 leading-snug mt-0.5">{toast.message}</p>

                {/* XP amount badge */}
                {toast.type === 'xp' && toast.amount && (
                    <motion.span
                        initial={{ scale: 0.5, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ delay: 0.15 }}
                        className="inline-block mt-1 px-2 py-0.5 text-xs font-black text-neon-blue bg-neon-blue/10 rounded-full"
                    >
                        +{toast.amount} XP
                    </motion.span>
                )}

                {/* Streak count */}
                {toast.type === 'streak' && toast.streak && (
                    <p className="text-xs font-black text-orange-400 mt-0.5">
                        🔥 {toast.streak} day streak
                    </p>
                )}
            </div>

            {/* Dismiss */}
            <button
                onClick={() => dismissToast(toast.id)}
                className="flex-shrink-0 text-gray-500 hover:text-white transition-colors mt-0.5"
            >
                <X size={14} />
            </button>

            {/* Level-up shimmer */}
            {toast.type === 'level_up' && (
                <motion.div
                    className="absolute inset-0 rounded-xl bg-gradient-to-r from-yellow-500/0 via-yellow-500/20 to-yellow-500/0"
                    animate={{ x: ['-100%', '100%'] }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
                    style={{ mixBlendMode: 'screen' }}
                />
            )}
        </motion.div>
    );
};

const ToastManager = () => {
    const { toasts } = useNotificationStore();

    return (
        <div className="fixed bottom-6 right-6 z-[200] flex flex-col gap-2 items-end pointer-events-none">
            <AnimatePresence mode="popLayout">
                {toasts.map(toast => (
                    <div key={toast.id} className="pointer-events-auto">
                        <Toast toast={toast} />
                    </div>
                ))}
            </AnimatePresence>
        </div>
    );
};

export default ToastManager;
