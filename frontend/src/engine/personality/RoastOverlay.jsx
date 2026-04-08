import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const RoastOverlay = ({ message, active, onClose }) => {
    useEffect(() => {
        if (active) {
            const timer = setTimeout(() => {
                if (onClose) onClose();
            }, 3000);
            return () => clearTimeout(timer);
        }
    }, [active, onClose]);

    return (
        <AnimatePresence>
            {active && (
                <motion.div
                    initial={{ opacity: 0, x: 50, y: 20 }}
                    animate={{ opacity: 1, x: 0, y: 0 }}
                    exit={{ opacity: 0, x: 50, scale: 0.9 }}
                    className="absolute top-1/4 right-8 z-[80] pointer-events-none max-w-[60%]"
                >
                    <div className="relative bg-black/80 border-2 border-neon-blue rounded-3xl rounded-tr-none p-4 max-w-sm shadow-[0_0_20px_rgba(0,255,255,0.3)] backdrop-blur-md">
                        {/* Triangle for speech bubble effect */}
                        <div className="absolute -top-2 right-0 w-4 h-4 bg-black border-t-2 border-r-2 border-neon-blue transform rotate-45" />

                        <div className="flex items-start gap-4">
                            <div className="w-10 h-10 rounded-full bg-neon-pink/20 border border-neon-pink flex-shrink-0 flex items-center justify-center overflow-hidden">
                                <img src={`https://api.dicebear.com/7.x/bottts/svg?seed=rival&colors=pink`} alt="Rival AI" className="w-full h-full" />
                            </div>
                            <p className="text-white font-bold leading-relaxed">
                                {message}
                            </p>
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default RoastOverlay;
