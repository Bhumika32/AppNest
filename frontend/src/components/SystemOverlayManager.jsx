import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Flame, Lightbulb, Trophy } from 'lucide-react';
import { useOverlayStore } from '../store/overlayStore';

const SystemOverlayManager = () => {
    const { activeOverlay, hideOverlay } = useOverlayStore();

    if (!activeOverlay) return null;

    const isRoast = activeOverlay.type === 'roast';
    const Icon = activeOverlay.icon === 'Flame' ? Flame :
        activeOverlay.icon === 'Lightbulb' ? Lightbulb : Trophy;

    return (
        <AnimatePresence>
            <div className="fixed inset-0 z-[300] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.9, y: 20 }}
                    className={`relative max-w-lg w-full rounded-3xl border-2 p-8 shadow-2xl overflow-hidden
                        ${isRoast ? 'bg-deep-black border-neon-pink/30 shadow-neon-pink/10' : 'bg-deep-black border-neon-blue/30 shadow-neon-blue/10'}`}
                >
                    {/* Background Glow */}
                    <div className={`absolute -top-24 -right-24 w-48 h-48 rounded-full blur-[100px] opacity-20
                        ${isRoast ? 'bg-neon-pink' : 'bg-neon-blue'}`} />

                    <button
                        onClick={hideOverlay}
                        className="absolute top-4 right-4 p-2 text-gray-500 hover:text-white transition-colors"
                    >
                        <X size={20} />
                    </button>

                    <div className="flex flex-col items-center text-center">
                        <div className={`p-4 rounded-2xl mb-6 
                            ${isRoast ? 'bg-neon-pink/10 text-neon-pink' : 'bg-neon-blue/10 text-neon-blue'}`}>
                            <Icon size={40} />
                        </div>

                        <h2 className={`text-2xl font-black uppercase tracking-tight mb-2
                            ${isRoast ? 'text-neon-pink' : 'text-neon-blue'}`}>
                            {isRoast ? 'System Roast' : 'Neural Mentor Tip'}
                        </h2>

                        <p className="text-gray-300 text-lg leading-relaxed mb-8">
                            {activeOverlay.message}
                        </p>

                        <button
                            onClick={hideOverlay}
                            className={`px-8 py-3 rounded-xl font-bold uppercase tracking-widest text-sm transition-all
                                ${isRoast ? 'bg-neon-pink text-white shadow-[0_0_20px_rgba(255,0,128,0.4)] hover:scale-105' : 'bg-neon-blue text-deep-black shadow-[0_0_20px_rgba(0,243,255,0.4)] hover:scale-105'}`}
                        >
                            Understood
                        </button>
                    </div>
                </motion.div>
            </div>
        </AnimatePresence>
    );
};

export default SystemOverlayManager;
