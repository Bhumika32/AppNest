# -----------------------------------------------------------------------------
# File: backend/app/modules/games/tictactoe_executor.py
#
# FINAL FIXED VERSION (AI UPGRADE ONLY)
# - SOLO unchanged ✅
# - VS_AI flow unchanged ✅
# - PVP unchanged ✅
# - AI logic upgraded (easy / medium / hard) ✅
# -----------------------------------------------------------------------------

from app.platform.module_executor import ModuleExecutor
from app.platform.module_result import ModuleResult

from typing import Optional, List
from dataclasses import dataclass
import random
import logging

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# GAME STATE
# -----------------------------------------------------------------------------
@dataclass
class TicTacToeState:
    board: List[str]
    status: str
    ai_move: Optional[int] = None
    message: Optional[str] = None


# -----------------------------------------------------------------------------
# GAME LOGIC SERVICE
# -----------------------------------------------------------------------------
class TicTacToeService:

    WINNING_COMBINATIONS = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6],
    ]

    # -----------------------------
    # UTILITIES
    # -----------------------------
    @staticmethod
    def normalize(board: List[str]) -> List[str]:
        return [cell if cell in ["X", "O"] else "" for cell in board]

    @staticmethod
    def available(board: List[str]) -> List[int]:
        return [i for i, v in enumerate(board) if v == ""]

    @staticmethod
    def is_full(board: List[str]) -> bool:
        return len(TicTacToeService.available(board)) == 0

    @staticmethod
    def check_winner(board: List[str], player: str) -> bool:
        return any(all(board[i] == player for i in combo)
                   for combo in TicTacToeService.WINNING_COMBINATIONS)

    # -----------------------------
    # 🔥 MINIMAX (HARD AI)
    # -----------------------------
    @staticmethod
    def minimax(board, depth, is_maximizing):

        if TicTacToeService.check_winner(board, "O"):
            return 10 - depth

        if TicTacToeService.check_winner(board, "X"):
            return depth - 10

        if TicTacToeService.is_full(board):
            return 0

        if is_maximizing:
            best_score = -float("inf")

            for move in TicTacToeService.available(board):
                board[move] = "O"
                score = TicTacToeService.minimax(board, depth + 1, False)
                board[move] = ""
                best_score = max(score, best_score)

            return best_score

        else:
            best_score = float("inf")

            for move in TicTacToeService.available(board):
                board[move] = "X"
                score = TicTacToeService.minimax(board, depth + 1, True)
                board[move] = ""
                best_score = min(score, best_score)

            return best_score

    # -----------------------------
    # BEST MOVE (USED IN MEDIUM + HARD)
    # -----------------------------
    @staticmethod
    def best_move(board: List[str]) -> int:
        best_score = -float("inf")
        move = None

        for i in TicTacToeService.available(board):
            board[i] = "O"
            score = TicTacToeService.minimax(board, 0, False)
            board[i] = ""

            if score > best_score:
                best_score = score
                move = i

        return move

    # -----------------------------
    # AI SELECTOR (INDUSTRY STYLE)
    # -----------------------------
    @staticmethod
    def get_ai_move(board: List[str], difficulty: str) -> Optional[int]:

        moves = TicTacToeService.available(board)
        if not moves:
            return None

        # EASY → RANDOM
        if difficulty == "easy":
            return random.choice(moves)

        # MEDIUM → MIXED BEHAVIOR
        elif difficulty == "medium":
            if random.random() < 0.5:
                return random.choice(moves)
            return TicTacToeService.best_move(board)

        # HARD → MINIMAX (UNBEATABLE)
        else:
            return TicTacToeService.best_move(board)


