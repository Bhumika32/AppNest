import axios from './axios';

/**
 * Games API Service
 * Handles all game-related API calls
 */

const gamesApi = {
  // TicTacToe
  getTicTacToeMove: (board) =>
    axios.post('/games/tictactoe/move', { board }),

  resetTicTacToe: () =>
    axios.post('/games/tictactoe/reset'),

  // Snake
  getSnakeScore: (length, difficulty) =>
    axios.post('/games/snake/score', { length, difficulty }),

  // Break Breaker
  getBreakBreakerLevel: (level) =>
    axios.get(`/games/break-breaker/level?level=${level}`),

  getBreakBreakerScore: (level, bricksBroken) =>
    axios.post('/games/break-breaker/score', { level, bricks_broken: bricksBroken }),

  // Flappy Bird
  getFlappyBirdScore: (pipesPassed, difficulty) =>
    axios.post('/games/flappy-bird/score', { pipes_passed: pipesPassed, difficulty }),

  // Game Roasts
  getGameRoast: (gameName) =>
    axios.get(`/roast/game/${gameName}`),

  // Complete game session and award credits
  completeGame: (payload) =>
    axios.post('/games/complete', payload),
};

export default gamesApi;
