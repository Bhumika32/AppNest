import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const TicTacToeGame = ({ engine }) => {
    const { config, endGame } = engine;
    const { mode = 'SOLO', difficulty = 'EASY' } = config || {};

    const [board, setBoard] = useState(Array(9).fill(null));
    const [xIsNext, setXIsNext] = useState(true);
    const [winner, setWinner] = useState(null);
    const [winningLine, setWinningLine] = useState(null);

    const checkWinner = (squares) => {
        const lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6],
        ];
        for (let i = 0; i < lines.length; i++) {
            const [a, b, c] = lines[i];
            if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
                return { player: squares[a], line: lines[i] };
            }
        }
        return null;
    };

    const getAIMove = (squares) => {
        const emptyIndices = squares.map((val, idx) => val === null ? idx : null).filter(val => val !== null);
        if (emptyIndices.length === 0) return -1;

        if (difficulty === 'EASY') {
            return emptyIndices[Math.floor(Math.random() * emptyIndices.length)];
        }

        // MEDIUM: Block winning move or random
        if (difficulty === 'MEDIUM') {
            for (let i of emptyIndices) {
                const tempBoard = [...squares];
                tempBoard[i] = 'O';
                if (checkWinner(tempBoard)) return i;
            }
            for (let i of emptyIndices) {
                const tempBoard = [...squares];
                tempBoard[i] = 'X';
                if (checkWinner(tempBoard)) return i;
            }
            return emptyIndices[Math.floor(Math.random() * emptyIndices.length)];
        }

        // HARD: Simple approach (block + win + center + corners)
        if (difficulty === 'HARD') {
            // Can AI win?
            for (let i of emptyIndices) {
                const tempBoard = [...squares];
                tempBoard[i] = 'O';
                if (checkWinner(tempBoard)) return i;
            }
            // Can Player win? (Block)
            for (let i of emptyIndices) {
                const tempBoard = [...squares];
                tempBoard[i] = 'X';
                if (checkWinner(tempBoard)) return i;
            }
            // Take center
            if (squares[4] === null) return 4;
            // Take corner
            const corners = [0, 2, 6, 8].filter(i => squares[i] === null);
            if (corners.length > 0) return corners[Math.floor(Math.random() * corners.length)];
            // Take side
            return emptyIndices[Math.floor(Math.random() * emptyIndices.length)];
        }

        return emptyIndices[0];
    };

    useEffect(() => {
        if (!xIsNext && mode === 'VS_AI' && !winner && board.includes(null)) {
            const timer = setTimeout(() => {
                const aiMove = getAIMove(board);
                if (aiMove !== -1) {
                    handleClick(aiMove);
                }
            }, 600);
            return () => clearTimeout(timer);
        }
    }, [xIsNext, mode, winner, board]);

    const handleClick = (i) => {
        if (board[i] || winner) return;

        const newBoard = [...board];
        newBoard[i] = xIsNext ? 'X' : 'O';
        setBoard(newBoard);

        const winResult = checkWinner(newBoard);
        if (winResult) {
            setWinner(winResult.player);
            setWinningLine(winResult.line);
            setTimeout(() => {
                if (engine.completedRef?.current) return;
                const isPlayerWin = winResult.player === 'X' || mode === 'PVP';
                endGame({
                    score: isPlayerWin ? 100 : 10,
                    win: isPlayerWin,
                    metadata: { turns: newBoard.filter(Boolean).length }
                });
            }, 1500);
        } else if (!newBoard.includes(null)) {
            setWinner('DRAW');
            setTimeout(() => {
                if (engine.completedRef?.current) return;
                endGame({ score: 50, win: false, result: 'draw', metadata: { 9: 9 } });
            }, 1500);
        } else {
            setXIsNext(!xIsNext);
            if (mode === 'VS_AI' && xIsNext && engine.showRoast && Math.random() > 0.6) {
                engine.showRoast('GAME_LOSS'); // Roast during game
            }
        }
    };

    return (
        <div className="flex flex-col items-center justify-center p-4">
            <div className="mb-8 text-center">
                <h2 className="text-2xl font-black uppercase text-white mb-2 tracking-widest">
                    {winner === 'DRAW' ? 'STALEMATE' : winner ? `PLAYER ${winner} WINS` : `PLAYER ${xIsNext ? 'X' : 'O'}'S TURN`}
                </h2>
                {mode === 'VS_AI' && (
                    <p className="text-sm font-bold text-neon-pink uppercase tracking-widest">
                        AI LEVEL: {difficulty}
                    </p>
                )}
            </div>

            <div className="grid grid-cols-3 gap-2 sm:gap-4 p-4 sm:p-6 bg-white/5 border border-white/10 rounded-3xl backdrop-blur-sm shadow-2xl relative">
                {board.map((square, i) => {
                    const isWinningSquare = winningLine?.includes(i);
                    return (
                        <motion.button
                            key={i}
                            whileHover={{ scale: square || winner ? 1 : 1.05 }}
                            whileTap={{ scale: square || winner ? 1 : 0.95 }}
                            onClick={() => handleClick(i)}
                            className={`w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center text-5xl sm:text-6xl font-black rounded-2xl transition-all duration-300
                                ${square ? 'bg-white/10' : 'bg-white/5 hover:bg-white/10'} 
                                ${isWinningSquare ? 'bg-neon-pink/20 border border-neon-pink shadow-[0_0_20px_rgba(255,0,128,0.4)]' : 'border border-white/5'}
                                ${square === 'X' ? 'text-neon-blue drop-shadow-[0_0_10px_rgba(0,255,255,0.8)]' : square === 'O' ? 'text-neon-pink drop-shadow-[0_0_10px_rgba(255,0,128,0.8)]' : ''}
                            `}
                            disabled={square !== null || winner !== null || (!xIsNext && mode === 'VS_AI')}
                        >
                            {square && (
                                <motion.span
                                    initial={{ scale: 0, rotate: -180 }}
                                    animate={{ scale: 1, rotate: 0 }}
                                    type="spring"
                                >
                                    {square}
                                </motion.span>
                            )}
                        </motion.button>
                    );
                })}
            </div>
        </div>
    );
};

export default TicTacToeGame;
