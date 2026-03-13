import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Trophy, Medal, Target, Zap, ArrowUp, ArrowDown, Minus, Loader2 } from 'lucide-react';
import { ModuleService } from '../../api/api';

const LeaderboardRow = ({ rank, name, xp, level, color = 'neon-blue' }) => {
    const icons = {
        1: Trophy,
        2: Medal,
        3: Target
    };
    const Icon = icons[rank] || Zap;
    const itemColor = rank === 1 ? 'neon-yellow' : rank === 2 ? 'gray-300' : rank === 3 ? 'orange-400' : color;

    return (
        <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center justify-between p-4 bg-white/5 border border-white/5 rounded-2xl hover:bg-white/10 transition-all group"
        >
            <div className="flex items-center gap-6">
                <div className={`w-8 text-center font-black ${rank <= 3 ? `text-${itemColor}` : 'text-gray-600'}`}>
                    {rank === 1 ? <Trophy size={18} className="mx-auto" /> : `#${rank}`}
                </div>
                <div className={`w-10 h-10 rounded-xl bg-${color}/10 flex items-center justify-center text-${color} border border-${color}/20`}>
                    <Icon size={20} />
                </div>
                <div>
                    <h4 className="font-black text-sm uppercase tracking-tight">{name}</h4>
                    <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">Level {level} Agent</div>
                </div>
            </div>
            <div className="flex items-center gap-8">
                <div className="text-right">
                    <div className="text-sm font-black text-white">{xp.toLocaleString()}</div>
                    <div className="text-[9px] text-gray-500 font-black uppercase">Neutral_XP</div>
                </div>
            </div>
        </motion.div>
    );
};

const Leaderboard = () => {
    const [rankings, setRankings] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchRankings = async () => {
            try {
                const { data } = await ModuleService.getGlobalLeaderboard(20);
                setRankings(data);
            } catch (err) {
                console.error("Failed to fetch rankings", err);
            } finally {
                setLoading(false);
            }
        };
        fetchRankings();
    }, []);

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

                    {loading ? (
                        <div className="flex flex-col items-center justify-center py-20">
                            <Loader2 className="animate-spin text-neon-green mb-4" size={48} />
                            <p className="text-gray-500 font-bold uppercase tracking-widest">Accessing Neural Registry...</p>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            <AnimatePresence>
                                {rankings.map(p => (
                                    <LeaderboardRow
                                        key={p.rank}
                                        rank={p.rank}
                                        name={p.name}
                                        xp={p.xp}
                                        level={p.level}
                                    />
                                ))}
                            </AnimatePresence>
                        </div>
                    )}
                </section>

                <aside className="space-y-8">
                    <div className="bg-neon-blue/5 border border-neon-blue/20 rounded-3xl p-8">
                        <h3 className="text-sm font-black text-neon-blue uppercase tracking-widest mb-6">Your Status</h3>
                        <p className="text-xs text-gray-400 mb-4">Complete modules to climb the rankings and secure your place in the matrix.</p>
                        <button className="w-full py-3 bg-neon-blue/10 border border-neon-blue/20 text-neon-blue font-black rounded-xl uppercase text-[10px] tracking-tighter hover:bg-neon-blue/20 transition-all">
                            View Personal Stats
                        </button>
                    </div>

                    <div className="bg-dark-surface/40 border border-white/5 rounded-3xl p-8">
                        <h3 className="text-sm font-black text-white uppercase tracking-widest mb-6 underline decoration-neon-pink underline-offset-8 decoration-2">Circuit Rules</h3>
                        <ul className="space-y-4 text-xs text-gray-400 font-medium">
                            <li className="flex gap-3">
                                <div className="w-1 h-1 rounded-full bg-neon-pink mt-1.5" />
                                Rankings are calculated based on total Neural XP.
                            </li>
                            <li className="flex gap-3">
                                <div className="w-1 h-1 rounded-full bg-neon-pink mt-1.5" />
                                Game performance adds directly to your Neural XP.
                            </li>
                            <li className="flex gap-3">
                                <div className="w-1 h-1 rounded-full bg-neon-pink mt-1.5" />
                                High performance in complex difficulties yields higher rewards.
                            </li>
                        </ul>
                    </div>
                </aside>
            </div>
        </div>
    );
};

export default Leaderboard;
