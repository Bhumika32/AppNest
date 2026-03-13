import { create } from 'zustand';
import { adminService } from '../api/adminService';

export const useAdminAnalyticsStore = create((set) => ({
    stats: {
        activeUsers: 0,
        platformGrowth: [],
        gamePopularity: [],
        toolUsage: [],
        matchesToday: 0,
        toolUsageCount: 0,
        roastBattles: 0,
        systemHealth: 'optimal'
    },
    isLoading: false,
    error: null,

    fetchStats: async () => {
        set({ isLoading: true });
        try {
            const [overview, growth, games, tools] = await Promise.all([
                adminService.getOverview(),
                adminService.getGrowth(),
                adminService.getGamePopularity(),
                adminService.getToolUsage()
            ]);

            set({
                stats: {
                    activeUsers: overview.data.activeUsers,
                    platformGrowth: growth.data,
                    gamePopularity: games.data,
                    toolUsage: tools.data,
                    matchesToday: overview.data.matchesToday,
                    toolUsageCount: overview.data.toolUsage,
                    roastBattles: overview.data.roastBattles,
                    systemHealth: overview.data.systemHealth
                },
                isLoading: false
            });
        } catch (err) {
            set({ error: 'System telemetry offline', isLoading: false });
        }
    }
}));
