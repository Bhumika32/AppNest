import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Gamepad2, Play, Star, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useModuleStore } from '../../store/moduleStore.js';

const GameCard = ({ name, description, category, difficulty, rating = "4.8", version = "1.0", icon, slug }) => {
    const navigate = useNavigate();

    return (
        <motion.div
            whileHover={{ y: -8, scale: 1.02 }}
            className="group relative bg-dark-surface/40 border border-white/5 rounded-3xl p-8 overflow-hidden cursor-pointer hover:border-white/10 transition-all"
            onClick={() => navigate(`/dashboard/module/${slug}`)}
        >
            <div className={`absolute top-0 right-0 w-48 h-48 bg-neon-blue/5 blur-[80px] -mr-20 -mt-20 group-hover:bg-neon-blue/10 transition-all`} />

            <div className="relative z-10">
                <div className={`p-4 rounded-2xl bg-neon-blue/10 border border-neon-blue/20 w-fit mb-6 text-white`}>
                    <span className="text-3xl">{icon || '🎮'}</span>
                </div>

                <div className="flex items-center gap-2 mb-2">
                    <span className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-500">{category || 'Simulation'}</span>
                    <span className="w-1 h-1 rounded-full bg-gray-700" />
                    <div className="flex items-center gap-1">
                        <Star size={10} className="text-yellow-500 fill-yellow-500" />
                        <span className="text-[10px] font-black text-gray-400">{rating}</span>
                    </div>
                </div>

                <h3 className="text-2xl font-black mb-1 tracking-tighter uppercase">{name}</h3>
                <div className="text-[8px] font-black text-neon-blue mb-4 uppercase tracking-widest">v{version}</div>

                <p className="text-gray-400 text-sm leading-relaxed mb-8 opacity-80 group-hover:opacity-100 transition-opacity line-clamp-2">
                    {description}
                </p>

                <div className="flex items-center justify-between">
                    <div className="flex flex-col">
                        <span className="text-[8px] font-black text-gray-600 uppercase tracking-widest">Skill Level</span>
                        <span className="text-[10px] font-black uppercase text-neon-green">{difficulty}</span>
                    </div>

                    <motion.div
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        className={`p-3 rounded-full bg-white/5 border border-white/10 text-white group-hover:bg-neon-blue group-hover:text-black transition-all`}
                    >
                        <Play size={18} fill="currentColor" />
                    </motion.div>
                </div>
            </div>
        </motion.div>
    );
};

const ArcadeRealm = () => {
    const { modules, fetchModules, loading } = useModuleStore();
    const games = modules.filter(m => m.type === 'game');

    useEffect(() => {
        if (modules.length === 0) fetchModules();
    }, [modules.length, fetchModules]);

    if (loading) return (
        <div className="h-[60vh] flex flex-col items-center justify-center gap-4">
            <Loader2 className="animate-spin text-neon-blue" size={48} />
            <span className="text-[10px] font-black uppercase tracking-[0.4em] text-neon-blue">Mapping Virtual Realms...</span>
        </div>
    );

    return (
        <div className="space-y-12 pb-20">
            {/* Header */}
            <header className="relative p-12 rounded-[2rem] overflow-hidden bg-dark-surface/30 border border-white/5">
                <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-neon-blue/5 blur-[120px] -mr-48 -mt-48 rounded-full" />
                <div className="relative z-10 max-w-2xl">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="w-fit p-3 rounded-2xl bg-neon-blue/10 border border-neon-blue/20 text-neon-blue mb-8 shadow-[0_0_20px_rgba(0,243,255,0.2)]"
                    >
                        <Gamepad2 size={32} />
                    </motion.div>
                    <h1 className="text-6xl font-black mb-6 tracking-tighter leading-[0.9]">
                        THE <span className="text-neon-blue">ARCADE</span><br />
                        ARENA
                    </h1>
                    <p className="text-gray-400 text-lg leading-relaxed font-medium">
                        Access the neural simulation layer. Earn XP, climb the local leaderboards, and sharpen your cognitive reflexes.
                    </p>
                </div>
            </header>

            {/* Game Grid */}
            <section>
                <div className="flex items-center justify-between mb-10">
                    <h2 className="text-2xl font-black tracking-tight flex items-center gap-4">
                        <div className="w-2 h-8 bg-neon-pink rounded-full" />
                        AVAILABLE SIMULATIONS
                    </h2>
                </div>

                {games.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {games.map((game) => (
                            <GameCard key={game.id} {...game} />
                        ))}
                    </div>
                ) : (
                    <div className="p-20 border-2 border-dashed border-white/5 rounded-[2rem] text-center">
                        <p className="text-gray-600 font-bold uppercase tracking-widest text-xs">No active simulations detected in this sector.</p>
                    </div>
                )}
            </section>
        </div>
    );
};

export default ArcadeRealm;
