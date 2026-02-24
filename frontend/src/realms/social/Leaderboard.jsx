import React from 'react';
import { motion } from 'framer-motion';
import { Trophy, Medal, Target, Zap, ArrowUp, ArrowDown, Minus } from 'lucide-react';

const LeaderboardRow = ({ rank, name, xp, change, icon: Icon, color }) => (
    <motion.div
        initial={{ opacity: 0, x: -20 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true }}
        className="flex items-center justify-between p-4 bg-white/5 border border-white/5 rounded-2xl hover:bg-white/10 transition-all group"
    >
        <div className="flex items-center gap-6">
            <div className={`w-8 text-center font-black ${rank <= 3 ? `text-${color}` : 'text-gray-600'}`}>
                {rank === 1 ? <Trophy size={18} className="mx-auto" /> : `#${rank}`}
            </div>
            <div className={`w-10 h-10 rounded-xl bg-${color}/10 flex items-center justify-center text-${color} border border-${color}/20`}>
                <Icon size={20} />
            </div>
            <div>
                <h4 className="font-black text-sm uppercase tracking-tight">{name}</h4>
                <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">Sector_7-B</div>
            </div>
        </div>
        <div className="flex items-center gap-8">
            <div className="text-right">
                <div className="text-sm font-black text-white">{xp.toLocaleString()}</div>
                <div className="text-[9px] text-gray-500 font-black uppercase">Neutral_XP</div>
            </div>
            <div className="w-12 flex justify-center">
                {change > 0 ? (
                    <div className="flex items-center gap-1 text-neon-green text-[10px] font-black">
                        <ArrowUp size={10} /> {change}
                    </div>
                ) : change < 0 ? (
                    <div className="flex items-center gap-1 text-red-500 text-[10px] font-black">
                        <ArrowDown size={10} /> {Math.abs(change)}
                    </div>
                ) : (
                    <Minus size={10} className="text-gray-700" />
                )}
            </div>
        </div>
    </motion.div>
);

const Leaderboard = () => {
    const topPerformers = [
        { rank: 1, name: 'AG_ZERO', xp: 125430, change: 12, icon: Zap, color: 'neon-blue' },
        { rank: 2, name: 'CYBER_PULSE', xp: 118220, change: -2, icon: Target, color: 'neon-pink' },
        { rank: 3, name: 'NEO_GHOST', xp: 95400, change: 5, icon: Medal, color: 'neon-green' },
        { rank: 4, name: 'QUANTUM_RAY', xp: 82100, change: 0, icon: Zap, color: 'neon-blue' },
        { rank: 5, name: 'VOID_WALKER', xp: 75600, change: -1, icon: Medal, color: 'neon-pink' },
    ];

    return (
        <div className="space-y-12 pb-20">
            <header className="relative p-12 rounded-[2rem] overflow-hidden bg-dark-surface/30 border border-white/5">
                <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-neon-green/5 blur-[120px] -mr-48 -mt-48 rounded-full" />
                <div className="relative z-10 max-w-2xl">
                    <div className="w-fit p-3 rounded-2xl bg-neon-green/10 border border-neon-green/20 text-neon-green mb-8">
                        <Trophy size={32} />
                    </div>
                    <h1 className="text-6xl font-black mb-6 tracking-tighter leading-[0.9]">
                        GLOBAL <span className="text-neon-green">RANKING</span><br />
                        MATRIX
                    </h1>
                    <p className="text-gray-400 text-lg leading-relaxed font-medium">
                        Compare your neural synchronization levels with other agents. Maintain high uptime to ascend the hierarchy.
                    </p>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <section className="lg:col-span-2 space-y-4">
                    <div className="flex items-center justify-between px-4 mb-6">
                        <h2 className="text-xl font-black tracking-tight uppercase flex items-center gap-3">
                            <div className="w-1.5 h-6 bg-neon-green rounded-full" />
                            Elite Synchronizers
                        </h2>
                        <span className="text-[10px] font-black text-gray-500 uppercase tracking-widest">Live Sync: Active</span>
                    </div>
                    {topPerformers.map(p => <LeaderboardRow key={p.rank} {...p} />)}

                    <button className="w-full mt-6 py-4 border border-white/5 hover:bg-white/5 rounded-2xl text-[10px] font-black text-gray-400 uppercase tracking-[0.3em] transition-all">
                        Load Complete Global Directory
                    </button>
                </section>

                <aside className="space-y-8">
                    <div className="bg-neon-blue/5 border border-neon-blue/20 rounded-3xl p-8">
                        <h3 className="text-sm font-black text-neon-blue uppercase tracking-widest mb-6">Your Status</h3>
                        <div className="flex items-center gap-4 mb-8">
                            <div className="w-16 h-16 rounded-2xl bg-neon-blue/20 border border-neon-blue/30 flex items-center justify-center text-neon-blue">
                                <span className="text-2xl font-black">#42</span>
                            </div>
                            <div>
                                <div className="text-xs font-black text-white uppercase">Agent_Zero</div>
                                <div className="text-[10px] text-gray-500 font-bold">Top 5.2% of Network</div>
                            </div>
                        </div>
                        <div className="space-y-4">
                            <div className="flex justify-between text-[10px] font-black uppercase text-gray-500">
                                <span>Next Rank</span>
                                <span className="text-neon-blue">840 XP Needed</span>
                            </div>
                            <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                                <div className="h-full bg-neon-blue w-[65%]" />
                            </div>
                        </div>
                    </div>

                    <div className="bg-dark-surface/40 border border-white/5 rounded-3xl p-8">
                        <h3 className="text-sm font-black text-white uppercase tracking-widest mb-6 underline decoration-neon-pink underline-offset-8 decoration-2">Circuit Rules</h3>
                        <ul className="space-y-4 text-xs text-gray-400 font-medium">
                            <li className="flex gap-3">
                                <div className="w-1 h-1 rounded-full bg-neon-pink mt-1.5" />
                                Daily resets occur at midnight UTC.
                            </li>
                            <li className="flex gap-3">
                                <div className="w-1 h-1 rounded-full bg-neon-pink mt-1.5" />
                                Game performance adds directly to your Neural XP.
                            </li>
                            <li className="flex gap-3">
                                <div className="w-1 h-1 rounded-full bg-neon-pink mt-1.5" />
                                Tool executions provide a base synchronization bonus.
                            </li>
                        </ul>
                    </div>
                </aside>
            </div>
        </div>
    );
};

export default Leaderboard;
