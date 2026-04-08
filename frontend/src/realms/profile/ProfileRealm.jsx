import React from 'react';
import { motion } from 'framer-motion';
import { User, Mail, Shield, Award, Activity, Edit3, Key } from 'lucide-react';
import { useAuthStore } from '../../store/authStore.js';
import { useUserStore } from '../../store/userStore.js';
import { UserService } from '../../api/api';
import { useState, useRef } from 'react';
import { Settings } from 'lucide-react';
//import Settings from "../../pages/Settings";

const ProfileRealm = () => {
    const { user } = useAuthStore();
    const setUser = useAuthStore(state => state.setUser);
    const { level, xp, nextLevelXp, rank, achievements } = useUserStore();
    const inputRef = useRef(null);
    const [uploading, setUploading] = useState(false);

    const xpPercentage = (xp / nextLevelXp) * 100;

    const metadata = [
        { label: 'Neural Identity', value: user?.username || 'ANON_AGENT', icon: User },
        { label: 'Network Address', value: user?.email || 'N/A', icon: Mail },
        { label: 'Access Level', value: user?.role?.toUpperCase() || 'USER', icon: Shield },
        { label: 'System Rank', value: rank, icon: Award },
    ];

    return (
        <div className="space-y-10 pb-20">
            {/* Header / Banner */}
            <header className="relative h-64 rounded-[2rem] overflow-hidden bg-dark-surface/40 border border-white/5">
                <div className="absolute inset-0 bg-gradient-to-r from-neon-blue/10 via-neon-pink/10 to-neon-blue/10 animate-gradient-x bg-[length:200%_auto]" />
                <div className="absolute bottom-0 left-0 w-full p-10 flex items-end justify-between z-10">
                    <div className="flex items-center gap-8">
                        <div className="relative group">
                            <div className="w-24 h-24 rounded-2xl bg-dark-surface border-2 border-neon-blue p-1 shadow-[0_0_20px_rgba(0,243,255,0.3)]">
                                <div className="w-full h-full rounded-xl bg-gradient-to-br from-neon-blue/20 to-neon-pink/20 flex items-center justify-center">
                                    <img src={user?.avatar_url || user?.avatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${user?.username || 'PlayerOne'}`}
                                        alt="avatar"
                                        className="w-full h-full object-cover rounded-xl" />
                                </div>
                            </div>
                            <div className="absolute -bottom-2 -right-2">
                                <input ref={inputRef} onChange={async (e) => {
                                    const file = e.target.files?.[0];
                                    if (!file) return;
                                    const form = new FormData();
                                    form.append('avatar', file);
                                    try {
                                        setUploading(true);
                                        const res = await UserService.uploadAvatar(form);
                                        const avatarUrl = res?.data?.avatar_url || res?.data?.data?.avatar_url;
                                        if (avatarUrl) {
                                            setUser({ ...user, avatar_url: avatarUrl });
                                        }
                                    } catch (err) {
                                        console.error('Avatar upload failed', err);
                                    } finally {
                                        setUploading(false);
                                        e.target.value = '';
                                    }
                                }} type="file" accept="image/*" id="avatar-upload-input" className="hidden" />
                                <button onClick={() => inputRef.current?.click()} id="avatar-upload-btn" className="p-2 rounded-lg bg-neon-blue text-black hover:scale-110 transition-transform shadow-lg">
                                    <Edit3 size={14} />
                                </button>
                            </div>
                        </div>
                        <div>
                            <h1 className="text-4xl font-black tracking-tighter uppercase mb-2">
                                {user?.username || 'AGENT_ZERO'}
                            </h1>
                            <div className="flex items-center gap-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">
                                <span className="flex items-center gap-1.5"><div className="w-1.5 h-1.5 rounded-full bg-neon-green" /> Online</span>
                                <span className="flex items-center gap-1.5"><div className="w-1.5 h-1.5 rounded-full bg-neon-blue" /> Level {level}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
                {/* Identity Matrix */}
                <section className="bg-dark-surface/30 border border-white/5 rounded-3xl p-8 space-y-8">
                    <h2 className="text-xl font-black flex items-center gap-3">
                        <Shield size={20} className="text-neon-blue" />
                        IDENTITY MATRIX
                    </h2>

                    <div className="space-y-6">
                        {metadata.map((item, i) => (
                            <div key={i} className="flex items-center gap-4 group">
                                <div className="p-3 rounded-xl bg-white/5 border border-white/5 text-gray-500 group-hover:text-neon-blue group-hover:border-neon-blue/20 transition-all">
                                    <item.icon size={18} />
                                </div>
                                <div className="flex flex-col">
                                    <span className="text-[9px] font-black text-gray-500 uppercase tracking-widest">{item.label}</span>
                                    <span className="text-sm font-bold text-gray-300 group-hover:text-white transition-colors">{item.value}</span>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="pt-6 border-t border-white/5 flex flex-wrap gap-2">
                        <button className="flex-1 py-3 bg-white/5 border border-white/10 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-white/10 transition-all flex items-center justify-center gap-2">
                            <Settings size={14} /> Global Config
                        </button>
                        <button className="flex-1 py-3 bg-white/5 border border-white/10 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-white/10 transition-all flex items-center justify-center gap-2">
                            <Key size={14} /> Revoke Keys
                        </button>
                    </div>
                </section>

                {/* Performance & Mastery */}
                <section className="lg:col-span-2 space-y-10">
                    {/* Level Progress */}
                    <div className="bg-dark-surface/40 border border-white/5 rounded-3xl p-8 relative overflow-hidden group">
                        <div className="flex items-center justify-between mb-8">
                            <h2 className="text-xl font-black flex items-center gap-3">
                                <Award size={22} className="text-neon-pink" />
                                NEURAL PROGRESS
                            </h2>
                            <div className="text-right">
                                <div className="text-2xl font-black text-neon-pink tracking-tighter">LVL {level}</div>
                                <div className="text-[10px] font-black text-gray-600 uppercase tracking-widest">{xp} / {nextLevelXp} XP</div>
                            </div>
                        </div>

                        <div className="relative h-4 bg-white/5 rounded-full overflow-hidden border border-white/5 p-0.5">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${xpPercentage}%` }}
                                className="h-full bg-gradient-to-r from-neon-pink to-neon-blue rounded-full shadow-[0_0_15px_rgba(255,0,255,0.3)]"
                            />
                        </div>
                        <div className="mt-4 flex justify-between text-[9px] font-black text-gray-500 uppercase tracking-widest">
                            <span>Sector Mastery: {Math.floor(xpPercentage)}%</span>
                            <span>Synchronizing...</span>
                        </div>
                    </div>

                    {/* Achievements Grid */}
                    <div className="bg-dark-surface/20 border border-white/5 rounded-3xl p-8">
                        <div className="flex items-center justify-between mb-8">
                            <h2 className="text-xl font-black flex items-center gap-3">
                                <Award size={22} className="text-yellow-500" />
                                SYSTEM HONORS
                            </h2>
                            <span className="text-[10px] font-black text-gray-500 uppercase tracking-widest">0 / 42 Collected</span>
                        </div>

                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {[...Array(8)].map((_, i) => (
                                <div key={i} className="aspect-square rounded-2xl bg-white/5 border border-white/5 flex flex-col items-center justify-center gap-2 group hover:border-white/10 transition-all cursor-not-allowed opacity-20 hover:opacity-100">
                                    <div className="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center">
                                        <Award size={20} className="text-gray-600 group-hover:text-yellow-500 transition-colors" />
                                    </div>
                                    <span className="text-[8px] font-black uppercase text-gray-600 tracking-tighter">Locked</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default ProfileRealm;
