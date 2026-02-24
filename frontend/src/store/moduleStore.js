import { create } from 'zustand';
import axios from '../api/axios';

export const useModuleStore = create((set, get) => ({
    modules: [],
    loading: false,
    error: null,

    fetchModules: async (type = null) => {
        set({ loading: true, error: null });
        try {
            const url = type ? `/modules?type=${type}` : '/modules';
            const { data } = await axios.get(url);
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
            const { data } = await axios.post('/modules/analytics/start', { module_id: moduleId });
            return data.entry_id;
        } catch (err) {
            console.error('Analytics failed to initiate:', err);
            return null;
        }
    },

    trackEnd: async (entryId, duration) => {
        try {
            await axios.post('/modules/analytics/end', { entry_id: entryId, duration });
        } catch (err) {
            console.error('Analytics failed to finalize:', err);
        }
    }
}));
