from app.platform.module_executor import ModuleExecutor

"""
app/services/games/flappy_bird.py

Flappy Bird game service with scoring and difficulty progression.

Features:
- Score calculation
- Difficulty modes
- High score tracking
- Game state management
"""

from dataclasses import dataclass


@dataclass
class FlappyBirdGameState:
    """Represents the current state of Flappy Bird game."""
    score: int
    high_score: int
    difficulty: str
    pipes_passed: int
    status: str  # 'ongoing', 'game_over', 'paused'
    message: str


class FlappyBirdService:
    """Service class for Flappy Bird game logic."""

    DIFFICULTY_MODES = {
        'easy': {'pipe_gap': 120, 'gravity': 0.5, 'speed': 4},
        'normal': {'pipe_gap': 100, 'gravity': 0.6, 'speed': 5},
        'hard': {'pipe_gap': 80, 'gravity': 0.7, 'speed': 6},
        'extreme': {'pipe_gap': 60, 'gravity': 0.8, 'speed': 7},
    }

    @staticmethod
    def calculate_score(pipes_passed: int, difficulty: str) -> int:
        """
        Calculate score based on pipes passed and difficulty.
        
        Args:
            pipes_passed: Number of pipes successfully passed
            difficulty: Difficulty mode
            
        Returns:
            Calculated score
        """
        multipliers = {
            'easy': 1,
            'normal': 1.5,
            'hard': 2,
            'extreme': 3,
        }
        base_score = pipes_passed * 10
        multiplier = multipliers.get(difficulty, 1)
        return int(base_score * multiplier)

    @staticmethod
    def validate_difficulty(difficulty: str) -> bool:
        """Check if difficulty mode is valid."""
        return difficulty in FlappyBirdService.DIFFICULTY_MODES

    @staticmethod
    def get_difficulty_config(difficulty: str) -> dict:
        """Get configuration for specific difficulty."""
        return FlappyBirdService.DIFFICULTY_MODES.get(difficulty, {})

    @staticmethod
    def get_gravity(difficulty: str) -> float:
        """Get gravity constant for difficulty."""
        config = FlappyBirdService.get_difficulty_config(difficulty)
        return config.get('gravity', 0.5)

    @staticmethod
    def get_pipe_speed(difficulty: str) -> float:
        """Get pipe movement speed for difficulty."""
        config = FlappyBirdService.get_difficulty_config(difficulty)
        return config.get('speed', 5)

    @staticmethod
    def get_pipe_gap(difficulty: str) -> int:
        """Get vertical gap between pipes for difficulty."""
        config = FlappyBirdService.get_difficulty_config(difficulty)
        return config.get('pipe_gap', 100)

    @staticmethod
    def create_game_state(
        pipes_passed: int = 0,
        difficulty: str = 'normal',
        high_score: int = 0
    ) -> FlappyBirdGameState:
        """
        Create initial or updated game state.
        
        Args:
            pipes_passed: Number of pipes passed
            difficulty: Game difficulty mode
            high_score: Best score so far
            
        Returns:
            FlappyBirdGameState object
        """
        if not FlappyBirdService.validate_difficulty(difficulty):
            difficulty = 'normal'

        calculated_score = FlappyBirdService.calculate_score(pipes_passed, difficulty)
        config = FlappyBirdService.get_difficulty_config(difficulty)

        return FlappyBirdGameState(
            score=calculated_score,
            high_score=max(calculated_score, high_score),
            difficulty=difficulty,
            pipes_passed=pipes_passed,
            status='ongoing',
            message=f"Difficulty: {difficulty.capitalize()} | Pipes: {pipes_passed}"
        )



from app.platform.module_result import ModuleResult

import logging
logger = logging.getLogger(__name__)

class FlappyBirdExecutor(ModuleExecutor):
    module_key = "flappy-bird"

    def execute(self, payload: dict, user) -> ModuleResult:
        logger.info(f"Executing Flappy Bird for user: {user.id}")
        score = int(payload.get("score", 0))
        win = bool(payload.get("win", False))
        status = payload.get("status", "completed")
        
        # Consider game completed if status is game_over or explicitly marked as win
        is_completed = status == "game_over" or win or payload.get("completed")
        
        return ModuleResult(
            completed=is_completed,
            score=score,
            status="win" if win else "lose" if status == "game_over" else "success",
            data={
                "win": win,
                "metadata": payload.get("metadata", {})
            }
        )
