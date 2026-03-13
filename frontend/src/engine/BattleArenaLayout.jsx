import React from 'react';
import { motion } from 'framer-motion';

const BattleArenaLayout = ({ children, module, config }) => {
    return (
        <div className="relative w-full h-[calc(100vh-5rem)] overflow-hidden bg-black flex flex-col">
            {/* Animated Aura Background */}
            <div className="absolute inset-0 z-0 opacity-20 pointer-events-none">
                <motion.div
                    animate={{
                        rotate: [0, 360],
                        scale: [1, 1.1, 1]
                    }}
                    transition={{
                        duration: 20,
                        repeat: Infinity,
                        ease: "linear"
                    }}
                    className="absolute -top-[50%] -left-[20%] w-[150%] h-[150%] bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-neon-blue/40 via-transparent to-transparent opacity-50 blur-[100px]"
                />
                <motion.div
                    animate={{
                        rotate: [360, 0],
                        scale: [1, 1.2, 1]
                    }}
                    transition={{
                        duration: 25,
                        repeat: Infinity,
                        ease: "linear"
                    }}
                    className="absolute -top-[20%] -right-[20%] w-[120%] h-[120%] bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-neon-pink/30 via-transparent to-transparent opacity-40 blur-[100px]"
                />
            </div>

            {/* Battle Header */}
            <div className="relative z-10 w-full p-4 flex justify-between items-center border-b border-white/5 bg-gradient-to-b from-black/80 to-transparent">
                <div className="flex items-center gap-4">
                    <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-neon-blue to-white uppercase tracking-tighter drop-shadow-[0_0_10px_rgba(0,255,255,0.3)]">
                        {module.name}
                    </h1>
                    {config?.difficulty && (
                        <span className="px-2 py-0.5 text-[10px] font-black uppercase tracking-widest text-neon-pink border border-neon-pink/30 rounded bg-neon-pink/10">
                            {config.difficulty}
                        </span>
                    )}
                    {config?.mode && (
                        <span className="px-2 py-0.5 text-[10px] font-black uppercase tracking-widest text-neon-blue border border-neon-blue/30 rounded bg-neon-blue/10">
                            {config.mode}
                        </span>
                    )}
                </div>
            </div>

            {/* Main Stage */}
            <div className="relative z-10 flex-1 w-full flex items-center justify-center p-4">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    transition={{ type: "spring", stiffness: 200, damping: 20 }}
                    className="w-full max-w-5xl max-h-full flex items-center justify-center"
                >
                    {children}
                </motion.div>
            </div>
        </div>
    );
};

export default BattleArenaLayout;
