from app.platform.module_executor import ModuleExecutor

"""
app/services/games/tictactoe.py

TicTacToe game service with intelligent AI opponent.

Features:
- Minimax algorithm for optimal AI moves
- Win detection
- Board validation
- Professional architecture
"""

from typing import Optional, Tuple
from dataclasses import dataclass
import random


@dataclass
class TicTacToeState:
    """Represents the current state of a TicTacToe game."""
    board: list  # 9-element list: 'X', 'O', or ''
    status: str  # 'ongoing', 'player_win', 'ai_win', 'draw'
    ai_move: Optional[int] = None
    message: Optional[str] = None


class TicTacToeService:
    """Service class for TicTacToe game logic."""

    WINNING_COMBINATIONS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6],              # Diagonals
    ]

    @staticmethod
    def validate_board(board: list) -> bool:
        """Validate board state."""
        if not isinstance(board, list) or len(board) != 9:
            return False
        for cell in board:
            if cell not in ['X', 'O', '']:
                return False
        return True

    @staticmethod
    def check_winner(board: list, player: str) -> bool:
        """Check if specified player has won."""
        for combo in TicTacToeService.WINNING_COMBINATIONS:
            if all(board[i] == player for i in combo):
                return True
        return False

    @staticmethod
    def get_available_moves(board: list) -> list:
        """Get all available empty positions."""
        return [i for i, cell in enumerate(board) if cell == '']

    @staticmethod
    def is_board_full(board: list) -> bool:
        """Check if board is completely filled."""
        return len(TicTacToeService.get_available_moves(board)) == 0

    @staticmethod
    def _minimax(board: list, depth: int, is_maximizing: bool) -> int:
        """Minimax algorithm for optimal AI moves."""
        # Check terminal states
        if TicTacToeService.check_winner(board, 'O'):
            return 10 - depth  # AI wins
        if TicTacToeService.check_winner(board, 'X'):
            return depth - 10  # Player wins
        if TicTacToeService.is_board_full(board):
            return 0  # Draw

        available = TicTacToeService.get_available_moves(board)

        if is_maximizing:  # AI's turn
            max_score = float('-inf')
            for move in available:
                board[move] = 'O'
                score = TicTacToeService._minimax(board, depth + 1, False)
                board[move] = ''
                max_score = max(score, max_score)
            return max_score
        else:  # Player's turn
            min_score = float('inf')
            for move in available:
                board[move] = 'X'
                score = TicTacToeService._minimax(board, depth + 1, True)
                board[move] = ''
                min_score = min(score, min_score)
            return min_score

    @staticmethod
    def get_ai_move(board: list) -> TicTacToeState:
        """
        Get the best AI move using minimax algorithm.
        
        Args:
            board: Current board state (9 elements: 'X', 'O', or '')
            
        Returns:
            TicTacToeState with AI move and game status
        """
        # Accept boards using None/null (from frontend) by normalizing here
        normalized = [cell if cell in ['X', 'O'] else '' for cell in board]
        if not TicTacToeService.validate_board(normalized):
            return TicTacToeState(
                board=board,
                status='error',
                message='Invalid board state'
            )

        # Check if player already won
        if TicTacToeService.check_winner(board, 'X'):
            return TicTacToeState(
                board=board,
                status='player_win',
                message='Player wins!'
            )

        # Check if AI already won
        if TicTacToeService.check_winner(board, 'O'):
            return TicTacToeState(
                board=board,
                status='ai_win',
                message='AI wins!'
            )

        # Work on normalized board for minimax
        available = TicTacToeService.get_available_moves(normalized)

        # No moves left - draw
        if not available:
            return TicTacToeState(
                board=board,
                status='draw',
                message='Game is a draw!'
            )

        # Find best AI move
        best_score = float('-inf')
        best_move = None

        for move in available:
            normalized[move] = 'O'
            score = TicTacToeService._minimax(normalized, 0, False)
            normalized[move] = ''
            
            if score > best_score:
                best_score = score
                best_move = move

        # Make the move on normalized board
        normalized[best_move] = 'O'

        # Update original board representation accordingly
        board[best_move] = 'O'

        # Check game status after AI move
        if TicTacToeService.check_winner(normalized, 'O'):
            return TicTacToeState(
                board=normalized,
                status='ai_win',
                ai_move=best_move,
                message='AI wins!'
            )

        if TicTacToeService.is_board_full(normalized):
            return TicTacToeState(
                board=normalized,
                status='draw',
                ai_move=best_move,
                message='Game is a draw!'
            )

        return TicTacToeState(
            board=normalized,
            status='ongoing',
            ai_move=best_move,
            message='Your turn!'
        )

    @staticmethod
    def reset_game() -> TicTacToeState:
        """Create a new game board."""
        return TicTacToeState(
            board=['', '', '', '', '', '', '', '', ''],
            status='ongoing',
            message='Game started. You are X, AI is O.'
        )



from app.platform.module_result import ModuleResult

class TicTacToeExecutor(ModuleExecutor):
    module_key = "tic-tac-toe"

    def execute(self, payload: dict, user) -> ModuleResult:
        score = int(payload.get("score", 0))
        win = bool(payload.get("win", False))
        status = payload.get("status", "completed")
        
        # In TicTacToe, player_win, ai_win, or draw means game is over
        is_completed = status in ["player_win", "ai_win", "draw"] or win
        
        return ModuleResult(
            completed=is_completed,
            score=score,
            status="win" if status == "player_win" or win else "lose" if status == "ai_win" else "draw" if status == "draw" else "success",
            data={
                "win": win,
                "status": status,
                "metadata": payload.get("metadata", {})
            }
        )
