import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { DASHBOARD_THEMES, THEME_CONFIGS } from '../theme/themeConfigs';

const useThemeStore = create(
    persist(
        (set, get) => ({
            currentThemeId: DASHBOARD_THEMES.FROST_WINTER,
            currentTheme: THEME_CONFIGS[DASHBOARD_THEMES.FROST_WINTER],

            setTheme: (themeId) => {
                const config = THEME_CONFIGS[themeId];
                if (config) {
                    set({ currentThemeId: themeId, currentTheme: config });
                }
            },

            // Helper to get all themes for UI
            getAllThemes: () => THEME_CONFIGS,
        }),
        {
            name: 'dashboard-theme-storage',
        }
    )
);

export default useThemeStore;
