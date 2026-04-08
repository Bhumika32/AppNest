// -----------------------------------------------------------------------------
// File: frontend/src/modules/games/TicTacToeGame.jsx
//
// FINAL CORRECT VERSION
// - Backend controls ALL game logic (X/O)
// - No optimistic UI corruption
// - Proper payload (board + move)
// - Clean structure (no duplicate functions)
// -----------------------------------------------------------------------------

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import apiClient from '@/api/apiClient';
import { useAuthStore } from '@/store/authStore';

const TicTacToeGame = ({ engine }) => {
    const { config, endGame, completedRef } = engine;

    const mode = config?.mode || 'solo';
    const difficulty = config?.difficulty || 'medium';

    const [board, setBoard] = useState(Array(9).fill(""));
    const [winner, setWinner] = useState(null);
    const [loading, setLoading] = useState(false);

    // -----------------------------
    // CALL BACKEND
    // -----------------------------
    const playMove = async (moveIndex) => {
        try {
            setLoading(true);

            // 🚨 AUTH GUARD
            const token = useAuthStore.getState().token;
            if (!token || token.split('.').length !== 3) {
                console.warn("⛔ Invalid token, blocking request");
                return;
            }

            const { data: result } = await apiClient.post(
                '/modules/execute/tic-tac-toe',
                {
                    board,          // 🔥 send current board
                    move: moveIndex, // 🔥 send move index
                    mode,
                    difficulty
                }
            );

            if (!result || result.error) {
                console.error("Invalid response:", result);
                return;
            }

            const boardFromServer =
                result?.data?.board ??
                result?.data?.data?.board;

            if (!Array.isArray(boardFromServer)) {
                console.error("Invalid board structure:", result);
                return;
            }

            // ✅ update board ONLY from backend
            setBoard(boardFromServer);

            // ✅ handle game end
            if (result.completed) {
                setWinner(result.status);

                setTimeout(() => {
                    if (completedRef?.current) return;

                    endGame({
                        score: result.score,
                        win: result.status === "player_win" || result.status === "X_win",
                        result: result.status,
                        metadata: { mode, difficulty }
                    });
                }, 800);
            }

        } catch (err) {
            console.error("Execution failed:", err);
        } finally {
            setLoading(false);
        }
    };

    // -----------------------------
    // HANDLE CLICK
    // -----------------------------
    const handleClick = (i) => {
        if (loading || winner || board[i]) return;

        // ❗ DO NOT modify board here
        // backend decides X or O
        playMove(i);
    };

    // -----------------------------
    // UI
    // -----------------------------
    return (
        <div className="flex flex-col items-center justify-center p-4">

            <h2 className="text-xl text-white mb-4 uppercase tracking-widest">
                {winner
                    ? winner === "draw"
                        ? "DRAW"
                        : winner.includes("win")
                        ? `${winner.replace("_", " ").toUpperCase()}`
                        : "GAME OVER"
                    : loading
                        ? "PROCESSING..."
                        : "YOUR TURN"}
            </h2>

            <div className="grid grid-cols-3 gap-3 p-4 bg-white/5 rounded-2xl">
                {board.map((cell, i) => (
                    <motion.button
                        key={i}
                        whileTap={{ scale: 0.9 }}
                        onClick={() => handleClick(i)}
                        className="w-20 h-20 text-4xl font-bold bg-white/10 rounded-xl"
                        disabled={loading || winner}
                    >
                        {cell}
                    </motion.button>
                ))}
            </div>

            <p className="mt-4 text-sm text-gray-400 uppercase">
                Mode: {mode} | Difficulty: {difficulty}
            </p>

        </div>
    );
};

export default TicTacToeGame;

// import React, { useState } from 'react';
// import { motion } from 'framer-motion';

// const TicTacToeGame = ({ engine }) => {
//     const { config, endGame } = engine;

//     const mode = config?.mode || 'ai';
//     const difficulty = config?.difficulty || 'medium';

//     const [board, setBoard] = useState(Array(9).fill(""));
//     const [winner, setWinner] = useState(null);
//     const [loading, setLoading] = useState(false);

//     // -----------------------------
//     // CALL BACKEND
//     // -----------------------------
//     const playMove = async (newBoard) => {
//         try {
//             setLoading(true);

//             const res = await fetch("/api/modules/execute/tic-tac-toe", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json"
//                 },
//                 body: JSON.stringify({
//                     board: newBoard,
//                     mode,
//                     difficulty
//                 })
//             });

//             const result = await res.json();

//             if (!result || result.error) {
//                 console.error(result?.error);
//                 return;
//             }

//             const data = result.data;

//             setBoard(data.board);

//             if (result.completed) {
//                 setWinner(result.status);

//                 setTimeout(() => {
//                     if (engine.completedRef?.current) return;

//                     endGame({
//                         score: result.score,
//                         win: result.status === "player_win",
//                         metadata: { mode, difficulty }
//                     });
//                 }, 1200);
//             }

//         } catch (err) {
//             console.error("Execution failed:", err);
//         } finally {
//             setLoading(false);
//         }
//     };

//     // -----------------------------
//     // HANDLE CLICK
//     // -----------------------------
//     const handleClick = (i) => {
//         if (board[i] || winner || loading) return;

//         const newBoard = [...board];
//         newBoard[i] = "X";

//         setBoard(newBoard);

//         // Call backend for AI move + validation
//         playMove(newBoard);
//     };

//     // -----------------------------
//     // UI
//     // -----------------------------
//     return (
//         <div className="flex flex-col items-center justify-center p-4">

//             <h2 className="text-xl text-white mb-4 uppercase tracking-widest">
//                 {winner
//                     ? winner === "draw"
//                         ? "DRAW"
//                         : winner === "player_win"
//                         ? "YOU WIN"
//                         : "AI WINS"
//                     : "YOUR TURN"}
//             </h2>

//             <div className="grid grid-cols-3 gap-3 p-4 bg-white/5 rounded-2xl">

//                 {board.map((cell, i) => (
//                     <motion.button
//                         key={i}
//                         whileTap={{ scale: 0.9 }}
//                         onClick={() => handleClick(i)}
//                         className="w-20 h-20 text-4xl font-bold bg-white/10 rounded-xl"
//                         disabled={loading}
//                     >
//                         {cell}
//                     </motion.button>
//                 ))}

//             </div>

//             <p className="mt-4 text-sm text-gray-400 uppercase">
//                 Mode: {mode} | Difficulty: {difficulty}
//             </p>

//         </div>
//     );
// };

// export default TicTacToeGame;

