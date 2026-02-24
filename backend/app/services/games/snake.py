"""
app/services/games/snake.py

Snake game service with scoring and difficulty levels.

Features:
- Score calculation based on difficulty
- Collision detection
- Food generation
- Grid management
"""

from dataclasses import dataclass
from typing import List, Tuple
import random


@dataclass
class SnakeGameState:
    """Represents the current state of Snake game."""
    score: int
    length: int
    difficulty: int
    level: str
    high_score: int
    status: str  # 'ongoing', 'game_over', 'level_up'
    message: str


class SnakeService:
    """Service class for Snake game logic."""

    DIFFICULTY_LEVELS = {
        1: {"name": "Easy", "speed": 1, "multiplier": 1},
        2: {"name": "Medium", "speed": 2, "multiplier": 1.5},
        3: {"name": "Hard", "speed": 3, "multiplier": 2},
        4: {"name": "Insane", "speed": 4, "multiplier": 3},
    }

    @staticmethod
    def calculate_score(length: int, difficulty: int) -> int:
        """
        Calculate score based on snake length and difficulty.
        
        Args:
            length: Current snake length
            difficulty: Difficulty level (1-4)
            
        Returns:
            Calculated score
        """
        multiplier = SnakeService.DIFFICULTY_LEVELS.get(difficulty, {}).get("multiplier", 1)
        base_score = (length - 3) * 10  # Start from length 3
        return int(base_score * multiplier)

    @staticmethod
    def validate_difficulty(difficulty: int) -> bool:
        """Check if difficulty level is valid."""
        return difficulty in SnakeService.DIFFICULTY_LEVELS

    @staticmethod
    def get_difficulty_info(difficulty: int) -> dict:
        """Get information about specific difficulty level."""
        return SnakeService.DIFFICULTY_LEVELS.get(difficulty, {})

    @staticmethod
    def generate_food(grid_width: int = 20, grid_height: int = 20) -> Tuple[int, int]:
        """
        Generate random food position on grid.
        
        Args:
            grid_width: Width of game grid
            grid_height: Height of game grid
            
        Returns:
            (x, y) coordinates of food
        """
        return (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))

    @staticmethod
    def calculate_level(score: int) -> str:
        """
        Determine level based on score.
        
        Args:
            score: Current game score
            
        Returns:
            Level name
        """
        if score >= 500:
            return "Master"
        elif score >= 300:
            return "Expert"
        elif score >= 150:
            return "Advanced"
        elif score >= 50:
            return "Intermediate"
        else:
            return "Beginner"

    @staticmethod
    def create_game_state(length: int, score: int, difficulty: int, high_score: int = 0) -> SnakeGameState:
        """Create initial game state."""
        calculated_score = SnakeService.calculate_score(length, difficulty)
        difficulty_info = SnakeService.get_difficulty_info(difficulty)
        
        return SnakeGameState(
            score=calculated_score,
            length=length,
            difficulty=difficulty,
            level=SnakeService.calculate_level(calculated_score),
            high_score=max(calculated_score, high_score),
            status='ongoing',
            message=f"Level: {difficulty_info.get('name', 'Unknown')}"
        )
