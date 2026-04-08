import apiClient from './apiClient'; // Updated imported reference

export const gameService = {
    getGames: () => apiClient.get('/games'),
    getLeaderboard: (gameId) => apiClient.get(`/games/${gameId}/leaderboard`),
    // completeGame is removed. Use moduleExecutionService.execute instead.
};

export const roastService = {
    getRoast: (name) => apiClient.get(`/roast/game/${name}`),
    getGlobalStats: () => apiClient.get('/roast/stats'),
};
