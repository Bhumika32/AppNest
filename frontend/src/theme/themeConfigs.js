export const DASHBOARD_THEMES = {
    FROST_WINTER: 'frost_winter',
    CHERRY_SPRING: 'cherry_spring',
    SUNSET_SUMMER: 'sunset_summer',
    AUTUMN_HARVEST: 'autumn_harvest',
    MIDNIGHT: 'midnight'
};

export const THEME_CONFIGS = {
    [DASHBOARD_THEMES.FROST_WINTER]: {
        id: DASHBOARD_THEMES.FROST_WINTER,
        name: 'Frost Winter',
        colors: {
            primary: '#00d9ff',
            secondary: '#0088ff',
            accent: '#1a5f7a',
            background: '#0a1628',
            text: '#e0f7fa',
            frostGradient: 'linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 136, 255, 0.05) 100%)',
            realmColors: {
                games: '#00d9ff',
                tools: '#0088ff',
                roast: '#ff1744',
                profile: '#00e676'
            }
        },
        effects: {
            frostEffect: 'backdrop-blur-xl bg-white/5 border border-cyan-400/30',
            glassEffect: 'bg-black/40 backdrop-blur-lg border border-cyan-300/20'
        }
    },
    [DASHBOARD_THEMES.CHERRY_SPRING]: {
        id: DASHBOARD_THEMES.CHERRY_SPRING,
        name: 'Cherry Spring',
        colors: {
            primary: '#ff1493',
            secondary: '#ff69b4',
            accent: '#ff85c0',
            background: '#fff5f7',
            text: '#881337',
            springGradient: 'linear-gradient(135deg, rgba(255, 20, 147, 0.1) 0%, rgba(255, 105, 180, 0.05) 100%)',
            realmColors: {
                games: '#ff1493',
                tools: '#ff69b4',
                roast: '#ff6b9d',
                profile: '#c2185b'
            }
        },
        effects: {
            frostEffect: 'backdrop-blur-xl bg-pink-50/70 border border-pink-400/40',
            glassEffect: 'bg-white/60 backdrop-blur-lg border border-pink-300/40'
        }
    },
    [DASHBOARD_THEMES.SUNSET_SUMMER]: {
        id: DASHBOARD_THEMES.SUNSET_SUMMER,
        name: 'Sunset Summer',
        colors: {
            primary: '#ff6b35',
            secondary: '#f7931e',
            accent: '#fbb03b',
            background: '#0d1b2a',
            text: '#fff7ed',
            sunsetGradient: 'linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(247, 147, 30, 0.05) 100%)',
            realmColors: {
                games: '#ff6b35',
                tools: '#f7931e',
                roast: '#fbb03b',
                profile: '#dc2743'
            }
        },
        effects: {
            frostEffect: 'backdrop-blur-xl bg-orange-50/10 border border-orange-400/40',
            glassEffect: 'bg-black/50 backdrop-blur-lg border border-orange-300/30'
        }
    },
    [DASHBOARD_THEMES.AUTUMN_HARVEST]: {
        id: DASHBOARD_THEMES.AUTUMN_HARVEST,
        name: 'Autumn Harvest',
        colors: {
            primary: '#d84315',
            secondary: '#bf360c',
            accent: '#ff9800',
            background: '#1a1410',
            text: '#fffbeb',
            autumnGradient: 'linear-gradient(135deg, rgba(216, 67, 21, 0.1) 0%, rgba(255, 152, 0, 0.05) 100%)',
            realmColors: {
                games: '#d84315',
                tools: '#ff9800',
                roast: '#ff5722',
                profile: '#795548'
            }
        },
        effects: {
            frostEffect: 'backdrop-blur-xl bg-amber-50/5 border border-amber-600/40',
            glassEffect: 'bg-black/60 backdrop-blur-lg border border-amber-700/30'
        }
    },
    [DASHBOARD_THEMES.MIDNIGHT]: {
        id: DASHBOARD_THEMES.MIDNIGHT,
        name: 'Midnight',
        colors: {
            primary: '#3b82f6',
            secondary: '#1e3a8a',
            accent: '#6366f1',
            background: '#0a0a0a',
            text: '#e5e5e5',
            realmColors: {
                games: '#3b82f6',
                tools: '#6366f1',
                roast: '#ef4444',
                profile: '#10b981'
            }
        },
        effects: {
            frostEffect: 'backdrop-blur-xl bg-black/50 border border-blue-900/40',
            glassEffect: 'bg-black/60 backdrop-blur-xl border border-white/5'
        }
    }
};
