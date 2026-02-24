import { create } from 'zustand';
import profileApi from '../api/profileApi';

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
            const { data } = await profileApi.getDashboardSummary();
            set({
                xp: data.xp || 0,
                level: data.level || 1,
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
        const newXp = state.xp + amount;
        // Update history for the current day (simplified)
        const newHistory = [...state.performanceHistory];
        // Ensure there's at least one entry or handle empty history
        if (newHistory.length > 0) {
            newHistory[newHistory.length - 1].xp += amount;
        } else {
            // If history is empty, add a placeholder or handle as needed
            newHistory.push({ day: 'Today', xp: amount, activity: 0 });
        }


        if (newXp >= state.nextLevelXp) {
            return {
                xp: newXp - state.nextLevelXp,
                level: state.level + 1,
                nextLevelXp: Math.floor(state.nextLevelXp * 1.2),
                performanceHistory: newHistory
            };
        }
        return { xp: newXp, performanceHistory: newHistory };
    }),

    updateQuestProgress: (id, progress) => set((state) => ({
        dailyQuests: state.dailyQuests.map(q => q.id === id ? { ...q, progress } : q)
    })),

    setStats: (stats) => set({ ...stats }),
    addAchievement: (achievement) => set((state) => ({
        achievements: [...state.achievements, achievement]
    })),
}));