# -----------------------------------------------------------------------------
# EXECUTOR (UNCHANGED LOGIC)
# -----------------------------------------------------------------------------
class TicTacToeExecutor(ModuleExecutor):

    module_key = "TicTacToeGame"

    def execute(self, payload: dict, user) -> ModuleResult:
        try:
            board = payload.get("board", [""] * 9)
            mode = str(payload.get("mode", "solo")).lower()
            difficulty = str(payload.get("difficulty", "easy")).lower()

            board = TicTacToeService.normalize(board)

            # -----------------------------
            # PLAYER WIN CHECK
            # -----------------------------
            if TicTacToeService.check_winner(board, "X"):
                return ModuleResult(
                    completed=True,
                    score=100,
                    status="player_win",
                    data={"board": board}
                )

            # -----------------------------
            # DRAW CHECK
            # -----------------------------
            if TicTacToeService.is_full(board):
                return ModuleResult(
                    completed=True,
                    score=50,
                    status="draw",
                    data={"board": board}
                )

            # =========================================================
            # SOLO (LOCAL PvP)
            # =========================================================
            if mode == "solo":

                move = payload.get("move")

                if move is None or board[move] != "":
                    return ModuleResult(False, status="invalid_move", data={"board": board})

                x_count = board.count("X")
                o_count = board.count("O")
                current_player = "X" if x_count == o_count else "O"

                board[move] = current_player

                if TicTacToeService.check_winner(board, current_player):
                    return ModuleResult(True, 100, f"{current_player}_win", data={"board": board})

                if TicTacToeService.is_full(board):
                    return ModuleResult(True, 50, "draw", data={"board": board})

                return ModuleResult(False, status="ongoing", data={"board": board})

            # =========================================================
            # VS AI (UNCHANGED FLOW)
            # =========================================================
            if mode == "vs_ai":

                move = payload.get("move")

                if move is None or board[move] != "":
                    return ModuleResult(False, status="invalid_move", data={"board": board})

                # Player move
                board[move] = "X"

                if TicTacToeService.check_winner(board, "X"):
                    return ModuleResult(True, 100, "player_win", data={"board": board})

                if TicTacToeService.is_full(board):
                    return ModuleResult(True, 50, "draw", data={"board": board})

                # AI move (NOW FIXED)
                ai_move = TicTacToeService.get_ai_move(board, difficulty)

                if ai_move is not None:
                    board[ai_move] = "O"

                if TicTacToeService.check_winner(board, "O"):
                    return ModuleResult(True, 10, "ai_win", data={"board": board, "ai_move": ai_move})

                if TicTacToeService.is_full(board):
                    return ModuleResult(True, 50, "draw", data={"board": board})

                return ModuleResult(False, status="ongoing", data={"board": board, "ai_move": ai_move})

            # =========================================================
            # FUTURE PVP
            # =========================================================
            if mode == "pvp":
                return ModuleResult(
                    completed=False,
                    status="waiting",
                    message="Online PvP not implemented yet",
                    data={"board": board}
                )

            return ModuleResult(False, status="error", message=f"Invalid mode: {mode}")

        except Exception as e:
            logger.exception("TicTacToe execution failed")

            return ModuleResult(
                completed=False,
                status="error",
                error="EXECUTION_FAILED",
                message=str(e),
                data={"board": payload.get("board", [])}
            )
# # -----------------------------------------------------------------------------
# # File: backend/app/modules/games/tictactoe_executor.py
# # FULL FIXED VERSION (Production-safe, stateless, correct contract)
# # -----------------------------------------------------------------------------

# from app.platform.module_executor import ModuleExecutor
# from app.platform.module_result import ModuleResult
# import random

# from typing import Optional
# from dataclasses import dataclass
# import logging

# logger = logging.getLogger(__name__)


# # -----------------------------------------------------------------------------
# # GAME STATE
# # -----------------------------------------------------------------------------
# @dataclass
# class TicTacToeState:
#     board: list
#     status: str
#     ai_move: Optional[int] = None
#     message: Optional[str] = None


# # -----------------------------------------------------------------------------
# # GAME SERVICE
# # -----------------------------------------------------------------------------
# class TicTacToeService:

