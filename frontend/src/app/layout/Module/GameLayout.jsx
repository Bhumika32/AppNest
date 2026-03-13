import React from 'react';
import { motion } from 'framer-motion';
import { ChevronLeft, Trophy, RotateCcw } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const GameLayout = ({ children, module, score = null, onReset = null }) => {
    const navigate = useNavigate();

    return (
        <div className="min-h-[80vh] flex flex-col gap-6 max-w-6xl mx-auto">
            {/* Game Header */}
            <div className="flex items-center justify-between bg-dark-surface/30 border border-white/5 p-4 rounded-2xl backdrop-blur-md">
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => navigate(-1)}
                        className="p-2 hover:bg-white/5 rounded-xl transition-all text-gray-400 hover:text-white"
                    >
                        <ChevronLeft size={24} />
                    </button>
                    <div>
                        <h3 className="text-xl font-black uppercase tracking-tighter flex items-center gap-2">
                            <span className="text-2xl">{module.icon}</span>
                            {module.name}
                        </h3>
                        <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">{module.difficulty} | ANALYTICS ACTIVE</p>
                    </div>
                </div>

                <div className="flex items-center gap-6">
                    {score !== null && (
                        <div className="flex items-center gap-3 px-4 py-2 bg-neon-blue/10 border border-neon-blue/20 rounded-xl">
                            <Trophy size={18} className="text-neon-blue" />
                            <span className="text-lg font-black text-white">{score}</span>
                        </div>
                    )}
                    {onReset && (
                        <button
                            onClick={onReset}
                            className="p-3 hover:bg-white/5 rounded-xl transition-all text-gray-400 hover:text-neon-pink group"
                        >
                            <RotateCcw size={20} className="group-hover:rotate-180 transition-transform duration-500" />
                        </button>
                    )}
                </div>
            </div>

            {/* Main Game Area */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex-1 bg-dark-bg/40 border border-white/5 rounded-3xl p-8 relative overflow-hidden"
            >
                <div className="absolute top-0 right-0 w-96 h-96 bg-neon-blue/5 blur-[100px] -mr-48 -mt-48 rounded-full" />
                <div className="relative z-10 h-full">
                    {children}
                </div>
            </motion.div>
        </div>
    );
};

export default GameLayout;
