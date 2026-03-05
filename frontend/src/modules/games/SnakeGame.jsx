import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';

const GRID_SIZE = 20;
const INITIAL_SPEED = 150;

const SnakeGame = ({ engine }) => {
    const { config, endGame, showRoast } = engine;
    const difficultyLevel = config?.difficulty || 'EASY';

    const getDifficultySpeed = () => {
        switch (difficultyLevel) {
            case 'MEDIUM': return 100;
            case 'HARD': return 60;
            case 'EASY':
            default: return 150;
        }
    };

    const [snake, setSnake] = useState([{ x: 10, y: 10 }]);
    const [direction, setDirection] = useState({ x: 0, y: -1 });
    const [isGameOver, setIsGameOver] = useState(false);
    const [score, setScore] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);

    const generateFood = useCallback((currentSnake) => {
        let newFood;
        while (true) {
            newFood = {
                x: Math.floor(Math.random() * GRID_SIZE),
                y: Math.floor(Math.random() * GRID_SIZE)
            };
            const collision = currentSnake.some(segment => segment.x === newFood.x && segment.y === newFood.y);
            if (!collision) break;
        }
        return newFood;
    }, []);

    const [food, setFood] = useState(() => generateFood([{ x: 10, y: 10 }]));

    const isPlayingRef = React.useRef(false);

    useEffect(() => {
        const handleKeyPress = (e) => {
            if (!isPlayingRef.current) {
                isPlayingRef.current = true;
                setIsPlaying(true);
            }

            switch (e.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    setDirection(prev => prev.y !== 1 ? { x: 0, y: -1 } : prev);
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    setDirection(prev => prev.y !== -1 ? { x: 0, y: 1 } : prev);
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    setDirection(prev => prev.x !== 1 ? { x: -1, y: 0 } : prev);
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    setDirection(prev => prev.x !== -1 ? { x: 1, y: 0 } : prev);
                    break;
                default:
                    break;
            }
        };

        window.addEventListener('keydown', handleKeyPress);
        return () => window.removeEventListener('keydown', handleKeyPress);
    }, []); // Runs once

    useEffect(() => {
        if (!isPlaying || isGameOver) return;

        const moveSnake = () => {
            setSnake((prevSnake) => {
                const head = prevSnake[0];
                const newHead = { x: head.x + direction.x, y: head.y + direction.y };

                // Collision with walls
                if (newHead.x < 0 || newHead.x >= GRID_SIZE || newHead.y < 0 || newHead.y >= GRID_SIZE) {
                    handleGameOver();
                    return prevSnake;
                }

                // Collision with self
                if (prevSnake.some(segment => segment.x === newHead.x && segment.y === newHead.y)) {
                    handleGameOver();
                    return prevSnake;
                }

                const newSnake = [newHead, ...prevSnake];

                // Ate food
                if (newHead.x === food.x && newHead.y === food.y) {
                    setScore(s => s + 10);
                    setFood(generateFood(newSnake));
                    if (score > 0 && score % 50 === 0 && showRoast) {
                        showRoast('STREAK_ACTIVE');
                    }
                } else {
                    newSnake.pop(); // Remove tail if no food eaten
                }

                return newSnake;
            });
        };

        const interval = setInterval(moveSnake, getDifficultySpeed());
        return () => clearInterval(interval);
    }, [isPlaying, isGameOver, direction, food, score, showRoast, generateFood]);

    const handleGameOver = () => {
        setIsGameOver(true);
        if (showRoast) showRoast('GAME_LOSS');
        setTimeout(() => {
            endGame({
                score: score,
                win: score > 50,
                result: 'completed',
                metadata: { snakeLength: snake.length }
            });
        }, 2000);
    };

    return (
        <div className="flex flex-col items-center gap-6">
            <div className="flex justify-between w-full max-w-md px-4 mt-8">
                <div className="text-xl font-black text-white uppercase tracking-widest">
                    Score: <span className="text-neon-pink">{score}</span>
                </div>
                <div className="text-xl font-black text-gray-500 uppercase tracking-widest">
                    Len: <span className="text-neon-blue">{snake.length}</span>
                </div>
            </div>

            <div
                className="bg-black/80 border-2 border-white/10 rounded-lg overflow-hidden relative"
                style={{
                    width: '300px',
                    height: '300px',
                    display: 'grid',
                    gridTemplateColumns: `repeat(${GRID_SIZE}, 1fr)`,
                    gridTemplateRows: `repeat(${GRID_SIZE}, 1fr)`,
                }}
            >
                {!isPlaying && !isGameOver && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-10">
                        <span className="text-white font-black uppercase tracking-widest animate-pulse">Press any WASD key to start</span>
                    </div>
                )}
                {isGameOver && (
                    <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/80 backdrop-blur-sm z-10 text-white">
                        <span className="text-3xl font-black text-red-500 uppercase tracking-widest mb-2">System Failure</span>
                        <span className="text-gray-400">Final Score: {score}</span>
                    </div>
                )}

                {/* Render Snake */}
                {snake.map((segment, index) => (
                    <motion.div
                        key={`${index}-${segment.x}-${segment.y}`}
                        className={`w-full h-full border border-black/20 ${index === 0 ? 'bg-neon-pink rounded-sm shadow-[0_0_10px_rgba(255,0,128,0.8)] z-10' : 'bg-neon-blue/80'}`}
                        style={{
                            gridColumnStart: segment.x + 1,
                            gridRowStart: segment.y + 1,
                        }}
                        initial={index === 0 ? { scale: 0.8 } : false}
                        animate={{ scale: 1 }}
                    />
                ))}

                {/* Render Food */}
                <motion.div
                    className="w-full h-full bg-neon-green rounded-full shadow-[0_0_15px_rgba(0,255,0,0.8)]"
                    style={{
                        gridColumnStart: food.x + 1,
                        gridRowStart: food.y + 1,
                    }}
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ repeat: Infinity, duration: 1 }}
                />
            </div>

            <div className="text-xs font-bold text-gray-600 uppercase tracking-widest mt-4 flex gap-4">
                <span>[W] Up</span>
                <span>[A] Left</span>
                <span>[S] Down</span>
                <span>[D] Right</span>
            </div>
        </div>
    );
};

export default SnakeGame;
