import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { DASHBOARD_THEMES, THEME_CONFIGS } from '../theme/themeConfigs';

const MIDNIGHT = (d) => {
    const n = new Date(d);
    n.setHours(0, 0, 0, 0);
    return n.getTime();
};

export const useUIStore = create(
    persist(
        (set, get) => ({
            // Theme State
            currentThemeId: DASHBOARD_THEMES.FROST_WINTER,
            currentTheme: THEME_CONFIGS[DASHBOARD_THEMES.FROST_WINTER],

            setTheme: (themeId) => {
                const config = THEME_CONFIGS[themeId];
                if (config) {
                    set({ currentThemeId: themeId, currentTheme: config });
                }
            },
            getAllThemes: () => THEME_CONFIGS,

            // Realm & Navigation State
            currentRealm: 'home',
            isSidebarCollapsed: false,
            setCurrentRealm: (realm) => set({ currentRealm: realm }),
            toggleSidebar: () => set((state) => ({ isSidebarCollapsed: !state.isSidebarCollapsed })),
            setSidebarCollapsed: (isCollapsed) => set({ isSidebarCollapsed: isCollapsed }),

            // Streak State
            streak: 0,
            longestStreak: 0,
            lastLoginDate: null,
            checkAndUpdateStreak: () => {
                const today = MIDNIGHT(new Date());
                const { lastLoginDate, streak, longestStreak } = get();

                if (!lastLoginDate) {
                    set({ streak: 1, longestStreak: 1, lastLoginDate: new Date().toISOString() });
                    return { isNew: true, streak: 1 };
                }

                const last = MIDNIGHT(new Date(lastLoginDate));
                const diffDays = Math.round((today - last) / (1000 * 60 * 60 * 24));

                if (diffDays === 0) {
                    return { isNew: false, streak };
                } else if (diffDays === 1) {
                    const newStreak = streak + 1;
                    const newLongest = Math.max(newStreak, longestStreak);
                    set({ streak: newStreak, longestStreak: newLongest, lastLoginDate: new Date().toISOString() });
                    return { isNew: true, streak: newStreak };
                } else {
                    set({ streak: 1, lastLoginDate: new Date().toISOString() });
                    return { isNew: true, streak: 1, broken: true };
                }
            },
            resetStreak: () => set({ streak: 0, longestStreak: 0, lastLoginDate: null }),

            // Roast Module State
            roastHistory: [],
            addRoast: (roast) => set((state) => ({
                roastHistory: [
                    { ...roast, timestamp: new Date().toISOString() },
                    ...state.roastHistory
                ].slice(0, 50)
            })),
            clearRoasts: () => set({ roastHistory: [] }),
        }),
        {
            name: 'appnest-ui-storage',
            partialize: (state) => ({
                currentThemeId: state.currentThemeId,
                streak: state.streak,
                longestStreak: state.longestStreak,
                lastLoginDate: state.lastLoginDate,
                roastHistory: state.roastHistory
            }),
        }
    )
);

export default useUIStore;
