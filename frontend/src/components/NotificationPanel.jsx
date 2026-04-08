/**
 * NotificationPanel.jsx
 * 
 * Industry-level notification bell dropdown panel.
 * Shows XP, streak, level-up, achievements and general app notifications.
 * Closes on outside click. Marks items as read when panel opens
 */
import React, { useRef, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Bell, Zap, Flame, Trophy, Star, Info, AlertCircle,
    CheckCheck, Trash2, X
} from 'lucide-react';
import { useNotificationStore } from '../store/notificationStore';
import { createPortal } from "react-dom";

// ── Type config ────────────────────────────────────────────────
const TYPE_META = {
    xp: { icon: Zap, color: 'text-neon-blue', bg: 'bg-neon-blue/10', border: 'border-neon-blue/20', label: 'XP Earned' },
    level_up: { icon: Star, color: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'border-yellow-500/20', label: 'Level Up!' },
    streak: { icon: Flame, color: 'text-orange-400', bg: 'bg-orange-500/10', border: 'border-orange-500/20', label: 'Streak' },
    achievement: { icon: Trophy, color: 'text-neon-pink', bg: 'bg-neon-pink/10', border: 'border-neon-pink/20', label: 'Achievement' },
    info: { icon: Info, color: 'text-gray-300', bg: 'bg-white/5', border: 'border-white/10', label: 'Info' },
    error: { icon: AlertCircle, color: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/20', label: 'Alert' },
};

const DEFAULT_META = TYPE_META.info;

// ── Relative time formatter ────────────────────────────────────
const timeAgo = (date) => {
    const diff = Date.now() - new Date(date).getTime();
    const s = Math.floor(diff / 1000);
    if (s < 60) return 'just now';
    const m = Math.floor(s / 60);
    if (m < 60) return `${m}m ago`;
    const h = Math.floor(m / 60);
    if (h < 24) return `${h}h ago`;
    return `${Math.floor(h / 24)}d ago`;
};

// ── Single notification row ────────────────────────────────────
const NotifRow = ({ notif, onRead }) => {
    const meta = TYPE_META[notif.type] ?? DEFAULT_META;
    const Icon = meta.icon;

    return (
        <motion.div
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, x: 20 }}
            onClick={() => onRead(notif.id)}
            className={`relative flex items-start gap-3 px-4 py-3 cursor-pointer transition-all
                ${notif.seen ? 'opacity-50 hover:opacity-70' : 'hover:bg-white/5'}
                border-b border-white/5 last:border-0`}
        >
            {/* Unread dot */}
            {!notif.is_read && (
                <span className="absolute top-4 right-4 w-1.5 h-1.5 bg-neon-blue rounded-full animate-pulse" />
            )}

            {/* Icon */}
            <div className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center mt-0.5
                ${meta.bg} border ${meta.border}`}>
                <Icon size={14} className={meta.color} />
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0 pr-4">
                <div className="flex items-center gap-2 flex-wrap">
                    <span className={`text-[10px] font-black uppercase tracking-widest ${meta.color}`}>
                        {meta.label}
                    </span>
                    {notif.type === 'xp' && notif.amount && (
                        <span className="text-[10px] font-black text-neon-blue bg-neon-blue/10 px-1.5 py-0.5 rounded-full">
                            +{notif.amount} XP
                        </span>
                    )}
                    {notif.type === 'streak' && notif.streak && (
                        <span className="text-[10px] font-black text-orange-400">
                            🔥 {notif.streak} days
                        </span>
                    )}
                </div>
                {notif.title && (
                    <p className="text-sm font-bold text-white mt-0.5 leading-tight">{notif.title}</p>
                )}
                {notif.message && (
                    <p className="text-xs text-gray-400 leading-snug mt-0.5 line-clamp-2">{notif.message}</p>
                )}
                <p className="text-[10px] text-gray-600 mt-1">{timeAgo(notif.timestamp)}</p>
            </div>
        </motion.div>
    );
};

// ── Main Panel ─────────────────────────────────────────────────
const NotificationPanel = () => {
    const [open, setOpen] = React.useState(false);
    const [rect, setRect] = React.useState(null);
    const panelRef = useRef(null);
    const btnRef = useRef(null);

    const { notifications, unreadCount, markAsRead, markAllAsRead, clearAll, fetchNotifications } = useNotificationStore();
    const unread = unreadCount;

    // Close on outside click
    useEffect(() => {
        const handler = (e) => {
            if (
                panelRef.current && !panelRef.current.contains(e.target) &&
                btnRef.current && !btnRef.current.contains(e.target)
            ) {
                setOpen(false);
            }
        };
        document.addEventListener('mousedown', handler);
        return () => document.removeEventListener('mousedown', handler);
    }, []);

    // When opening panel, fetch latest notifications if needed
    const handleOpen = useCallback(async () => {
        const willOpen = !open;
        setOpen(willOpen);

        if (willOpen && btnRef.current) {
            const r = btnRef.current.getBoundingClientRect();
            setRect(r);

            await fetchNotifications();
        }
    }, [open, fetchNotifications]);

    return (
        <div className="relative">
            {/* Bell Button */}
            <button
                ref={btnRef}
                id="notification-bell-btn"
                onClick={handleOpen}
                className="relative p-2 rounded-lg hover:bg-white/10 text-gray-400 hover:text-white transition-all"
                aria-label="Notifications"
            >
                <Bell size={20} />
                <AnimatePresence>
                    {unread > 0 && (
                        <motion.span
                            key="badge"
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            exit={{ scale: 0 }}
                            className="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] bg-neon-pink text-[9px] text-white font-black rounded-full flex items-center justify-center px-1 shadow-[0_0_8px_rgba(255,0,128,0.6)]"
                        >
                            {unread > 99 ? '99+' : unread}
                        </motion.span>
                    )}
                </AnimatePresence>
            </button>

            {/* Dropdown Panel */}
            {createPortal(
                <AnimatePresence>
                    {open && (
                        <motion.div
                            ref={panelRef}
                            initial={{ opacity: 0, y: -8, scale: 0.97 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            exit={{ opacity: 0, y: -8, scale: 0.97 }}
                            className="fixed w-96 max-h-[70vh] flex flex-col rounded-2xl bg-dark-surface/95 backdrop-blur-xl border border-white/10 shadow-[0_8px_40px_rgba(0,0,0,0.6)] z-[9999] overflow-hidden"
                            style={{
                                top: rect ? rect.bottom + 8 : 80,
                                left: rect ? rect.right - 384 : window.innerWidth - 420
                            }}
                        >
                            {/* Header */}
                            <div className="flex items-center justify-between px-4 py-3 border-b border-white/10 flex-shrink-0">
                                <div className="flex items-center gap-2">
                                    <Bell size={16} className="text-neon-blue" />
                                    <h3 className="text-sm font-black text-white">Notifications</h3>
                                    {unread > 0 && (
                                        <span className="text-[9px] font-black bg-neon-pink/20 text-neon-pink px-1.5 py-0.5 rounded-full border border-neon-pink/30">
                                            {unread} new
                                        </span>
                                    )}
                                </div>
                                <div className="flex items-center gap-2">
                                    {unread > 0 && (
                                        <button
                                            onClick={markAllAsRead}
                                            title="Mark all as read"
                                            className="p-1.5 rounded-lg text-gray-500 hover:text-neon-blue hover:bg-neon-blue/10 transition-all"
                                        >
                                            <CheckCheck size={14} />
                                        </button>
                                    )}
                                    {notifications.length > 0 && (
                                        <button
                                            onClick={clearAll}
                                            title="Clear all"
                                            className="p-1.5 rounded-lg text-gray-500 hover:text-red-400 hover:bg-red-500/10 transition-all"
                                        >
                                            <Trash2 size={14} />
                                        </button>
                                    )}
                                    <button
                                        onClick={() => setOpen(false)}
                                        className="p-1.5 rounded-lg text-gray-500 hover:text-white hover:bg-white/10 transition-all"
                                    >
                                        <X size={14} />
                                    </button>
                                </div>
                            </div>

                            {/* Notification List */}
                            <div className="flex-1 overflow-y-auto scrollbar-none">
                                <AnimatePresence initial={false}>
                                    {notifications.length === 0 ? (
                                        <motion.div
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            className="flex flex-col items-center justify-center py-14 text-center gap-3"
                                        >
                                            <div className="w-12 h-12 rounded-full bg-white/5 border border-white/10 flex items-center justify-center">
                                                <Bell size={20} className="text-gray-600" />
                                            </div>
                                            <p className="text-sm font-bold text-gray-500">No new notifications available.</p>
                                            <p className="text-[11px] text-gray-600">You can view past notifications here.</p>
                                        </motion.div>
                                    ) : (
                                        notifications.map(n => (
                                            <NotifRow
                                                key={n.id}
                                                notif={n}
                                                onRead={markAsRead}
                                            />
                                        ))
                                    )}
                                </AnimatePresence>
                            </div>

                            {/* Footer */}
                            {notifications.length > 0 && (
                                <div className="px-4 py-2 border-t border-white/5 flex-shrink-0">
                                    <p className="text-[10px] text-gray-600 text-center">
                                        {notifications.length} total · {unread} unread
                                    </p>
                                </div>
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>,
                document.body
            )}
        </div>
    );
}

export default NotificationPanel;
