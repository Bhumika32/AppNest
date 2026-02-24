/**
 * streakStore.js
 * Tracks daily login streaks entirely client-side using localStorage (via zustand persist).
 * Call `checkAndUpdateStreak()` on every app load from AppShell.
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const MIDNIGHT = (d) => {
    const n = new Date(d);
    n.setHours(0, 0, 0, 0);
    return n.getTime();
};

export const useStreakStore = create(
    persist(
        (set, get) => ({
            streak: 0,
            longestStreak: 0,
            lastLoginDate: null, // ISO date string

            /** Call on every authenticated app load */
            checkAndUpdateStreak: () => {
                const today = MIDNIGHT(new Date());
                const { lastLoginDate, streak, longestStreak } = get();

                if (!lastLoginDate) {
                    // First ever login
                    set({ streak: 1, longestStreak: 1, lastLoginDate: new Date().toISOString() });
                    return { isNew: true, streak: 1 };
                }

                const last = MIDNIGHT(new Date(lastLoginDate));
                const diffDays = Math.round((today - last) / (1000 * 60 * 60 * 24));

                if (diffDays === 0) {
                    // Already logged in today — no change
                    return { isNew: false, streak };
                } else if (diffDays === 1) {
                    // Consecutive day — extend streak
                    const newStreak = streak + 1;
                    const newLongest = Math.max(newStreak, longestStreak);
                    set({ streak: newStreak, longestStreak: newLongest, lastLoginDate: new Date().toISOString() });
                    return { isNew: true, streak: newStreak };
                } else {
                    // Streak broken
                    set({ streak: 1, lastLoginDate: new Date().toISOString() });
                    return { isNew: true, streak: 1, broken: true };
                }
            },

            reset: () => set({ streak: 0, longestStreak: 0, lastLoginDate: null }),
        }),
        {
            name: 'appnest-streak-storage',
        }
    )
);
