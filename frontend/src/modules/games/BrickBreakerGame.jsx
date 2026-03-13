import React, { useRef, useEffect, useState, useCallback } from 'react';

const BrickBreakerGame = ({ engine }) => {
    const { config, endGame, showRoast } = engine;
    const canvasRef = useRef(null);
    const [score, setScore] = useState(0);
    const [lives, setLives] = useState(3);
    const [isPlaying, setIsPlaying] = useState(false);
    const [isGameOver, setIsGameOver] = useState(false);

    // Initial Engine variables
    const state = useRef({
        ball: { x: 200, y: 350, dx: 4, dy: -4, radius: 8 },
        paddle: { x: 150, width: 100, height: 10, y: 380 },
        bricks: [],
        rightPressed: false,
        leftPressed: false
    });

    const initBricks = useCallback(() => {
        const brickRowCount = 5;
        const brickColumnCount = 7;
        const brickWidth = 45;
        const brickHeight = 15;
        const brickPadding = 10;
        const brickOffsetTop = 30;
        const brickOffsetLeft = 15;

        const bricks = [];
        for (let c = 0; c < brickColumnCount; c++) {
            for (let r = 0; r < brickRowCount; r++) {
                bricks.push({
                    x: (c * (brickWidth + brickPadding)) + brickOffsetLeft,
                    y: (r * (brickHeight + brickPadding)) + brickOffsetTop,
                    status: 1,
                    w: brickWidth,
                    h: brickHeight
                });
            }
        }
        state.current.bricks = bricks;
    }, []);

    useEffect(() => {
        initBricks();

        const handleKeyDown = (e) => {
            if (e.key === "Right" || e.key === "ArrowRight") state.current.rightPressed = true;
            else if (e.key === "Left" || e.key === "ArrowLeft") state.current.leftPressed = true;
        };

        const handleKeyUp = (e) => {
            if (e.key === "Right" || e.key === "ArrowRight") state.current.rightPressed = false;
            else if (e.key === "Left" || e.key === "ArrowLeft") state.current.leftPressed = false;
        };

        const handleMouseMove = (e) => {
            const canvas = canvasRef.current;
            if (!canvas) return;
            const relativeX = e.clientX - canvas.getBoundingClientRect().left;
            if (relativeX > 0 && relativeX < canvas.width) {
                state.current.paddle.x = relativeX - state.current.paddle.width / 2;
            }
        };

        document.addEventListener("keydown", handleKeyDown);
        document.addEventListener("keyup", handleKeyUp);
        document.addEventListener("mousemove", handleMouseMove);

        return () => {
            document.removeEventListener("keydown", handleKeyDown);
            document.removeEventListener("keyup", handleKeyUp);
            document.removeEventListener("mousemove", handleMouseMove);
        };
    }, [initBricks]); // Only runs once because initBricks is stable via useCallback

    useEffect(() => {
        if (!isPlaying || isGameOver) return;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        let animationFrameId;

        const drawBall = () => {
            ctx.beginPath();
            ctx.arc(state.current.ball.x, state.current.ball.y, state.current.ball.radius, 0, Math.PI * 2);
            ctx.fillStyle = "#00FFFF";
            ctx.shadowColor = "#00FFFF";
            ctx.shadowBlur = 15;
            ctx.fill();
            ctx.closePath();
            ctx.shadowBlur = 0; // reset
        };

        const drawPaddle = () => {
            ctx.beginPath();
            ctx.rect(state.current.paddle.x, state.current.paddle.y, state.current.paddle.width, state.current.paddle.height);
            ctx.fillStyle = "#FF0080";
            ctx.shadowColor = "#FF0080";
            ctx.shadowBlur = 10;
            ctx.fill();
            ctx.closePath();
            ctx.shadowBlur = 0;
        };

        const drawBricks = () => {
            state.current.bricks.forEach(b => {
                if (b.status === 1) {
                    ctx.beginPath();
                    ctx.rect(b.x, b.y, b.w, b.h);
                    ctx.fillStyle = "#FFFFFF";
                    ctx.fill();
                    ctx.closePath();
                }
            });
        };

        const collisionDetection = () => {
            let activeBricks = 0;
            state.current.bricks.forEach(b => {
                if (b.status === 1) {
                    if (state.current.ball.x > b.x && state.current.ball.x < b.x + b.w && state.current.ball.y > b.y && state.current.ball.y < b.y + b.h) {
                        state.current.ball.dy = -state.current.ball.dy;
                        b.status = 0;
                        setScore(s => s + 10);
                        if (!state.current.pendingRoast && showRoast) {
                            state.current.pendingRoast = true;
                        }
                    } else {
                        activeBricks++;
                    }
                }
            });

            if (activeBricks === 0) {
                // Next level / reset bricks
                initBricks();
                state.current.ball.dy *= 1.2; // faster
                state.current.ball.dx *= 1.2;
                state.current.ball.x = canvas.width / 2;
                state.current.ball.y = canvas.height - 30;
                setLives(l => l + 1); // bonus life
            }
        };

        const draw = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawBricks();
            drawBall();
            drawPaddle();
            collisionDetection();

            // Wall collisions (X)
            if (state.current.ball.x + state.current.ball.dx > canvas.width - state.current.ball.radius || state.current.ball.x + state.current.ball.dx < state.current.ball.radius) {
                state.current.ball.dx = -state.current.ball.dx;
            }

            // Wall collisions (Y)
            if (state.current.ball.y + state.current.ball.dy < state.current.ball.radius) {
                state.current.ball.dy = -state.current.ball.dy; // ceiling bounce
            } else if (state.current.ball.y + state.current.ball.dy > canvas.height - state.current.ball.radius) {
                // hit ground
                setLives(l => {
                    if (l - 1 <= 0) {
                        setIsGameOver(true);
                        if (showRoast) showRoast('GAME_LOSS');
                        setTimeout(() => endGame({ score, win: false, result: 'completed' }), 2000);
                        return 0;
                    } else {
                        state.current.ball.x = canvas.width / 2;
                        state.current.ball.y = canvas.height - 30;
                        state.current.ball.dy = -4; // reset speed lightly
                        state.current.ball.dx = 4;
                        state.current.paddle.x = (canvas.width - state.current.paddle.width) / 2;
                        return l - 1;
                    }
                });
            } else if (
                state.current.ball.y + state.current.ball.dy > state.current.paddle.y - state.current.ball.radius &&
                state.current.ball.y < state.current.paddle.y && // ensure coming from top
                state.current.ball.x > state.current.paddle.x && state.current.ball.x < state.current.paddle.x + state.current.paddle.width
            ) {
                // Paddle bounce and angle shift based on where it hit
                let hitPoint = state.current.ball.x - (state.current.paddle.x + state.current.paddle.width / 2);
                state.current.ball.dx = hitPoint * 0.15;
                state.current.ball.dy = -state.current.ball.dy;
            }

            // Paddle move
            if (state.current.rightPressed && state.current.paddle.x < canvas.width - state.current.paddle.width) {
                state.current.paddle.x += 7;
            } else if (state.current.leftPressed && state.current.paddle.x > 0) {
                state.current.paddle.x -= 7;
            }

            state.current.ball.x += state.current.ball.dx;
            state.current.ball.y += state.current.ball.dy;

            animationFrameId = requestAnimationFrame(draw);
        };

        draw();

        return () => cancelAnimationFrame(animationFrameId);
    }, [isPlaying, isGameOver, score, endGame, showRoast, initBricks]);

    useEffect(() => {
        if (state.current.pendingRoast && score > 0 && score % 100 === 0 && showRoast) {
            showRoast('STREAK_ACTIVE');
            state.current.pendingRoast = false;
        }
    }, [score, showRoast]);

    const startGame = () => {
        setIsPlaying(true);
    };

    return (
        <div className="flex flex-col items-center gap-4">
            <div className="flex justify-between w-[400px] text-white font-black uppercase tracking-widest px-2">
                <span>Score: <span className="text-neon-pink">{score}</span></span>
                <span>Lives: <span className="text-neon-blue">{lives}</span></span>
            </div>

            <div className="relative">
                <canvas
                    ref={canvasRef}
                    width={400}
                    height={400}
                    className="bg-black/60 border border-white/20 rounded-xl shadow-2xl backdrop-blur-md block"
                />

                {!isPlaying && !isGameOver && (
                    <div
                        className="absolute inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm cursor-pointer"
                        onClick={startGame}
                    >
                        <span className="text-white font-black uppercase tracking-widest animate-pulse px-6 py-3 border border-white/20 rounded-xl hover:bg-white/10 transition-colors">Click to Start Process</span>
                    </div>
                )}

                {isGameOver && (
                    <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/80 backdrop-blur-md text-white">
                        <span className="text-4xl font-black text-red-500 uppercase tracking-widest mb-2 shadow-red-500 drop-shadow-lg">Game Over</span>
                        <span className="text-gray-300 font-bold tracking-widest">Final Code Output: {score}</span>
                    </div>
                )}
            </div>

            <span className="text-xs text-gray-600 font-bold uppercase tracking-widest mt-2">[Left/Right Arrows] to Move Paddle</span>
        </div>
    );
};

export default BrickBreakerGame;
