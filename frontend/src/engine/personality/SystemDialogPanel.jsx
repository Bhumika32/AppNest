import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Terminal } from 'lucide-react';

const SystemDialogPanel = ({ message, active, type = 'info', onClose }) => {
    useEffect(() => {
        if (active) {
            const timer = setTimeout(() => {
                if (onClose) onClose();
            }, 4000);
            return () => clearTimeout(timer);
        }
    }, [active, onClose]);

    const colors = {
        info: 'text-neon-blue border-neon-blue shadow-[0_0_15px_rgba(0,255,255,0.2)]',
        success: 'text-neon-green border-neon-green shadow-[0_0_15px_rgba(0,255,0,0.2)]',
        error: 'text-neon-pink border-neon-pink shadow-[0_0_15px_rgba(255,0,128,0.2)]'
    };

    return (
        <AnimatePresence>
            {active && (
                <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 50 }}
                    className="fixed bottom-8 left-1/2 -translate-x-1/2 z-[80] pointer-events-none"
                >
                    <div className={`flex items-center gap-3 bg-black/90 border-l-4 ${colors[type].split(' ')[1]} p-3 pr-6 rounded-r-lg shadow-2xl backdrop-blur-md relative overflow-hidden`}>
                        {/* Scanline effect */}
                        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-white/5 to-transparent h-[200%] animate-[scan_2s_linear_infinite] opacity-50" />

                        <div className={`p-2 rounded bg-white/5 ${colors[type].split(' ')[0]}`}>
                            <Terminal size={20} />
                        </div>

                        <div className="flex flex-col">
                            <span className="text-[10px] uppercase font-black tracking-widest text-gray-400 mb-0.5">
                                System Override
                            </span>
                            <span className={`text-sm font-bold ${colors[type].split(' ')[0]}`}>
                                {message}
                            </span>
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default SystemDialogPanel;
