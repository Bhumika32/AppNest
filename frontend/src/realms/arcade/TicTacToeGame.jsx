import React from 'react';
import GameLayout from '../../layout/Module/GameLayout.jsx';
import { motion } from 'framer-motion';

const TicTacToeGame = ({ module }) => {
    const [board, setBoard] = React.useState(Array(9).fill(null));
    const [isXNext, setIsXNext] = React.useState(true);
    const [isAiMode, setIsAiMode] = React.useState(true);
    const [winner, setWinner] = React.useState(null);

    const calculateWinner = (squares) => {
        const lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ];
        for (let i = 0; i < lines.length; i++) {
            const [a, b, c] = lines[i];
            if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
                return squares[a];
            }
        }
        return squares.includes(null) ? null : 'Draw';
    };

    const handleClick = (i) => {
        if (winner || board[i]) return;
        const newBoard = [...board];
        newBoard[i] = isXNext ? 'X' : 'O';
        setBoard(newBoard);
        setIsXNext(!isXNext);

        const win = calculateWinner(newBoard);
        if (win) {
            setWinner(win);
        } else if (isAiMode && isXNext) {
            // Trigger AI move
            setTimeout(() => makeAiMove(newBoard), 500);
        }
    };

    const makeAiMove = (currentBoard) => {
        const available = currentBoard.map((v, i) => v === null ? i : null).filter(v => v !== null);
        if (available.length === 0) return;
        const randomMove = available[Math.floor(Math.random() * available.length)];
        const newBoard = [...currentBoard];
        newBoard[randomMove] = 'O';
        setBoard(newBoard);
        setIsXNext(true);
        const win = calculateWinner(newBoard);
        if (win) setWinner(win);
    };

    const reset = () => {
        setBoard(Array(9).fill(null));
        setIsXNext(true);
        setWinner(null);
    };

    return (
        <GameLayout module={module} onReset={reset} score={winner === 'X' ? 'WIN' : winner === 'O' ? 'LOSS' : winner === 'Draw' ? 'DRAW' : null}>
            <div className="flex flex-col items-center justify-center gap-8 h-full">
                <div className="flex gap-4">
                    <button
                        onClick={() => { setIsAiMode(true); reset(); }}
                        className={`px-6 py-2 rounded-xl border font-black uppercase text-xs transition-all ${isAiMode ? 'bg-neon-blue border-neon-blue text-black' : 'bg-white/5 border-white/10 text-gray-400'}`}
                    >
                        VERSUS AI
                    </button>
                    <button
                        onClick={() => { setIsAiMode(false); reset(); }}
                        className={`px-6 py-2 rounded-xl border font-black uppercase text-xs transition-all ${!isAiMode ? 'bg-neon-pink border-neon-pink text-black' : 'bg-white/5 border-white/10 text-gray-400'}`}
                    >
                        PLAYER VS PLAYER
                    </button>
                </div>

                <div className="grid grid-cols-3 gap-3">
                    {board.map((val, i) => (
                        <motion.button
                            key={i}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => handleClick(i)}
                            className={`w-24 h-24 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-4xl font-black transition-all ${val === 'X' ? 'text-neon-blue' : 'text-neon-pink'} ${!val && !winner ? 'hover:bg-white/10 cursor-alias' : ''}`}
                        >
                            {val && (
                                <motion.span initial={{ scale: 0, rotate: -45 }} animate={{ scale: 1, rotate: 0 }}>
                                    {val}
                                </motion.span>
                            )}
                        </motion.button>
                    ))}
                </div>

                <div className="text-center">
                    {!winner ? (
                        <div className="text-[10px] font-black uppercase tracking-[0.4em] text-gray-500">
                            Neural Turn: <span className={isXNext ? 'text-neon-blue' : 'text-neon-pink'}>{isXNext ? 'AGENT (X)' : isAiMode ? 'CORE AI (O)' : 'OPPONENT (O)'}</span>
                        </div>
                    ) : (
                        <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="text-2xl font-black uppercase tracking-widest text-white">
                            {winner === 'Draw' ? 'STALEMATE DETECTED' : `${winner === 'X' ? 'AGENT' : 'CORE AI'} DOMINANCE`}
                        </motion.div>
                    )}
                </div>
            </div>
        </GameLayout>
    );
};

export default TicTacToeGame;
