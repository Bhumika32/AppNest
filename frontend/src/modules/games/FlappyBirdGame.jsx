import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';

const GRAVITY = 0.6;
const JUMP_STRENGTH = -8;
const OBSTACLE_WIDTH = 40;
const OBSTACLE_GAP = 150;

const FlappyBirdGame = ({ engine }) => {
    const { config, endGame, showRoast } = engine;

    const [birdY, setBirdY] = useState(200);
    const [velocity, setVelocity] = useState(0);
    const [obstacles, setObstacles] = useState([]);
    const [score, setScore] = useState(0);
    const [isGameOver, setIsGameOver] = useState(false);
    const [isPlaying, setIsPlaying] = useState(false);

    const generateObstacle = useCallback(() => {
        const minHeight = 50;
        const maxHeight = 300;
        const topHeight = Math.floor(Math.random() * (maxHeight - minHeight + 1)) + minHeight;
        return {
            x: 400, // Starts offscreen
            topHeight,
            passed: false
        };
    }, []);

    const jump = useCallback(() => {
        if (isGameOver) return;
        if (!isPlaying) {
            setIsPlaying(true);
            setObstacles([generateObstacle()]);
        }
        setVelocity(JUMP_STRENGTH);
    }, [isGameOver, isPlaying, generateObstacle]);

    useEffect(() => {
        const handleKeyPress = (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
                jump();
            }
        };
        window.addEventListener('keydown', handleKeyPress);
        return () => window.removeEventListener('keydown', handleKeyPress);
    }, [jump]);

    useEffect(() => {
        if (!isPlaying || isGameOver) return;

        let animationFrameId;

        const updateGame = () => {
            // physics
            setBirdY(prev => {
                const newY = prev + velocity;
                if (newY >= 400 || newY <= 0) {
                    return newY >= 400 ? 400 : 0; // stop falling instantly exactly
                }
                return newY;
            });
            setVelocity(prev => prev + GRAVITY);

            // obstacles update
            setObstacles(prevObstacles => {
                let newObstacles = prevObstacles.map(obs => ({ ...obs, x: obs.x - 3 })); // speed

                // spawn next
                if (newObstacles.length > 0 && newObstacles[newObstacles.length - 1].x < 200) {
                    newObstacles.push(generateObstacle());
                }

                // remove offscreen
                if (newObstacles.length > 0 && newObstacles[0].x < -OBSTACLE_WIDTH) {
                    newObstacles.shift();
                }

                // scoring check
                newObstacles = newObstacles.map(obs => {
                    if (!obs.passed && obs.x < 50) { // bird X is fixed at 50
                        setScore(s => s + 10);
                        return { ...obs, passed: true };
                    }
                    return obs;
                });

                // collision detection (Bird X: [50, 80], Y: [birdY, birdY+30])
                const birdLeft = 50;
                const birdRight = 80;

                for (let obs of newObstacles) {
                    const obsLeft = obs.x;
                    const obsRight = obs.x + OBSTACLE_WIDTH;

                    if (birdRight > obsLeft && birdLeft < obsRight) {
                        // In X collision zone
                        if (birdY < obs.topHeight || birdY + 30 > obs.topHeight + OBSTACLE_GAP) {
                            state.current.didCrash = true;
                        }
                    }
                }

                return newObstacles;
            });

            animationFrameId = requestAnimationFrame(updateGame);
        };

        animationFrameId = requestAnimationFrame(updateGame);
        return () => cancelAnimationFrame(animationFrameId);
    }, [isPlaying, isGameOver, velocity, birdY, generateObstacle, showRoast]);

    const handleGameOver = useCallback(() => {
        setIsGameOver(true);
        if (showRoast) showRoast('GAME_LOSS');
        setTimeout(() => {
            endGame({
                score: score,
                win: score > 30, // arbitrary win condition
                result: 'completed',
                metadata: { obstaclesPassed: score / 10 }
            });
        }, 2000);
    }, [endGame, score, showRoast]);

    const state = useRef({ didCrash: false, pendingRoast: false });

    useEffect(() => {
        if (!isGameOver && (birdY >= 400 || birdY <= 0 || state.current.didCrash)) {
            handleGameOver();
        }
    }, [birdY, isGameOver, handleGameOver]);

    useEffect(() => {
        if (score > 0 && score % 50 === 0 && !state.current.pendingRoast) {
            state.current.pendingRoast = true;
        } else if (score % 50 !== 0) {
            state.current.pendingRoast = false; // Reset when score moves past multiple
        }
    }, [score]);

    useEffect(() => {
        if (state.current.pendingRoast && showRoast) {
            showRoast('STREAK_ACTIVE');
            state.current.pendingRoast = false; // Prevent multiple fires
        }
    }, [score, showRoast]);

    return (
        <div className="flex flex-col items-center gap-4">
            <h2 className="text-3xl font-black text-white uppercase tracking-widest drop-shadow-lg">
                Score: <span className="text-neon-pink">{score}</span>
            </h2>

            <div
                className="relative w-[400px] h-[400px] bg-black/60 border-2 border-white/20 rounded-xl overflow-hidden cursor-pointer active:cursor-grabbing backdrop-blur-md"
                onClick={jump}
            >
                {/* Bird */}
                <motion.div
                    className="absolute w-8 h-8 bg-neon-blue rounded-full shadow-[0_0_15px_rgba(0,255,255,0.8)]"
                    style={{ left: 50, top: birdY }}
                />

                {/* Obstacles */}
                {obstacles.map((obs, i) => (
                    <React.Fragment key={i}>
                        {/* Top */}
                        <div
                            className="absolute bg-gradient-to-b from-white/10 to-neon-pink/80 border-b-2 border-neon-pink"
                            style={{ left: obs.x, top: 0, width: OBSTACLE_WIDTH, height: obs.topHeight }}
                        />
                        {/* Bottom */}
                        <div
                            className="absolute bg-gradient-to-t from-white/10 to-neon-pink/80 border-t-2 border-neon-pink"
                            style={{ left: obs.x, top: obs.topHeight + OBSTACLE_GAP, width: OBSTACLE_WIDTH, height: 400 - (obs.topHeight + OBSTACLE_GAP) }}
                        />
                    </React.Fragment>
                ))}

                {!isPlaying && !isGameOver && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm">
                        <span className="text-white font-black uppercase tracking-widest animate-pulse">Click or Space to Start</span>
                    </div>
                )}

                {isGameOver && (
                    <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/80 backdrop-blur-md">
                        <span className="text-4xl font-black text-red-500 uppercase tracking-widest mb-2 shadow-red-500 drop-shadow-lg">Crashed</span>
                        <span className="text-gray-300 font-bold tracking-widest">Score: {score}</span>
                    </div>
                )}
            </div>
        </div>
    );
};

export default FlappyBirdGame;
