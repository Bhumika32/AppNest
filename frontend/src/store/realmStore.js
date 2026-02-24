import { create } from 'zustand';

export const useRealmStore = create((set) => ({
    currentRealm: 'home',
    isSidebarCollapsed: false,

    setCurrentRealm: (realm) => set({ currentRealm: realm }),
    toggleSidebar: () => set((state) => ({ isSidebarCollapsed: !state.isSidebarCollapsed })),
    setSidebarCollapsed: (isCollapsed) => set({ isSidebarCollapsed: isCollapsed }),
}));
