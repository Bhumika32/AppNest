import React from 'react';
import { motion } from 'framer-motion';
import {
    Activity, Trophy, Clock, Gamepad2, Wrench, Zap,
    ChevronRight, ArrowUpRight, BrainCircuit, Sparkles
} from 'lucide-react';
import {
    ResponsiveContainer, AreaChart, Area, XAxis, YAxis,
    CartesianGrid, Tooltip
} from 'recharts';
import { useAuthStore } from '../../store/authStore';
import { useUserStore } from '../../store/userStore';
import LoadingSkeleton, { ChartSkeleton, BountySkeleton } from '../../components/LoadingSkeleton';

const RealmCard = ({ title, subtitle, icon: Icon, color }) => (
    <motion.div
        whileHover={{ y: -5, scale: 1.02 }}
        className="bg-dark-surface/30 border border-white/5 rounded-3xl p-8 relative overflow-hidden group hover:border-white/10 transition-all cursor-pointer"
    >
        <div className={`absolute top-0 right-0 w-32 h-32 bg-${color}/10 blur-3xl -mr-16 -mt-16 opacity-0 group-hover:opacity-100 transition-opacity`} />
        <div className={`w-12 h-12 rounded-2xl bg-${color}/10 border border-${color}/20 flex items-center justify-center text-${color} mb-6 group-hover:scale-110 transition-transform`}>
            <Icon size={24} />
        </div>
        <h3 className="text-xl font-black mb-3 tracking-tighter uppercase">{title}</h3>
        <p className="text-gray-500 text-sm font-medium mb-6 leading-relaxed">{subtitle}</p>
        <div className={`flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-${color}`}>
            Initiate Link <ArrowUpRight size={14} />
        </div>
    </motion.div>
);

