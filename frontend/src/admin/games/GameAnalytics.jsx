import React from 'react';
import { motion } from 'framer-motion';
import { Gamepad2, BarChart3, TrendingUp, Users, Zap, Clock, Star } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell, PieChart, Pie } from 'recharts';

const GameAnalytics = () => {
    // Mock data - in a real app, this would be fetched from adminAnalyticsStore
    const popularity = [
        { name: 'Neon Runner', sessions: 4500, active: 120, rating: 4.8 },
        { name: 'Tic-Tac-Toe AI', sessions: 3200, active: 45, rating: 4.2 },
        { name: 'Nexus Break', sessions: 1800, active: 12, rating: 4.5 },
        { name: 'Data Wing', sessions: 800, active: 8, rating: 3.9 },
    ];

    const COLORS = ['#00f3ff', '#ff00ff', '#39ff14', '#facc15'];

    return (
        <div className="space-y-8 pb-12">
            <header>
                <h1 className="text-3xl font-black mb-1 opacity-90 uppercase tracking-tighter">GAME <span className="text-neon-pink">ANALYTICS</span></h1>
                <p className="text-gray-500 text-[10px] uppercase tracking-[0.3em] font-black">Engagement Telemetry • Simulation Performance</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Popularity Chart */}
                <div className="lg:col-span-2 bg-dark-surface/40 border border-white/10 rounded-3xl p-8 backdrop-blur-md">
                    <h3 className="font-black text-xs uppercase tracking-widest mb-8 flex items-center gap-3">
                        <BarChart3 size={18} className="text-neon-pink" />
                        SESSION FREQUENCY BY SECTOR
                    </h3>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={popularity} layout="vertical">
                                <XAxis type="number" hide />
                                <YAxis dataKey="name" type="category" stroke="#555" fontSize={10} width={100} tick={{ fontWeight: 800 }} />
                                <Tooltip
                                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                                    contentStyle={{ backgroundColor: '#0a0a0c', border: '1px solid rgba(255,0,255,0.2)', borderRadius: '12px', fontSize: '10px' }}
                                />
                                <Bar dataKey="sessions" radius={[0, 4, 4, 0]}>
                                    {popularity.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Quick Stats */}
                <div className="space-y-6">
                    <div className="bg-dark-surface/30 border border-white/5 rounded-3xl p-6">
                        <div className="flex justify-between items-center mb-4">
                            <span className="text-[10px] font-black uppercase text-gray-500 tracking-widest">Active Players</span>
                            <Users size={16} className="text-neon-blue" />
                        </div>
                        <div className="text-3xl font-black tracking-tighter">185</div>
                        <div className="text-[9px] font-bold text-neon-green mt-1 flex items-center gap-1">
                            <TrendingUp size={10} /> +12% from last cycle
                        </div>
                    </div>

                    <div className="bg-dark-surface/30 border border-white/5 rounded-3xl p-6">
                        <div className="flex justify-between items-center mb-4">
                            <span className="text-[10px] font-black uppercase text-gray-500 tracking-widest">Avg. Session</span>
                            <Clock size={16} className="text-neon-pink" />
                        </div>
                        <div className="text-3xl font-black tracking-tighter">14.2m</div>
                        <div className="text-[9px] font-bold text-gray-600 mt-1 uppercase tracking-widest">Global Synchronization</div>
                    </div>

                    <div className="bg-dark-surface/30 border border-white/5 rounded-3xl p-6">
                        <div className="flex justify-between items-center mb-4">
                            <span className="text-[10px] font-black uppercase text-gray-500 tracking-widest">Platform Rating</span>
                            <Star size={16} className="text-yellow-500" />
                        </div>
                        <div className="text-3xl font-black tracking-tighter">4.6</div>
                        <div className="flex gap-1 mt-2">
                            {[1, 2, 3, 4, 5].map(i => <Star key={i} size={10} className={i <= 4 ? 'text-yellow-500 fill-yellow-500' : 'text-gray-700'} />)}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GameAnalytics;
