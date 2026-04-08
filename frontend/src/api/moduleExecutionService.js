import apiClient from './apiClient';

/**
 * Executes a module (game or tool) via the unified execution pipeline.
 *
 * @param {string} slug - The module's unique slug
 * @param {object} payload - The execution payload (e.g., config, input data)
 * @returns {Promise<object>} The execution result, including any lifecycle events like XP
 */
import { useAuthStore } from '../store/authStore';

    export const ModuleExecutionService = {
        execute: async (slug, payload) => {

            const token = useAuthStore.getState().token;

            // 🚫 HARD BLOCK
            if (!token || token.split('.').length !== 3) {
                console.error("🚨 BLOCKED: Invalid token before execution");
                throw new Error("AUTH_NOT_READY");
            }

            const { data } = await apiClient.post(`/modules/execute/${slug}`, payload);
            return data;
        }
    };
export default ModuleExecutionService;
