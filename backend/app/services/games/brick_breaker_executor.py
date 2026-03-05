from app.platform.module_executor import ModuleExecutor

"""
app/services/games/break_breaker.py

Break Breaker (Brick Breaker) game service.

Features:
- Scoring system
- Difficulty progression
- Level management
- Collision detection helpers
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class BreakBreakerGameState:
    """Represents the current state of Break Breaker game."""
    score: int
    level: int
    bricks_remaining: int
    lives: int
    status: str  # 'ongoing', 'level_complete', 'game_over', 'won'
    message: str


class BreakBreakerService:
    """Service class for Break Breaker game logic."""

    LEVEL_CONFIGS = {
        1: {"bricks": 15, "speed": 3, "difficulty": "Easy"},
        2: {"bricks": 20, "speed": 5, "difficulty": "Medium"},
        3: {"bricks": 25, "speed": 7, "difficulty": "Hard"},
        4: {"bricks": 30, "speed": 9, "difficulty": "Expert"},
        5: {"bricks": 40, "speed": 11, "difficulty": "Insane"},
    }

    @staticmethod
    def calculate_score(bricks_broken: int, level: int) -> int:
        """
        Calculate score based on bricks broken and level.
        
        Args:
            bricks_broken: Number of bricks destroyed
            level: Current game level (1-5)
            
        Returns:
            Calculated score
        """
        base_score = bricks_broken * 10
        level_multiplier = 1 + (level - 1) * 0.5
        return int(base_score * level_multiplier)

    @staticmethod
    def get_level_config(level: int) -> dict:
        """Get configuration for specific level."""
        return BreakBreakerService.LEVEL_CONFIGS.get(level, {})

    @staticmethod
    def is_level_complete(bricks_remaining: int) -> bool:
        """Check if all bricks have been broken."""
        return bricks_remaining == 0

    @staticmethod
    def validate_level(level: int) -> bool:
        """Check if level is valid."""
        return level in BreakBreakerService.LEVEL_CONFIGS

    @staticmethod
    def calculate_ball_speed(level: int) -> float:
        """Get ball speed for given level."""
        config = BreakBreakerService.get_level_config(level)
        return config.get("speed", 3) / 10.0

    @staticmethod
    def create_game_state(
        level: int = 1,
        score: int = 0,
        lives: int = 3,
        bricks_broken: int = 0
    ) -> BreakBreakerGameState:
        """Create initial or updated game state."""
        config = BreakBreakerService.get_level_config(level)
        calculated_score = BreakBreakerService.calculate_score(bricks_broken, level)
        bricks_remaining = config.get("bricks", 15) - bricks_broken

        if bricks_remaining <= 0:
            status = 'level_complete' if level < 5 else 'won'
            message = 'Level Complete!' if status == 'level_complete' else 'You Won!'
        elif lives <= 0:
            status = 'game_over'
            message = 'Game Over!'
        else:
            status = 'ongoing'
            message = f"Level {level}: {config.get('difficulty', 'Unknown')}"

        return BreakBreakerGameState(
            score=calculated_score,
            level=level,
            bricks_remaining=max(0, bricks_remaining),
            lives=lives,
            status=status,
            message=message
        )



class BrickBreakerExecutor(ModuleExecutor):
    module_key = "brick-breaker"

    def execute(self, payload: dict, user):
        score = int(payload.get("score", 0))
        win = bool(payload.get("win", False))
        
        return {
            "score": score,
            "win": win,
            "metadata": payload.get("metadata", {})
        }
