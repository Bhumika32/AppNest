import { create } from 'zustand';

export const useOverlayStore = create((set) => ({
    activeOverlay: null, // { type: 'roast' | 'mentor_tip', message: string, icon: string, color: string }

    showOverlay: (overlay) => set({ activeOverlay: overlay }),
    hideOverlay: () => set({ activeOverlay: null })
}));

export default useOverlayStore;