#     WINNING_COMBINATIONS = [
#         [0,1,2],[3,4,5],[6,7,8],
#         [0,3,6],[1,4,7],[2,5,8],
#         [0,4,8],[2,4,6],
#     ]

#     @staticmethod
#     def normalize(board):
#         return [cell if cell in ['X', 'O'] else '' for cell in board]

#     @staticmethod
#     def check_winner(board, player):
#         return any(all(board[i] == player for i in combo)
#                    for combo in TicTacToeService.WINNING_COMBINATIONS)

#     @staticmethod
#     def available(board):
#         return [i for i,v in enumerate(board) if v == '']

#     @staticmethod
#     def is_full(board):
#         return len(TicTacToeService.available(board)) == 0

#     @staticmethod
#     def ai_move(board):
#         available = TicTacToeService.available(board)
#         if not available:
#             return None
#         return available[0]  # simple AI (stable, predictable)


# # -----------------------------------------------------------------------------
# # EXECUTOR (FIXED)
# # -----------------------------------------------------------------------------
# class TicTacToeExecutor(ModuleExecutor):
#     module_key = "TicTacToeGame"   # 🔥 MUST match DB slug/component_key

#     def execute(self, payload: dict, user) -> ModuleResult:
#         try:
#             board = payload.get("board", [""] * 9)

#             # ✅ ALWAYS NORMALIZE
#             board = TicTacToeService.normalize(board)

#             # -----------------------------
#             # PLAYER WIN CHECK
#             # -----------------------------
#             if TicTacToeService.check_winner(board, "X"):
#                 return ModuleResult(
#                     completed=True,
#                     score=100,
#                     status="player_win",
#                     data={"board": board}
#                 )

#             # -----------------------------
#             # DRAW CHECK
#             # -----------------------------
#             if TicTacToeService.is_full(board):
#                 return ModuleResult(
#                     completed=True,
#                     score=50,
#                     status="draw",
#                     data={"board": board}
#                 )

#             # -----------------------------
#             # AI MOVE
#             # -----------------------------
#             move = TicTacToeService.ai_move(board)
#             if move is not None:
#                 board[move] = "O"

#             # -----------------------------
#             # AI WIN CHECK
#             # -----------------------------
#             if TicTacToeService.check_winner(board, "O"):
#                 return ModuleResult(
#                     completed=True,
#                     score=10,
#                     status="ai_win",
#                     data={
#                         "board": board,
#                         "ai_move": move
#                     }
#                 )

#             # -----------------------------
#             # DRAW AFTER AI
#             # -----------------------------
#             if TicTacToeService.is_full(board):
#                 return ModuleResult(
#                     completed=True,
#                     score=50,
#                     status="draw",
#                     data={
#                         "board": board,
#                         "ai_move": move
#                     }
#                 )

#             # -----------------------------
#             # CONTINUE GAME
#             # -----------------------------
#             return ModuleResult(
#                 completed=False,
#                 score=0,
#                 status="ongoing",
#                 data={
#                     "board": board,
#                     "ai_move": move
#                 }
#             )

#         except Exception as e:
#             logger.exception("TicTacToe execution failed")

#             return ModuleResult(
#                 completed=False,
#                 status="error",
#                 error="EXECUTION_FAILED",
#                 message=str(e),
#                 data={"board": payload.get("board", [])}
#             )
        
#     def get_ai_move_by_difficulty(board, difficulty):

#         if difficulty == "easy":
#             available = TicTacToeService.get_available_moves(board)
#             move = random.choice(available)
#             board[move] = "O"
#             return move, board

#         elif difficulty == "medium":
#             if random.random() < 0.5:
#                 return TicTacToeService.get_ai_move(board).ai_move, board
#             else:
#                 available = TicTacToeService.get_available_moves(board)
#                 move = random.choice(available)
#                 board[move] = "O"
#                 return move, board

#         else:  # hard
#             res = TicTacToeService.get_ai_move(board)
#             return res.ai_move, res.board