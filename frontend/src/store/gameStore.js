import { create } from 'zustand';

export const useGameStore = create((set) => ({
    games: [
        { id: 'neon-runner', title: 'Neon Runner', genre: 'Arcade', status: 'ready' },
        { id: 'cipher-break', title: 'Cipher Break', genre: 'Puzzle', status: 'maintenance' },
    ],
    recentGames: [],
    matchHistory: [],

    launchGame: (gameId) => {
        console.log(`Launching game: ${gameId}`);
    },

    addMatch: (match) => set((state) => ({
        matchHistory: [match, ...state.matchHistory]
    }))
}));
