import apiClient from './apiClient';

export const gameService = {
    getGames: () => apiClient.get('/games'),
    getLeaderboard: (gameId) => apiClient.get(`/games/${gameId}/leaderboard`),
    completeGame: (payload) => apiClient.post('/games/complete', payload),
};

export const roastService = {
    getRoast: (name) => apiClient.get(`/roast/game/${name}`),
    getGlobalStats: () => apiClient.get('/roast/stats'),
};
