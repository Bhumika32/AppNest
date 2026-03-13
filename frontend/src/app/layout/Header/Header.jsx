import React from 'react';
import { motion } from 'framer-motion';
import { Search, Command, Activity, Shield } from 'lucide-react';
import { useAuthStore } from '../../../store/authStore.js';
import { useUserStore } from '../../../store/userStore.js';
import { useUIStore } from '../../../store/uiStore.js';
import { USER_REALMS, ADMIN_REALMS } from '../../realmConstants.js';
import NotificationPanel from '../../../components/NotificationPanel.jsx';

const Header = () => {
    const user = useAuthStore(state => state.user);
    const role = useAuthStore(state => state.role);
    const xp = useUserStore(state => state.xp);
    const level = useUserStore(state => state.level);
    const nextLevelXp = useUserStore(state => state.nextLevelXp);
    const title = useUserStore(state => state.title);
    const currentRealm = useUIStore(state => state.currentRealm);
    const isDashboardLoading = useUserStore(state => state.isLoading);

    const activeRealm = [...USER_REALMS, ...ADMIN_REALMS].find(r => r.id === currentRealm);

    return (
        <header className="h-20 border-b border-white/10 bg-dark-bg/40 backdrop-blur-md flex items-center justify-between px-8 sticky top-0 z-50 overflow-hidden">
            {/* Left: Realm Info */}
            <div className="flex flex-col">
                <h2 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
                    {activeRealm?.icon && <activeRealm.icon size={18} className="text-neon-blue" />}
                    {activeRealm?.label || 'Gateway'}
                </h2>
                <span className="text-[10px] text-gray-500 uppercase tracking-[0.2em]">
                    Sector: {currentRealm?.replace('admin-', '') || 'unknown'}
                </span>
            </div>

            {/* Center: Search */}
            <div className="hidden lg:flex items-center bg-white/5 rounded-full px-4 py-1.5 border border-white/10 w-96 group focus-within:border-neon-blue/50 transition-all">
                <Search size={16} className="text-gray-500 group-focus-within:text-neon-blue transition-colors" />
                <input
                    type="text"
                    placeholder="Search realms, tools, or users..."
                    className="bg-transparent border-none focus:ring-0 text-sm ml-2 w-full text-gray-300 placeholder:text-gray-600 outline-none"
                />
                <div className="flex items-center gap-1 border border-white/20 px-1.5 rounded bg-white/5">
                    <Command size={10} className="text-gray-500" />
                    <span className="text-[10px] text-gray-500">K</span>
                </div>
            </div>

            {/* Right */}
            <div className="flex items-center gap-6">
                {role === 'admin' ? (
                    /* ── Admin Header ─────────────────────────── */
                    <div className="flex items-center gap-4">
                        <div className="flex flex-col items-end">
                            <div className="flex items-center gap-2 text-[10px] text-neon-green font-black bg-neon-green/10 px-2 py-0.5 rounded border border-neon-green/20">
                                <Activity size={12} />
                                CORE OPTIMAL
                            </div>
                            <span className="text-[10px] text-gray-500 mt-1 uppercase font-bold tracking-tighter">
                                12,402 Active Sessions
                            </span>
                        </div>
                        <div className="h-8 w-px bg-white/10 mx-2" />
                        <div className="flex items-center gap-3 text-gray-400">
                            <div className="relative">
                                <Shield size={20} />
                                <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse" />
                            </div>
                            <NotificationPanel />
                        </div>
                    </div>
                ) : (
                    /* ── User Header ──────────────────────────── */
                    <div className="flex items-center gap-6">
                        {/* XP Progress Bar */}
                        <div className="hidden sm:flex flex-col items-end">
                            <div className="flex items-center gap-2 mb-1">
                                <span className="text-[10px] font-black text-gray-400">LVL {level}</span>
                                <div className="w-32 h-1 bg-white/10 rounded-full overflow-hidden border border-white/5">
                                    <motion.div
                                        initial={{ width: 0 }}
                                        animate={{ width: `${Math.min(100, (xp / nextLevelXp) * 100)}%` }}
                                        transition={{ duration: 0.8, ease: 'easeOut' }}
                                        className="h-full bg-gradient-to-r from-neon-blue to-neon-pink"
                                    />
                                </div>
                            </div>
                            <span className="text-[10px] text-gray-500 uppercase font-black tracking-widest">
                                {xp} / {nextLevelXp} XP
                            </span>
                        </div>

                        {/* 🔔 Notification Bell */}
                        <NotificationPanel />

                        {/* Profile */}
                        <div className="flex items-center gap-3 pl-4 border-l border-white/10">
                            <div className="flex flex-col items-end">
                                <span className="text-sm font-black text-white leading-tight">
                                    {user?.username || 'PLAYER_ONE'}
                                </span>
                                <span className="text-[10px] text-neon-blue uppercase font-black tracking-tighter">
                                    {title}
                                </span>
                            </div>
                            {/* Settings accessible from sidebar; header button removed to avoid duplication */}
                            <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-neon-blue/20 to-neon-pink/20 border border-white/10 overflow-hidden group cursor-pointer">
                                <img
                                    src={user?.avatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${user?.username || 'PlayerOne'}`}
                                    alt="avatar"
                                    className="w-full h-full object-cover group-hover:scale-110 transition-transform"
                                />
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </header>
    );
};

export default Header;
