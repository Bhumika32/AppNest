import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Wrench, Search, Zap, Cpu, Star, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useModuleStore } from '../../store/moduleStore.js';

const ToolCard = ({ name, description, icon, category, version = "1.0", xp_reward = 200, slug }) => {
    const navigate = useNavigate();

    return (
        <motion.div
            whileHover={{ scale: 1.02, y: -5 }}
            className="group relative bg-[#0d0d12] border border-white/5 rounded-2xl p-6 cursor-pointer hover:border-white/10 transition-all overflow-hidden"
            onClick={() => navigate(`/dashboard/module/${slug}`)}
        >
            <div className={`absolute top-0 right-0 w-32 h-32 bg-neon-pink/5 blur-[60px] -mr-16 -mt-16 group-hover:bg-neon-pink/10 transition-all`} />

            <div className="relative z-10">
                <div className={`p-3 rounded-xl bg-white/5 border border-white/10 w-fit mb-5 text-white group-hover:text-neon-pink transition-colors`}>
                    <span className="text-2xl">{icon || '🛠️'}</span>
                </div>

                <div className="flex items-center gap-2 mb-2">
                    <span className="text-[10px] font-black uppercase tracking-widest text-gray-500">{category || 'Utility'}</span>
                    <span className="w-1 h-1 rounded-full bg-gray-800" />
                    <span className="text-[9px] font-black text-gray-600 uppercase tracking-tighter">Active Sync</span>
                </div>

                <h3 className="text-lg font-black mb-1 tracking-tight uppercase group-hover:text-white transition-colors">{name}</h3>
                <div className="text-[7px] font-black text-neon-blue mb-4 uppercase tracking-[0.3em]">Module_v{version}</div>

                <p className="text-gray-500 text-xs leading-relaxed mb-6 opacity-80 group-hover:opacity-100 line-clamp-2">
                    {description}
                </p>

                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-[9px] font-black text-neon-blue uppercase tracking-[0.2em] opacity-0 group-hover:opacity-100 transition-all duration-300">
                        Execute Module <Zap size={10} fill="currentColor" />
                    </div>
                    <div className="text-[8px] font-black text-neon-green uppercase">+{xp_reward} XP</div>
                </div>
            </div>
        </motion.div>
    );
};

const ForgeRealm = () => {
    const { modules, fetchModules, loading } = useModuleStore();
    const [searchQuery, setSearchQuery] = useState('');
    const tools = modules.filter(m => m.type === 'tool');

    useEffect(() => {
        if (modules.length === 0) fetchModules();
    }, [modules.length, fetchModules]);

    const filteredTools = tools.filter(t =>
        t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.category?.toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (loading) return (
        <div className="h-[60vh] flex flex-col items-center justify-center gap-4">
            <Loader2 className="animate-spin text-neon-pink" size={48} />
            <span className="text-[10px] font-black uppercase tracking-[0.4em] text-neon-pink">Forging Toolsets...</span>
        </div>
    );

    return (
        <div className="space-y-10 pb-20">
            {/* Header */}
            <header className="relative p-10 rounded-[2rem] overflow-hidden bg-dark-surface/40 border border-white/5 backdrop-blur-md">
                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-neon-pink/5 blur-[100px] -mr-40 -mt-40 rounded-full" />
                <div className="relative z-10 flex flex-col md:flex-row items-center gap-10">
                    <div className="p-5 rounded-3xl bg-neon-pink/10 border border-neon-pink/20 text-neon-pink shadow-[0_0_30px_rgba(255,0,255,0.15)]">
                        <Wrench size={48} />
                    </div>
                    <div>
                        <h1 className="text-5xl font-black mb-3 tracking-tighter uppercase">Forge <span className="text-neon-pink">Assistant</span></h1>
                        <p className="text-gray-400 max-w-xl text-sm leading-relaxed font-medium">
                            Synthesize real-world data with AI-enhanced precision. Use our suite of utility modules for instant environmental and temporal analysis.
                        </p>
                    </div>
                </div>
            </header>

            {/* Tool Grid */}
            <section>
                <div className="flex items-center justify-between mb-8">
                    <h2 className="text-xl font-black tracking-widest flex items-center gap-3">
                        <div className="w-1.5 h-6 bg-neon-blue rounded-full" />
                        ACTIVE MODULES
                    </h2>
                    <div className="relative group">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-neon-blue transition-colors" size={14} />
                        <input
                            type="text"
                            placeholder="Search Modules..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="bg-white/5 border border-white/10 rounded-xl py-2 pl-10 pr-4 text-xs font-bold focus:outline-none focus:border-neon-blue/50 focus:bg-white/10 transition-all w-64"
                        />
                    </div>
                </div>

                {filteredTools.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filteredTools.map((tool) => (
                            <ToolCard key={tool.id} {...tool} />
                        ))}
                    </div>
                ) : (
                    <div className="p-20 border-2 border-dashed border-white/5 rounded-[2rem] text-center">
                        <p className="text-gray-600 font-bold uppercase tracking-widest text-xs">No utility modules detected in this sector.</p>
                    </div>
                )}
            </section>
        </div>
    );
};

export default ForgeRealm;
