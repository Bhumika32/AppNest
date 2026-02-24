import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldAlert, Flame, Trash2, CheckCircle, MessageSquare, ShieldCheck, AlertTriangle } from 'lucide-react';

const RoastModeration = () => {
    // Mock flagged roasts - normally from an API
    const [flaggedRoasts, setFlaggedRoasts] = useState([
        { id: 1, content: "You look like a default skin in a game that's about to be shut down.", type: 'ultra', reason: 'High Entropy', user: 'agent_zero' },
        { id: 2, content: "Your code has more bugs than an abandoned server room.", type: 'normal', reason: 'System Flag', user: 'neo_coder' },
        { id: 3, content: "I've seen better processing power in a calculator from 1985.", type: 'random', reason: 'User Report', user: 'trinity' },
    ]);

    const handleAction = (id, approved) => {
        // In a real app, call moderationApi
        setFlaggedRoasts(prev => prev.filter(r => r.id !== id));
    };

    return (
        <div className="space-y-8 pb-12">
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div>
                    <h1 className="text-3xl font-black mb-1 opacity-90 uppercase tracking-tighter">ROAST <span className="text-neon-pink">MODERATION</span></h1>
                    <p className="text-gray-500 text-[10px] uppercase tracking-[0.3em] font-black">Neural Filter Protocol • Banter Entropy Oversight</p>
                </div>
                <div className="flex items-center gap-4">
                    <div className="px-5 py-2.5 bg-neon-pink/10 border border-neon-pink/20 rounded-xl flex items-center gap-3">
                        <Flame size={16} className="text-neon-pink" />
                        <span className="text-[10px] font-black uppercase text-neon-pink tracking-widest">Global Entropy: 85%</span>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Review Queue */}
                <div className="lg:col-span-2 space-y-4">
                    <h3 className="font-black text-xs uppercase tracking-widest mb-6 flex items-center gap-3">
                        <ShieldAlert size={18} className="text-neon-pink" />
                        REVIEW QUEUE ({flaggedRoasts.length})
                    </h3>

                    <AnimatePresence mode="popLayout">
                        {flaggedRoasts.map((roast) => (
                            <motion.div
                                key={roast.id}
                                layout
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, scale: 0.95 }}
                                className="bg-dark-surface/40 border border-white/10 rounded-2xl p-6 backdrop-blur-md relative overflow-hidden group"
                            >
                                <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-3 mb-3">
                                            <span className={`text-[9px] font-black px-2 py-0.5 rounded border ${roast.type === 'ultra' ? 'bg-neon-pink/10 border-neon-pink/20 text-neon-pink' : 'bg-neon-blue/10 border-neon-blue/20 text-neon-blue'
                                                } uppercase tracking-tighter`}>{roast.type} mode</span>
                                            <span className="text-[9px] font-black text-gray-500 uppercase tracking-widest flex items-center gap-1">
                                                <AlertTriangle size={10} className="text-yellow-500" /> {roast.reason}
                                            </span>
                                        </div>
                                        <p className="text-sm font-bold text-gray-200 italic leading-relaxed">"{roast.content}"</p>
                                        <div className="mt-3 text-[9px] font-black text-gray-600 uppercase tracking-widest">
                                            Originating Node: {roast.user}
                                        </div>
                                    </div>

                                    <div className="flex items-center gap-2">
                                        <button
                                            onClick={() => handleAction(roast.id, true)}
                                            className="p-3 bg-neon-green/10 border border-neon-green/20 text-neon-green rounded-xl hover:bg-neon-green hover:text-black transition-all"
                                        >
                                            <ShieldCheck size={18} />
                                        </button>
                                        <button
                                            onClick={() => handleAction(roast.id, false)}
                                            className="p-3 bg-neon-pink/10 border border-neon-pink/20 text-neon-pink rounded-xl hover:bg-neon-pink hover:text-black transition-all"
                                        >
                                            <Trash2 size={18} />
                                        </button>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {flaggedRoasts.length === 0 && (
                        <div className="h-64 border-2 border-dashed border-white/5 rounded-3xl flex flex-col items-center justify-center text-gray-600">
                            <ShieldCheck size={48} className="mb-4 opacity-20" />
                            <p className="text-[10px] font-black uppercase tracking-[0.4em]">All Sectors Synchronized</p>
                        </div>
                    )}
                </div>

                {/* Rules / Settings */}
                <div className="space-y-6">
                    <div className="bg-dark-surface/30 border border-white/5 rounded-3xl p-8">
                        <h3 className="font-black text-xs uppercase tracking-widest mb-6 flex items-center gap-3">
                            <MessageSquare size={18} className="text-neon-blue" />
                            BANTER PROTOCOLS
                        </h3>
                        <div className="space-y-4">
                            {[
                                { label: 'AI Toxicity Threshold', val: 75 },
                                { label: 'Sarcasm Intensity', val: 90 },
                                { label: 'Recursive Roasting', val: 40 },
                            ].map((p, i) => (
                                <div key={i} className="space-y-2">
                                    <div className="flex justify-between text-[9px] font-black uppercase tracking-widest">
                                        <span className="text-gray-400">{p.label}</span>
                                        <span className="text-neon-blue">{p.val}%</span>
                                    </div>
                                    <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
                                        <div className="h-full bg-neon-blue" style={{ width: `${p.val}%` }} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="bg-neon-pink/5 border border-neon-pink/20 rounded-3xl p-6">
                        <div className="flex gap-4">
                            <ShieldAlert className="text-neon-pink flex-shrink-0" />
                            <div className="space-y-2">
                                <p className="text-[10px] font-black uppercase text-neon-pink tracking-widest">Sanitary Mode Off</p>
                                <p className="text-[11px] font-bold text-gray-400 leading-relaxed">
                                    Ultra-burn models are currently unrestricted. Emotional shielding is recommended for all active agents.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RoastModeration;