const HomePortal = () => {
    const user = useAuthStore(state => state.user);
    const rank = useUserStore(state => state.rank);
    const uptime = useUserStore(state => state.uptime);
    const performanceHistory = useUserStore(state => state.performanceHistory);
    const dailyQuests = useUserStore(state => state.dailyQuests);
    const isLoading = useUserStore(state => state.isLoading);
    const error = useUserStore(state => state.error);
    const fetchDashboard = useUserStore(state => state.fetchDashboard);

    if (error) {
        return (
            <div className="bg-red-500/10 border border-red-500/20 rounded-2xl p-8 text-center max-w-2xl mx-auto my-20">
                <div className="text-red-500 mb-4 font-black uppercase tracking-widest flex items-center justify-center gap-2">
                    <Activity size={24} />
                    Link Error
                </div>
                <p className="text-gray-400 mb-6">{error}</p>
                <button
                    onClick={() => fetchDashboard()}
                    className="px-8 py-3 bg-red-500 text-white font-black rounded-xl hover:bg-red-600 transition-colors uppercase tracking-tighter"
                >
                    Retry Connection
                </button>
            </div>
        );
    }

    return (
        <div className="space-y-8 max-w-7xl mx-auto pb-12">
            {/* Hero Section */}
            <section className="relative rounded-3xl overflow-hidden bg-dark-surface/30 border border-white/5 p-8 lg:p-12">
                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-neon-blue/5 blur-[120px] -mr-48 -mt-48 rounded-full" />

                <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-12">
                    <div className="flex-1">
                        <motion.div
                            initial={{ x: -20, opacity: 0 }}
                            animate={{ x: 0, opacity: 1 }}
                            className="flex items-center gap-3 text-neon-blue mb-6"
                        >
                            <div className="w-2 h-2 rounded-full bg-neon-blue animate-ping" />
                            <span className="text-[10px] font-black uppercase tracking-[0.4em]">Sub-Neural Link: Active</span>
                        </motion.div>
                        <h1 className="text-5xl lg:text-7xl font-black mb-6 leading-[0.9]">
                            GREETINGS,<br />
                            <span className="bg-gradient-to-r from-neon-blue via-neon-pink to-neon-blue bg-[length:200%_auto] bg-clip-text text-transparent animate-gradient-x">
                                {user?.username?.toUpperCase() || 'AGENT_ZERO'}
                            </span>
                        </h1>
                        <p className="text-gray-400 text-lg max-w-xl mb-10 leading-relaxed font-medium">
                            The ecosystem has synchronized with your neural signature. Your performance metrics are within optimal range.
                        </p>
                        <div className="flex flex-wrap gap-4">
                            <motion.button
                                whileTap={{ scale: 0.95 }}
                                className="px-10 py-4 bg-neon-blue text-black font-black rounded-xl hover:shadow-[0_0_30px_rgba(0,243,255,0.4)] transition-all uppercase tracking-tighter"
                            >
                                Resume Sync
                            </motion.button>
                            <button className="px-10 py-4 bg-white/5 border border-white/10 hover:bg-white/10 font-black rounded-xl transition-all text-white uppercase tracking-tighter">
                                Activity Logs
                            </button>
                        </div>
                    </div>

                    {/* Quick Stats Grid */}
                    <div className="grid grid-cols-2 gap-4 w-full lg:w-96">
                        {[
                            { label: 'Neural Rank', value: rank, icon: Trophy, color: 'text-neon-blue', bg: 'bg-neon-blue/5' },
                            { label: 'Active Uptime', value: uptime, icon: Clock, color: 'text-neon-pink', bg: 'bg-neon-pink/5' },
                        ].map((stat, i) => (
                            <div key={i} className={`${stat.bg} border border-white/5 rounded-2xl p-6 flex flex-col items-center group hover:border-white/10 transition-all`}>
                                <stat.icon className={`${stat.color} mb-3 group-hover:scale-110 transition-transform`} size={28} />
                                {isLoading ? (
                                    <LoadingSkeleton className="h-6 w-16 mb-1" />
                                ) : (
                                    <span className="text-2xl font-black tracking-tighter mb-1">{stat.value}</span>
                                )}
                                <span className="text-[10px] text-gray-500 uppercase font-black tracking-widest">{stat.label}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Performance Matrix (Recharts) */}
                <section className="lg:col-span-2 bg-dark-surface/20 border border-white/5 rounded-3xl p-8 relative overflow-hidden group">
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <h3 className="text-xl font-black tracking-tight mb-1 flex items-center gap-2">
                                <Activity className="text-neon-blue" size={20} />
                                NEURAL PERFORMANCE
                            </h3>
                            <p className="text-xs text-gray-500 font-bold uppercase tracking-widest">XP Synchronization (Last 7 Cycles)</p>
                        </div>
                        <div className="flex items-center gap-4 text-[10px] font-black uppercase text-gray-500">
                            <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-neon-blue" /> Actual</div>
                            <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-neon-pink/30" /> Reference</div>
                        </div>
                    </div>

                    <div className="h-[300px] w-full min-h-[300px]">
                        {isLoading ? (
                            <ChartSkeleton />
                        ) : (
                            <ResponsiveContainer width="100%" height={300}>
                                <AreaChart data={performanceHistory}>
                                    <defs>
                                        <linearGradient id="colorXp" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#00f3ff" stopOpacity={0.3} />
                                            <stop offset="95%" stopColor="#00f3ff" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff05" vertical={false} />
                                    <XAxis
                                        dataKey="day"
                                        stroke="#555"
                                        fontSize={10}
                                        tickLine={false}
                                        axisLine={false}
                                        tick={{ fontWeight: 800 }}
                                    />
                                    <YAxis hide />
                                    <Tooltip
                                        contentStyle={{
                                            backgroundColor: '#0a0a0c',
                                            border: '1px solid rgba(255,255,255,0.1)',
                                            borderRadius: '12px',
                                            fontSize: '12px',
                                            fontWeight: 'bold'
                                        }}
                                        itemStyle={{ color: '#00f3ff' }}
                                    />
                                    <Area
                                        type="monotone"
                                        dataKey="xp"
                                        stroke="#00f3ff"
                                        strokeWidth={4}
                                        fillOpacity={1}
                                        fill="url(#colorXp)"
                                        animationDuration={2000}
                                    />
                                </AreaChart>
                            </ResponsiveContainer>
                        )}
                    </div>
                </section>

                {/* AI Mentor & Quests Panel */}
                <aside className="space-y-8">
                    {/* AI Mentor Advice */}
                    <section className="bg-gradient-to-br from-neon-blue/20 to-neon-pink/20 border border-white/10 rounded-3xl p-8 relative overflow-hidden group">
                        <div className="absolute -top-4 -right-4 text-white/5 group-hover:text-white/10 transition-colors">
                            <BrainCircuit size={120} />
                        </div>
                        <h3 className="font-black text-sm mb-6 flex items-center gap-3 text-white uppercase tracking-widest">
                            <Sparkles size={16} className="text-neon-blue" />
                            Neural Advisor
                        </h3>
                        <div className="relative z-10">
                            <p className="text-sm font-medium text-gray-200 leading-relaxed italic">
                                "Your recent performance in Tic Tac Toe suggests a tactical deviation. Try controlling the center square to optimize your neural XP yield."
                            </p>
                            <div className="mt-6 flex items-center gap-3">
                                <div className="w-8 h-8 rounded-lg bg-neon-blue/20 flex items-center justify-center text-neon-blue">
                                    <Activity size={14} />
                                </div>
                                <span className="text-[10px] font-black uppercase tracking-widest text-gray-400">Status: Analyzing...</span>
                            </div>
                        </div>
                    </section>

                    {/* Daily Quests List */}
                    <section className="bg-dark-surface/40 border border-white/5 rounded-3xl p-8 backdrop-blur-sm">
                        <h3 className="font-black text-xl mb-8 flex items-center gap-3">
                            <Trophy size={22} className="text-neon-pink" />
                            ACTIVE BOUNTIES
                        </h3>
                        {isLoading ? (
                            <BountySkeleton />
                        ) : (
                            <div className="space-y-6">
                                {dailyQuests.map((q) => (
                                    <div key={q.id} className="flex flex-col gap-3 group cursor-help">
                                        <div className="flex justify-between items-center">
                                            <span className="text-xs font-bold text-gray-300 group-hover:text-white transition-colors">{q.task}</span>
                                            <span className={`text-[10px] font-black px-2 py-0.5 rounded border border-white/20 bg-white/5 text-neon-blue`}>
                                                {q.reward}
                                            </span>
                                        </div>
                                        <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden border border-white/5">
                                            <motion.div
                                                initial={{ width: 0 }}
                                                animate={{ width: `${q.progress}%` }}
                                                className={`h-full bg-gradient-to-r from-neon-blue to-neon-pink rounded-full transition-all duration-1000`}
                                            />
                                        </div>
                                        <div className="flex justify-end text-[8px] font-black text-gray-600 uppercase tracking-widest">
                                            {q.progress}% Complete
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                        <button className="w-full mt-10 py-3 border border-white/5 hover:border-white/10 hover:bg-white/5 rounded-xl text-[10px] font-black text-gray-500 uppercase tracking-widest transition-all">
                            Refresh Bounty Board
                        </button>
                    </section>
                </aside>
            </div>

            {/* Featured Realms */}
            <section className="pt-8">
                <div className="flex items-center justify-between mb-8">
                    <h2 className="text-3xl font-black flex items-center gap-4">
                        <div className="w-3 h-10 bg-neon-blue rounded-full" />
                        CORE ACCESS
                    </h2>
                    <span className="text-[10px] font-black text-gray-500 hover:text-neon-blue cursor-pointer transition-colors tracking-[0.2em]">INITIATE GLOBAL SEARCH</span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <RealmCard
                        title="THE ARCADE"
                        subtitle="Retro-futuristic gaming arena. High octane performance required."
                        icon={Gamepad2}
                        color="neon-blue"
                    />
                    <RealmCard
                        title="FORGE TOOLS"
                        subtitle="Precision utility modules for digital manipulation and analysis."
                        icon={Wrench}
                        color="neon-pink"
                    />
                    <RealmCard
                        title="ROAST ARENA"
                        subtitle="Neural network banter combat. Emotional shielded protocol recommended."
                        icon={Zap}
                        color="neon-green"
                    />
                </div>
            </section>
        </div>
    );
};

export default HomePortal;
