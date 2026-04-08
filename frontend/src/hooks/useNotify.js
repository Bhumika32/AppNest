/**
 * useNotify.js
 * Convenience hook to fire typed toasts from any component.
 *
 * Usage:
 *   const { notifyXp, notifyAchievement, notifyInfo } = useNotify();
 *   notifyXp(50);                           // "+50 XP earned"
 *   notifyXp(100, 'Challenge Complete!');   // Custom title
 *   notifyAchievement('First Roast!');
 *   notifyInfo('Saving your profile...');
 */
import { useCallback } from 'react';
import { useNotificationStore } from '../store/notificationStore';

export const useNotify = () => {
    const { notify } = useNotificationStore();

    const notifyXp = useCallback((amount, title = 'XP Earned') => {
        notify({
            type: 'xp',
            title,
            message: `Keep going — every action earns XP!`,
            amount,
        });
    }, [notify]);

    const notifyStreak = useCallback((streak) => {
        notify({
            type: 'streak',
            title: `${streak} Day Streak! 🔥`,
            message: streak >= 7 ? "You're absolutely on fire!" : 'Consistency wins.',
            streak,
        });
    }, [notify]);

    const notifyLevelUp = useCallback((level) => {
        notify({
            type: 'level_up',
            title: `LEVEL UP! → LVL ${level}`,
            message: 'New abilities unlocked. The Nest grows stronger.',
        });
    }, [notify]);

    const notifyAchievement = useCallback((title, message = 'Achievement unlocked on your journey.') => {
        notify({ type: 'achievement', title, message });
    }, [notify]);

    const notifyInfo = useCallback((message, title) => {
        notify({ type: 'info', title, message });
    }, [notify]);

    const notifyError = useCallback((message, title = 'Error') => {
        notify({ type: 'error', title, message });
    }, [notify]);

    return { notifyXp, notifyStreak, notifyLevelUp, notifyAchievement, notifyInfo, notifyError };
};

export default useNotify;
