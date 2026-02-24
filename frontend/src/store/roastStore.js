import { create } from 'zustand';

export const useRoastStore = create((set) => ({
    activePersonality: 'sarcastic-sage',
    history: [],
    personalities: [
        { id: 'sarcastic-sage', name: 'Sarcastic Sage' },
        { id: 'brutal-bard', name: 'Brutal Bard' },
    ],

    setPersonality: (id) => set({ activePersonality: id }),
    addRoast: (roast) => set((state) => ({
        history: [roast, ...state.history]
    }))
}));
