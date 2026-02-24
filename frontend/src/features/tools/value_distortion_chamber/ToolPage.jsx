import React from 'react';
import { motion } from 'framer-motion';
import { Zap, ShieldAlert } from 'lucide-react';

const ToolPage = () => {
    return (
        <div className="max-w-4xl mx-auto space-y-12">
            <header className="p-10 rounded-3xl bg-dark-surface/30 border border-white/5 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-64 h-64 bg-neon-blue/10 blur-[100px] -mr-20 -mt-20" />
                <div className="relative z-10 flex items-center gap-8">
                    <div className="p-4 rounded-2xl bg-neon-blue/10 border border-neon-blue/20 text-neon-blue animate-pulse">
                        <Zap size={40} />
                    </div>
                    <div>
                        <h1 className="text-4xl font-black mb-2 uppercase tracking-tighter">VALUE DISTORTION <span className="text-neon-blue">CHAMBER</span></h1>
                        <p className="text-gray-500 text-sm font-medium">Manipulate reality scales and objective metrics through our proprietary distortion engine.</p>
                    </div>
                </div>
            </header>

            <section className="p-12 border-2 border-dashed border-white/5 rounded-3xl flex flex-col items-center justify-center text-center space-y-6">
                <ShieldAlert className="text-neon-pink" size={48} />
                <div className="space-y-2">
                    <h2 className="text-xl font-black uppercase">Interace_Standby</h2>
                    <p className="text-gray-500 max-w-sm text-sm">The distortion matrix is currently calibrating. Please maintain neural sync while we finalize the interface injection.</p>
                </div>
                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="px-8 py-3 bg-neon-blue text-black font-black rounded-xl uppercase tracking-widest text-xs"
                >
                    Initialize Distortion
                </motion.button>
            </section>
        </div>
    );
};

export default ToolPage;
