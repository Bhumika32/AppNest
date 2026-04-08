import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const GameSetupModal = ({ module, onStart }) => {
    const capabilities = module.capabilities || {};

    // ✅ NEW STRUCTURE
    const modes = capabilities.modes || [];
    const difficultyLevels = capabilities.difficulty_levels || [];
    console.log("CAPS:", module.capabilities);

    const [difficulty, setDifficulty] = useState(
        difficultyLevels[0]?.toUpperCase() || 'EASY'
    );

    const [mode, setMode] = useState(
        modes[0]?.toUpperCase() || 'SOLO'
    );

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
                    className="bg-black/40 border border-white/10 rounded-2xl p-8 max-w-md w-full shadow-2xl"
                >
                    <h2 className="text-3xl font-black text-white mb-2">
                        {module.name} <span className="text-neon-blue">INIT</span>
                    </h2>

                    <p className="text-gray-400 mb-6">{module.description}</p>

                    <div className="space-y-6">

                        {/* ✅ DIFFICULTY */}
                        {difficultyLevels.length > 0 && (
                            <div>
                                <label className="text-xs text-gray-400 uppercase mb-2 block">
                                    Difficulty
                                </label>

                                <div className="flex gap-2">
                                    {difficultyLevels.map((lvl) => {
                                        const L = lvl.toUpperCase();
                                        return (
                                            <button
                                                key={L}
                                                onClick={() => setDifficulty(L)}
                                                className={`flex-1 py-2 rounded border ${
                                                    difficulty === L
                                                        ? 'bg-neon-blue text-black'
                                                        : 'bg-white/5 text-gray-400'
                                                }`}
                                            >
                                                {L}
                                            </button>
                                        );
                                    })}
                                </div>
                            </div>
                        )}

                        {/* ✅ MODES */}
                        {modes.length > 0 && (
                            <div>
                                <label className="text-xs text-gray-400 uppercase mb-2 block">
                                    Mode
                                </label>

                                <div className="flex gap-2">
                                    {modes.map((m) => {
                                        const M = m.toUpperCase();
                                        return (
                                            <button
                                                key={M}
                                                onClick={() => setMode(M)}
                                                className={`flex-1 py-2 rounded border ${
                                                    mode === M
                                                        ? 'bg-neon-pink text-black'
                                                        : 'bg-white/5 text-gray-400'
                                                }`}
                                            >
                                                {M.replace('_', ' ')}
                                            </button>
                                        );
                                    })}
                                </div>
                            </div>
                        )}

                    </div>

                    <div className="mt-6 flex justify-end">
                        <button
                            onClick={handleStart}
                            className="px-6 py-3 bg-neon-blue text-black font-bold rounded"
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