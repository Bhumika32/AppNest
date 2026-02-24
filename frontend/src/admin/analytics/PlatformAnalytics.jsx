import React from 'react';
import { motion } from 'framer-motion';
import { BarChart3, Globe, Users, TrendingUp, Activity, Server } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, BarChart, Bar, Cell } from 'recharts';

const PlatformAnalytics = () => {
    // Mock global data
    const trafficData = [
        { name: '00:00', load: 45, users: 1200 },
        { name: '04:00', load: 30, users: 800 },
        { name: '08:00', load: 65, users: 2100 },
        { name: '12:00', load: 85, users: 3400 },
        { name: '16:00', load: 95, users: 4200 },
        { name: '20:00', load: 75, users: 2800 },
        { name: '23:59', load: 55, users: 1800 },
    ];

    const regionData = [
        { name: 'NA-WEST', value: 4500, color: '#00f3ff' },
        { name: 'EU-CENTRAL', value: 3200, color: '#ff00ff' },
        { name: 'ASIA-EAST', value: 2800, color: '#39ff14' },
        { name: 'SA-BRAZIL', value: 1200, color: '#facc15' },
    ];

    return (
        <div className="space-y-8 pb-12">
            <header>
                <h1 className="text-3xl font-black mb-1 opacity-90 uppercase tracking-tighter">PLATFORM <span className="text-neon-blue">ANALYTICS</span></h1>
                <p className="text-gray-500 text-[10px] uppercase tracking-[0.3em] font-black">Global Node Telemetry • Traffic Orchestration</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Traffic Area Chart */}
                <div className="lg:col-span-2 bg-dark-surface/40 border border-white/10 rounded-3xl p-8 backdrop-blur-sm">
                    <h3 className="font-black text-xs uppercase tracking-widest mb-8 flex items-center gap-3">
                        <Activity size={18} className="text-neon-blue" />
                        GLOBAL TRAFFIC LOAD (24H)
                    </h3>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={trafficData}>
                                <defs>
                                    <linearGradient id="colorLoad" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#00f3ff" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#00f3ff" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff05" vertical={false} />
                                <XAxis dataKey="name" stroke="#555" fontSize={10} tickLine={false} axisLine={false} tick={{ fontWeight: 800 }} />
                                <YAxis hide />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0a0a0c', border: '1px solid rgba(0,243,255,0.2)', borderRadius: '12px', fontSize: '10px' }}
                                />
                                <Area type="monotone" dataKey="load" stroke="#00f3ff" strokeWidth={4} fillOpacity={1} fill="url(#colorLoad)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Regional Stats */}
                <div className="bg-dark-surface/40 border border-white/10 rounded-3xl p-8 backdrop-blur-sm">
                    <h3 className="font-black text-xs uppercase tracking-widest mb-8 flex items-center gap-3">
                        <Globe size={18} className="text-neon-pink" />
                        REGIONAL DISTRIBUTION
                    </h3>
                    <div className="space-y-6">
                        {regionData.map((region, i) => (
                            <div key={i} className="space-y-2">
                                <div className="flex justify-between text-[10px] font-black uppercase tracking-widest">
                                    <span className="text-gray-400">{region.name}</span>
                                    <span style={{ color: region.color }}>{region.value.toLocaleString()}</span>
                                </div>
                                <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
                                    <div className="h-full" style={{ width: `${(region.value / 4500) * 100}%`, backgroundColor: region.color }} />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Platform Health Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                    { label: 'Core Uptime', value: '99.98%', icon: Server, color: 'neon-green' },
                    { label: 'Cache Hit Rate', value: '88.4%', icon: Activity, color: 'neon-blue' },
                    { label: 'Active WebSockets', value: '4.2k', icon: TrendingUp, color: 'neon-pink' },
                    { label: 'Neural Threads', value: '12,040', icon: Users, color: 'yellow-500' },
                ].map((stat, i) => (
                    <div key={i} className="bg-dark-surface/30 border border-white/5 rounded-2xl p-6 relative group overflow-hidden">
                        <div className={`absolute -right-4 -top-4 opacity-5 text-${stat.color}`}>
                            <stat.icon size={80} />
                        </div>
                        <div className={`p-2 rounded-lg bg-${stat.color}/10 border border-${stat.color}/20 text-${stat.color} w-fit mb-4`}>
                            <stat.icon size={18} />
                        </div>
                        <p className="text-[10px] font-black uppercase text-gray-500 tracking-widest">{stat.label}</p>
                        <p className="text-2xl font-black tracking-tighter">{stat.value}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PlatformAnalytics;
