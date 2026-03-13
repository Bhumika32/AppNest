import apiClient from './apiClient';

/**
 * Executes a module (game or tool) via the unified execution pipeline.
 *
 * @param {string} slug - The module's unique slug
 * @param {object} payload - The execution payload (e.g., config, input data)
 * @returns {Promise<object>} The execution result, including any lifecycle events like XP
 */
export const ModuleExecutionService = {
    execute: async (slug, payload) => {
        try {
            const { data } = await apiClient.post(`/modules/execute/${slug}`, payload);
            return data;
        } catch (err) {
            console.error(`ModuleExecutionService error for ${slug}:`, err);
            throw err;
        }
    }
};

export default ModuleExecutionService;
