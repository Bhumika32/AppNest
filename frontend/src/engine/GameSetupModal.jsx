import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const GameSetupModal = ({ module, onStart }) => {
    const capabilities = module.capabilities || {};

    // Setup state
    const [difficulty, setDifficulty] = useState('EASY');
    const [mode, setMode] = useState('SOLO');

    const handleStart = () => {
        onStart({ difficulty, mode });
    };

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-[60] flex items-center justify-center bg-dark-bg/80 backdrop-blur-sm p-4"
            >
                <motion.div
                    initial={{ scale: 0.9, y: 20 }}
                    animate={{ scale: 1, y: 0 }}
                    className="bg-black/40 border border-white/10 rounded-2xl p-8 max-w-md w-full shadow-2xl overflow-hidden relative"
                >
                    {/* Glowing Accent */}
                    <div className="absolute -top-10 -right-10 w-32 h-32 bg-neon-blue/20 blur-3xl rounded-full" />

                    <h2 className="text-3xl font-black text-white uppercase tracking-tighter mb-2 relative z-10">
                        {module.name} <span className="text-neon-blue">INIT</span>
                    </h2>
                    <p className="text-gray-400 mb-8 relative z-10">{module.description}</p>

                    <div className="space-y-6 relative z-10">
                        {capabilities.supportsDifficulty && (
                            <div>
                                <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-3">Difficulty</label>
                                <div className="flex gap-2">
                                    {['EASY', 'MEDIUM', 'HARD'].map(level => (
                                        <button
                                            key={level}
                                            onClick={() => setDifficulty(level)}
                                            className={`flex-1 py-2 rounded border text-sm font-bold transition-all ${difficulty === level
                                                    ? 'bg-neon-blue/20 border-neon-blue text-neon-blue shadow-[0_0_15px_rgba(0,255,255,0.2)]'
                                                    : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:text-white'
                                                }`}
                                        >
                                            {level}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}

                        {(capabilities.supportsAI || capabilities.supportsPVP) && (
                            <div>
                                <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-3">Mode</label>
                                <div className="flex gap-2">
                                    <button
                                        onClick={() => setMode('SOLO')}
                                        className={`flex-1 py-2 rounded border text-sm font-bold transition-all ${mode === 'SOLO'
                                                ? 'bg-neon-pink/20 border-neon-pink text-neon-pink shadow-[0_0_15px_rgba(255,0,128,0.2)]'
                                                : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:text-white'
                                            }`}
                                    >
                                        SOLO
                                    </button>
                                    {capabilities.supportsAI && (
                                        <button
                                            onClick={() => setMode('VS_AI')}
                                            className={`flex-1 py-2 rounded border text-sm font-bold transition-all ${mode === 'VS_AI'
                                                    ? 'bg-neon-pink/20 border-neon-pink text-neon-pink shadow-[0_0_15px_rgba(255,0,128,0.2)]'
                                                    : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:text-white'
                                                }`}
                                        >
                                            VS AI
                                        </button>
                                    )}
                                    {capabilities.supportsPVP && (
                                        <button
                                            onClick={() => setMode('PVP')}
                                            className={`flex-1 py-2 rounded border text-sm font-bold transition-all ${mode === 'PVP'
                                                    ? 'bg-neon-pink/20 border-neon-pink text-neon-pink shadow-[0_0_15px_rgba(255,0,128,0.2)]'
                                                    : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:text-white'
                                                }`}
                                        >
                                            PVP
                                        </button>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="mt-8 pt-6 border-t border-white/10 relative z-10 flex justify-end gap-3">
                        <button
                            onClick={handleStart}
                            className="px-6 py-3 bg-neon-blue text-black font-black uppercase tracking-widest rounded hover:bg-white hover:shadow-[0_0_20px_rgba(0,255,255,0.4)] transition-all"
                        >
                            ENGAGE
                        </button>
                    </div>
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
};

export default GameSetupModal;
