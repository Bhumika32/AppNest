import { create } from 'zustand';
import { ModuleService } from '../api/api';

export const useModuleStore = create((set, get) => ({
    modules: [],
    loading: false,
    error: null,

    fetchModules: async (type = null) => {
        set({ loading: true, error: null });
        try {
            const { data } = await ModuleService.getAll(type);
            set({ modules: data, loading: false });
        } catch (err) {
            set({ error: err.response?.data?.error || 'Failed to sync modules', loading: false });
        }
    },

    getModuleBySlug: (slug) => {
        return get().modules.find(m => m.slug === slug);
    },

    trackLaunch: async (moduleId) => {
        try {
            const { data } = await ModuleService.trackStart(moduleId);
            return data.entry_id;
        } catch (err) {
            console.error('Analytics failed to initiate:', err);
            return null;
        }
    },

    trackEnd: async (entryId, duration) => {
        try {
            await ModuleService.trackEnd(entryId, duration);
        } catch (err) {
            console.error('Analytics failed to finalize:', err);
        }
    }
}));
