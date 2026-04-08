import React from 'react';
import { motion } from 'framer-motion';
import {
    Users, Gamepad2, Wrench, Flame, Activity, TrendingUp,
    ArrowUp, ArrowDown, Shield
} from 'lucide-react';
import {
    AreaChart, Area, XAxis, YAxis,
    CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { useAdminAnalyticsStore } from '../../store/adminAnalyticsStore';

const StatWidget = ({ title, value, change, icon: Icon, color, isLoading }) => (
    <motion.div
        whileHover={{ scale: 1.02 }}
        className="bg-dark-surface border border-white/10 rounded-2xl p-6 relative overflow-hidden"
    >
        <div className={`absolute -right-4 -top-4 opacity-5 text-neon-blue`}>
            <Icon size={120} />
        </div>
        <div className="flex justify-between items-start mb-4">
            <div className={`p-2 rounded-lg bg-${color}/10 border border-${color}/20 text-neon-blue`}>
                <Icon size={20} />
            </div>
            {!isLoading && (
                <div className={`flex items-center gap-1 text-xs font-bold ${change >= 0 ? 'text-neon-green' : 'text-neon-pink'}`}>
                    {change >= 0 ? <ArrowUp size={12} /> : <ArrowDown size={12} />}
                    {Math.abs(change)}%
                </div>
            )}
        </div>
        <h3 className="text-gray-500 text-[10px] uppercase tracking-widest font-black mb-1">{title}</h3>
        {isLoading ? (
            <div className="h-9 w-24 bg-white/5 animate-pulse rounded-lg" />
        ) : (
            <div className="text-3xl font-black tracking-tighter">{value}</div>
        )}
    </motion.div>
);

const AdminOverview = () => {
    const { stats, isLoading, fetchStats } = useAdminAnalyticsStore();

    React.useEffect(() => {
        fetchStats();
    }, [fetchStats]);

    return (
        <div className="space-y-8 max-w-7xl mx-auto pb-12">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-black mb-1 tracking-tighter uppercase">COMMAND CENTER</h1>
                    <p className="text-gray-500 text-[10px] uppercase tracking-[0.3em] font-black">Platform Overview • Neural Telemetry Active</p>
                </div>
                <div className="flex items-center gap-3">
                    <button
                        onClick={fetchStats}
                        className="px-6 py-2.5 bg-white/5 border border-white/10 hover:bg-white/10 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all"
                    >
                        REFRESH SYNC
                    </button>
                    <button className="px-6 py-2.5 bg-neon-pink text-black font-black rounded-xl text-[10px] uppercase tracking-widest hover:shadow-[0_0_30px_rgba(255,0,255,0.4)] transition-all">
                        EMERGENCY LOCKDOWN
                    </button>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatWidget
                    title="Active Users"
                    value={stats.activeUsers.toLocaleString()}
                    change={12.5}
                    icon={Users}
                    color="neon-blue"
                    isLoading={isLoading}
                />
                <StatWidget
                    title="Matches Today"
                    value={stats.matchesToday.toLocaleString()}
                    change={-3.2}
                    icon={Gamepad2}
                    color="neon-pink"
                    isLoading={isLoading}
                />
                <StatWidget
                    title="Tool Executions"
                    value={stats.toolUsageCount.toLocaleString()}
                    change={44.1}
                    icon={Wrench}
                    color="neon-blue"
                    isLoading={isLoading}
                />
                <StatWidget
                    title="Roast Battles"
                    value={stats.roastBattles.toLocaleString()}
                    change={2.8}
                    icon={Flame}
                    color="neon-blue"
                    isLoading={isLoading}
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main Chart */}
                <div className="lg:col-span-2 bg-dark-surface/40 border border-white/10 rounded-3xl p-8 backdrop-blur-sm">
                    <div className="flex items-center justify-between mb-8">
                        <h3 className="font-black text-xs uppercase tracking-widest flex items-center gap-3">
                            <TrendingUp size={20} className="text-neon-blue" />
                            NEURAL POPULATION TREND
                        </h3>
                        <div className="flex gap-2">
                            {['Live', '24h', '7d'].map(t => (
                                <button key={t} className={`px-4 py-1 text-[10px] font-black uppercase rounded-lg border border-white/5 ${t === '24h' ? 'bg-neon-blue text-black border-neon-blue' : 'text-gray-500 hover:text-white hover:bg-white/5'}`}>
                                    {t}
                                </button>
                            ))}
                        </div>
                    </div>
                    <div className="h-[300px] w-full min-h-[300px]">
                        {isLoading ? (
                            <div className="h-full w-full bg-white/5 rounded-2xl animate-pulse flex items-center justify-center text-[10px] font-black uppercase tracking-[0.5em] text-gray-600">
                                Calibrating Visuals...
                            </div>
                        ) : (
                            <ResponsiveContainer width="100%" height={300}>
                                <AreaChart data={stats.platformGrowth}>
                                    <defs>
                                        <linearGradient id="colorUsers" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#00f3ff" stopOpacity={0.3} />
                                            <stop offset="95%" stopColor="#00f3ff" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff05" vertical={false} />
                                    <XAxis
                                        dataKey="date"
                                        stroke="#555"
                                        fontSize={10}
                                        tickLine={false}
                                        axisLine={false}
                                        tick={{ fontWeight: 800 }}
                                    />
                                    <YAxis hide />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#0a0a0c', border: '1px solid rgba(0,243,255,0.2)', borderRadius: '12px', fontSize: '10px' }}
                                        itemStyle={{ color: '#00f3ff', fontWeight: 'bold' }}
                                    />
                                    <Area type="monotone" dataKey="users" stroke="#00f3ff" strokeWidth={4} fillOpacity={1} fill="url(#colorUsers)" />
                                </AreaChart>
                            </ResponsiveContainer>
                        )}
                    </div>
                </div>

                {/* System Health / Flags */}
                <div className="bg-dark-surface/40 border border-white/10 rounded-3xl p-8 backdrop-blur-sm">
                    <h3 className="font-black text-xs uppercase tracking-widest mb-6 flex items-center gap-3">
                        <Shield size={20} className="text-neon-pink" />
                        CORE INTEGRITY
                    </h3>
                    <div className="space-y-8">
                        {[
                            { label: 'Database Node', status: 'optimal', load: 12, color: 'neon-green' },
                            { label: 'WebSocket Hub', status: 'stressed', load: 88, color: 'neon-pink' },
                            { label: 'AI Inference', status: 'optimal', load: 45, color: 'neon-blue' },
                        ].map((node, i) => (
                            <div key={i} className="space-y-3">
                                <div className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest">
                                    <span className="text-gray-400">{node.label}</span>
                                    <span className={node.status === 'optimal' ? 'text-neon-green' : 'text-neon-pink'}>
                                        {node.status}
                                    </span>
                                </div>
                                <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden border border-white/5">
                                    <motion.div
                                        initial={{ width: 0 }}
                                        animate={{ width: `${node.load}%` }}
                                        className={`h-full rounded-full bg-${node.color}`}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="mt-12 pt-8 border-t border-white/5">
                        <div className="flex items-center gap-4 text-neon-pink bg-neon-pink/5 p-5 rounded-2xl border border-neon-pink/20">
                            <Activity className="animate-pulse flex-shrink-0" />
                            <div>
                                <p className="text-[10px] font-black uppercase tracking-widest">Anomaly Detected</p>
                                <p className="text-[10px] font-bold text-gray-400 mt-1">Roast Realm bypass attempt blocked at sector 0X-2.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AdminOverview;
