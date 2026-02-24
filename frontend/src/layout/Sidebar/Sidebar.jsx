import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Settings, Moon, Sun, LogOut, ChevronLeft, ChevronRight } from 'lucide-react';
import { useAuthStore } from '../../store/authStore.js';
import { useRealmStore } from '../../store/realmStore.js';
import { useTheme } from '../../context/ThemeContext.jsx';
import { USER_REALMS, ADMIN_REALMS } from '../../app/realmConstants.js';
//import Settings from "../pages/Settings"

const NavItem = ({ realm, isSidebarCollapsed, currentRealm, setCurrentRealm, navigate, location }) => {
    const isActive = location.pathname.startsWith(realm.path) || currentRealm === realm.id;
    const Icon = realm.icon;

    return (
        <motion.div
            whileHover={{ x: 4 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
                setCurrentRealm(realm.id);
                navigate(realm.path);
            }}
            className={`relative flex items-center p-3 mb-2 cursor-pointer rounded-lg transition-all duration-300
                ${isActive
                    ? 'bg-neon-blue/20 text-neon-blue shadow-[0_0_15px_rgba(0,243,255,0.3)]'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
        >
            <Icon size={20} className={isActive ? 'drop-shadow-[0_0_5px_rgba(0,243,255,1)]' : ''} />
            {!isSidebarCollapsed && (
                <motion.span
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="ml-3 font-medium whitespace-nowrap"
                >
                    {realm.label}
                </motion.span>
            )}
            {isActive && (
                <motion.div
                    layoutId="activeGlow"
                    className="absolute left-0 w-1 h-2/3 bg-neon-blue rounded-r-full"
                />
            )}
        </motion.div>
    );
};

const Sidebar = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { role, logout } = useAuthStore();
    const { isSidebarCollapsed, toggleSidebar, currentRealm, setCurrentRealm } = useRealmStore();
    const { isDark, toggleTheme } = useTheme();

    const navProps = { isSidebarCollapsed, currentRealm, setCurrentRealm, navigate, location };

    return (
        <motion.aside
            animate={{ width: isSidebarCollapsed ? 80 : 260 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className="h-screen bg-dark-surface border-r border-white/10 flex flex-col relative z-50 flex-shrink-0"
        >
            {/* Logo */}
            <div className="p-6 flex items-center justify-between">
                {!isSidebarCollapsed && (
                    <motion.h1
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="text-2xl font-black bg-gradient-to-r from-neon-blue to-neon-pink bg-clip-text text-transparent italic"
                    >
                        APPNEST
                    </motion.h1>
                )}
                <button
                    onClick={toggleSidebar}
                    className="p-1.5 rounded-md hover:bg-white/10 text-gray-400 transition-colors"
                >
                    {isSidebarCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
                </button>
            </div>

            {/* Nav Items */}
            <div className="flex-1 overflow-y-auto px-4 py-2 scrollbar-none">
                {/* User Realms */}
                <div className="mb-4">
                    <p className={`text-[10px] uppercase tracking-widest text-gray-500 mb-4 px-3 ${isSidebarCollapsed ? 'text-center' : ''}`}>
                        {isSidebarCollapsed ? '---' : 'Realms'}
                    </p>
                    {USER_REALMS.map(realm => (
                        <NavItem key={realm.id} realm={realm} {...navProps} />
                    ))}
                </div>

                {/* Admin Section */}
                {role === 'admin' && (
                    <div className="mt-8 mb-4">
                        <p className={`text-[10px] uppercase tracking-widest text-neon-pink mb-4 px-3 ${isSidebarCollapsed ? 'text-center' : ''}`}>
                            {isSidebarCollapsed ? '!!!' : 'Control Center'}
                        </p>
                        {ADMIN_REALMS.map(realm => (
                            <NavItem key={realm.id} realm={realm} {...navProps} />
                        ))}
                    </div>
                )}
            </div>

            {/* Bottom Actions */}
            <div className="p-4 border-t border-white/5 space-y-1">
                <div
                    onClick={() => navigate('/settings')}
                    className="flex items-center p-3 cursor-pointer text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-all"
                >
                    <Settings size={20} />
                    {!isSidebarCollapsed && <span className="ml-3 font-medium">Settings</span>}
                </div>
                <div
                    onClick={toggleTheme}
                    className="flex items-center p-3 cursor-pointer text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-all"
                >
                    {isDark ? <Sun size={20} className="text-yellow-400" /> : <Moon size={20} />}
                    {!isSidebarCollapsed && <span className="ml-3 font-medium">{isDark ? 'Light' : 'Dark'} Mode</span>}
                </div>
                <div
                    onClick={() => { logout(); navigate('/'); }}
                    className="flex items-center p-3 cursor-pointer text-red-500 hover:bg-red-500/10 rounded-lg transition-all"
                >
                    <LogOut size={20} />
                    {!isSidebarCollapsed && <span className="ml-3 font-medium">Logout</span>}
                </div>
            </div>
        </motion.aside>
    );
};

export default Sidebar;
