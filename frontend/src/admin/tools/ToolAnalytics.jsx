import React from 'react';
import { motion } from 'framer-motion';
import { Wrench, PieChart as PieChartIcon, TrendingUp, Cpu, Zap, Activity } from 'lucide-react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

const ToolAnalytics = () => {
    // Mock data - normally fetched from adminAnalyticsStore
    const toolUsage = [
        { name: 'Weather HUD', usage: 1240, color: '#00f3ff' },
        { name: 'Temporal Sync', usage: 850, color: '#ff00ff' },
        { name: 'Biometric Analysis', usage: 2100, color: '#39ff14' },
        { name: 'Market Converter', usage: 3400, color: '#facc15' },
        { name: 'Universal Scale', usage: 1100, color: '#00d2ff' },
    ];

    const weeklyTrend = [
        { day: 'Mon', loads: 420 },
        { day: 'Tue', loads: 510 },
        { day: 'Wed', loads: 480 },
        { day: 'Thu', loads: 620 },
        { day: 'Fri', loads: 890 },
        { day: 'Sat', loads: 950 },
        { day: 'Sun', loads: 780 },
    ];

    return (
        <div className="space-y-8 pb-12">
            <header>
                <h1 className="text-3xl font-black mb-1 opacity-90 uppercase tracking-tighter">TOOL <span className="text-neon-blue">ANALYTICS</span></h1>
                <p className="text-gray-500 text-[10px] uppercase tracking-[0.3em] font-black">Forge Utility Metrics • Neural Module Load Frequency</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Usage Distribution */}
                <div className="bg-dark-surface/40 border border-white/10 rounded-3xl p-8 backdrop-blur-sm">
                    <h3 className="font-black text-xs uppercase tracking-widest mb-8 flex items-center gap-3">
                        <PieChartIcon size={18} className="text-neon-blue" />
                        MODULE LOAD DISTRIBUTION
                    </h3>
                    <div className="h-[300px] w-full flex items-center justify-center min-h-[300px]">
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>
                                <Pie
                                    data={toolUsage}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={100}
                                    paddingAngle={8}
                                    dataKey="usage"
                                >
                                    {toolUsage.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} stroke="none" />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0a0a0c', border: '1px solid rgba(0,243,255,0.2)', borderRadius: '12px', fontSize: '10px' }}
                                    itemStyle={{ fontWeight: 'bold' }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Weekly Trend */}
                <div className="bg-dark-surface/40 border border-white/10 rounded-3xl p-8 backdrop-blur-sm">
                    <h3 className="font-black text-xs uppercase tracking-widest mb-8 flex items-center gap-3">
                        <TrendingUp size={18} className="text-neon-pink" />
                        WEEKLY SYNCHRONIZATION TREND
                    </h3>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={weeklyTrend}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff05" vertical={false} />
                                <XAxis dataKey="day" stroke="#555" fontSize={10} tickLine={false} axisLine={false} tick={{ fontWeight: 800 }} />
                                <YAxis hide />
                                <Tooltip
                                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                                    contentStyle={{ backgroundColor: '#0a0a0c', border: '1px solid rgba(255,0,255,0.2)', borderRadius: '12px', fontSize: '10px' }}
                                />
                                <Bar dataKey="loads" fill="#ff00ff" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* Performance Indicators */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                    { label: 'Avg. Latency', value: '18ms', icon: Activity, color: 'neon-green' },
                    { label: 'Compute Load', value: '42%', icon: Cpu, color: 'neon-blue' },
                    { label: 'Success Rate', value: '99.9%', icon: Zap, color: 'yellow-500' },
                ].map((stat, i) => (
                    <div key={i} className="bg-dark-surface/30 border border-white/5 rounded-2xl p-6 flex items-center gap-6">
                        <div className={`p-4 rounded-xl bg-${stat.color}/10 border border-${stat.color}/20 text-${stat.color}`}>
                            <stat.icon size={24} />
                        </div>
                        <div>
                            <p className="text-[10px] font-black uppercase text-gray-500 tracking-widest">{stat.label}</p>
                            <p className="text-2xl font-black tracking-tighter">{stat.value}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ToolAnalytics;
