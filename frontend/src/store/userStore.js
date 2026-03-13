import { create } from 'zustand';
import { UserService } from '../api/api';

export const useUserStore = create((set) => ({
    xp: 0,
    level: 1,
    nextLevelXp: 1000,
    rank: '#1,280',
    uptime: '1,240h',
    achievements: [],
    activities: [],

    // Performance Matrix Data (for charts)
    performanceHistory: [], // Initial state for performanceHistory
    // Daily Bounty Pool
    dailyQuests: [], // Initial state for dailyQuests

    isLoading: false,
    error: null,
    title: 'CYBER SCOUT',

    fetchDashboard: async () => {
        set({ isLoading: true, error: null });
        try {
            const { data } = await UserService.getDashboardSummary();
            const currentLevel = data.level || 1;
            const computedNextLevelXp = Math.floor(100 + Math.pow(currentLevel, 1.5) * 40);

            set({
                xp: data.xp || 0,
                level: currentLevel,
                nextLevelXp: computedNextLevelXp,
                rank: data.rank || '#???',
                title: data.title || 'CYBER SCOUT',
                uptime: data.uptime || '0h',
                performanceHistory: data.performance_history || [
                    { day: 'MON', xp: 2400 },
                    { day: 'TUE', xp: 1398 },
                    { day: 'WED', xp: 9800 },
                    { day: 'THU', xp: 3908 },
                    { day: 'FRI', xp: 4800 },
                    { day: 'SAT', xp: 3800 },
                    { day: 'SUN', xp: 4300 },
                ],
                dailyQuests: data.daily_quests || [],
                isLoading: false
            });
        } catch (err) {
            const errorMsg = err.response?.data?.error || err.message || 'Failed to sync with neural matrix';
            set({ error: errorMsg, isLoading: false });
        }
    },

    addXp: (amount) => set((state) => {
        let newXp = state.xp + amount;
        let newLevel = state.level;
        let nextLevelXp = state.nextLevelXp;

        // Level up logic
        while (newXp >= nextLevelXp) {
            newXp -= nextLevelXp;
            newLevel += 1;
            nextLevelXp = Math.floor(100 + Math.pow(newLevel, 1.5) * 40);
        }

        // Update history for the current day
        const today = new Date().toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase();
        const newHistory = [...state.performanceHistory];
        const todayEntry = newHistory.find(h => h.day === today);

        if (todayEntry) {
            todayEntry.xp += amount;
        } else {
            newHistory.push({ day: today, xp: amount });
            if (newHistory.length > 7) newHistory.shift();
        }

        return {
            xp: newXp,
            level: newLevel,
            nextLevelXp,
            performanceHistory: newHistory
        };
    }),

    updateQuestProgress: (id, progress) => set((state) => ({
        dailyQuests: state.dailyQuests.map(q => q.id === id ? { ...q, progress } : q)
    })),

    setStats: (stats) => set({ ...stats }),
    addAchievement: (achievement) => set((state) => ({
        achievements: [achievement, ...state.achievements].slice(0, 50)
    })),
}));
