import axios from './axios';

/**
 * Roast API Service
 * Handles all roast-related API calls
 */

const roastApi = {
  // Get roasts
  getNormalRoast: () =>
    axios.get('/roast/normal'),

  getPersonalRoast: (name) =>
    axios.post('/roast/personal', { name }),

  getUltraRoast: () =>
    axios.get('/roast/ultra'),

  getGameRoast: (gameName) =>
    axios.get(`/roast/game/${gameName}`),

  getToolRoast: (toolName) =>
    axios.get(`/roast/tool/${toolName}`),

  getRandomRoast: () =>
    axios.get('/roast/random'),
};

export default roastApi;
