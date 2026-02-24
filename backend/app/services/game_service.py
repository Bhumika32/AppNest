"""
app/services/game_service.py

Handles backend logic for mini-games.
"""

import random

class GameService:
    @staticmethod
    def get_tictactoe_move(board):
        """
        Simple AI for TicTacToe.
        Board is a list of 9 elements: 'X', 'O', or None/Empty string.
        AI plays as 'O'.
        """
        # 1. Check for winning move
        # 2. Block player winning move
        # 3. Take center
        # 4. Take random available
        
        available_moves = [i for i, x in enumerate(board) if not x]
        
        if not available_moves:
            return None, "Draw"

        # Simple random move for now to get it working (can be Minimax optimized later)
        move = random.choice(available_moves)
        return move, "Ongoing"

    @staticmethod
    def calculate_snake_score(length, difficulty):
        return length * 10 * difficulty
