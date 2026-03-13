import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, Zap, TrendingUp, Star } from 'lucide-react';

const XPRewardOverlay = ({ xpData, onClose }) => {
    if (!xpData) return null;

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-[70] flex items-center justify-center bg-black/80 backdrop-blur-md"
            >
                {/* Cinematic Background Lines */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                    <motion.div
                        initial={{ opacity: 0, scale: 0 }}
                        animate={{ opacity: [0, 1, 0], scale: [0, 2, 3] }}
                        transition={{ duration: 1.5, ease: "easeOut" }}
                        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-neon-blue/20 rounded-full blur-3xl"
                    />
                </div>

                <motion.div
                    initial={{ y: 50, scale: 0.8 }}
                    animate={{ y: 0, scale: 1 }}
                    transition={{ type: "spring", bounce: 0.5 }}
                    className="relative flex flex-col items-center z-10 p-8 max-w-lg w-full"
                >
                    <motion.div
                        initial={{ rotate: -180, scale: 0 }}
                        animate={{ rotate: 0, scale: 1 }}
                        transition={{ duration: 0.6, delay: 0.2, type: "spring" }}
                        className="w-24 h-24 rounded-full bg-gradient-to-br from-neon-blue to-neon-pink flex items-center justify-center mb-6 shadow-[0_0_40px_rgba(0,255,255,0.4)]"
                    >
                        <Zap size={48} className="text-white fill-white" />
                    </motion.div>

                    <h2 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400 uppercase tracking-tighter mb-2 text-center">
                        Session Complete
                    </h2>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4 }}
                        className="text-6xl font-black text-neon-blue drop-shadow-[0_0_15px_rgba(0,255,255,0.5)] my-6 flex items-center gap-2"
                    >
                        +{xpData.xp_awarded} <span className="text-3xl text-white">XP</span>
                    </motion.div>

                    {xpData.leveled_up && (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.5 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.8, type: "spring" }}
                            className="bg-neon-pink/10 border border-neon-pink text-neon-pink px-6 py-2 rounded-full font-bold uppercase tracking-widest flex items-center gap-2 mb-6 shadow-[0_0_20px_rgba(255,0,128,0.2)]"
                        >
                            <Star size={18} className="fill-neon-pink" />
                            Level Up! Rank: {xpData.rank_title}
                        </motion.div>
                    )}

                    <motion.button
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 1.2 }}
                        onClick={onClose}
                        className="mt-8 px-10 py-3 border border-white/20 text-white font-black uppercase tracking-widest rounded-full hover:bg-white hover:text-black transition-all"
                    >
                        Continue
                    </motion.button>
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
};

export default XPRewardOverlay;
