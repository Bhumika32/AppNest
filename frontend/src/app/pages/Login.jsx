import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore.js';
import { Lock, Mail, ChevronRight } from 'lucide-react';
import api from '../../api/apiClient';
import { useTheme } from '../../context/ThemeContext';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login, isLoading, error } = useAuthStore();
    const { isDark, setTheme } = useTheme();
    const navigate = useNavigate();

    const [connectionStatus, setConnectionStatus] = useState('checking');

    useEffect(() => {
        const checkConnection = async () => {
            try {
                await api.options('/auth/login');
                setConnectionStatus('connected');
            } catch (err) {
                console.error("Connectivity Check Failed:", err);
                setConnectionStatus('error');
            }
        };
        checkConnection();
    }, []);

    // Apply welcome theme if set (persisted by welcome page)
    useEffect(() => {
        try {
            const saved = localStorage.getItem('appnest-theme');
            if (saved) setTheme(saved);
        } catch (e) {
            // ignore
        }
    }, [setTheme]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const success = await login(email, password);
        if (success) {
            // ✅ Professional: Redirect admin users to admin dashboard
            // Wait a tick to ensure store is updated after login
            setTimeout(() => {
                const authState = useAuthStore.getState();
                console.log('[Login] User role:', authState.role);  // Debug log
                const dashboardPath = authState.role === 'admin' ? '/dashboard/admin' : '/dashboard';
                console.log('[Login] Redirecting to:', dashboardPath);
                navigate(dashboardPath);
            }, 0);
        }
    };

    return (
        <div className={`min-h-screen ${isDark ? 'bg-[#05060d] text-slate-100' : 'bg-[#fbf7f0] text-slate-900'} flex items-center justify-center p-4 relative overflow-hidden`}>
            {/* Background */}
            <div className="absolute inset-0 pointer-events-none">
                {isDark ? (
                    <>
                        <div className="absolute inset-0 bg-gradient-to-b from-[#060719] via-[#040510] to-[#02030a]" />
                        <div className="absolute -top-32 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-gradient-to-br from-violet-500/25 via-fuchsia-500/12 to-cyan-400/10 blur-3xl" />
                    </>
                ) : (
                    <>
                        <div className="absolute inset-0 bg-gradient-to-b from-[#fff7e8] via-[#fbf7f0] to-[#f6f1ff]" />
                        <div className="absolute -top-40 -left-40 h-[520px] w-[520px] rounded-full bg-gradient-to-br from-amber-200/70 via-rose-200/50 to-fuchsia-200/40 blur-3xl" />
                    </>
                )}
            </div>

            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                className={`w-full max-w-md ${isDark ? 'bg-dark-surface/50' : 'bg-white/70'} backdrop-blur-xl border ${isDark ? 'border-white/10' : 'border-white/20'} p-8 rounded-2xl shadow-2xl relative z-10`}
            >
                <div className="text-center mb-8">
                    <motion.h1
                        initial={{ y: -20 }}
                        animate={{ y: 0 }}
                        className={`text-4xl font-bold bg-clip-text text-transparent ${isDark ? 'bg-gradient-to-r from-violet-400 to-cyan-300' : 'bg-gradient-to-r from-amber-500 to-rose-500'}`}
                    >
                        SYSTEM ACCESS
                    </motion.h1>
                    <p className={`${isDark ? 'text-slate-400' : 'text-slate-600'} mt-2 text-sm tracking-wider`}>SECURE LOGIN REQUIRED</p>
                </div>

                {error && (
                    <motion.div
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        className={`bg-red-500/10 border ${isDark ? 'border-red-500/50' : 'border-red-400'} text-red-500 p-3 rounded mb-4 text-sm text-center font-bold`}
                    >
                        {error}
                    </motion.div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                        <label className={`text-xs ${isDark ? 'text-slate-400' : 'text-slate-600'} uppercase tracking-widest pl-1`}>Identifier</label>
                        <div className="relative">
                            <Mail className={`absolute left-3 top-1/2 -translate-y-1/2 ${isDark ? 'text-slate-500' : 'text-slate-400'} w-5 h-5`} />
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className={`w-full ${isDark ? 'bg-black/40 border-white/10 focus:border-violet-500 focus:ring-violet-500' : 'bg-white/40 border-white/20 focus:border-amber-500 focus:ring-amber-500'} border rounded-lg py-3 pl-10 pr-4 ${isDark ? 'text-white' : 'text-slate-900'} focus:outline-none focus:ring-1 transition-all`}
                                placeholder="user@appnest.io"
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className={`text-xs ${isDark ? 'text-slate-400' : 'text-slate-600'} uppercase tracking-widest pl-1`}>Passkey</label>
                        <div className="relative">
                            <Lock className={`absolute left-3 top-1/2 -translate-y-1/2 ${isDark ? 'text-slate-500' : 'text-slate-400'} w-5 h-5`} />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className={`w-full ${isDark ? 'bg-black/40 border-white/10 focus:border-violet-500 focus:ring-violet-500' : 'bg-white/40 border-white/20 focus:border-amber-500 focus:ring-amber-500'} border rounded-lg py-3 pl-10 pr-4 ${isDark ? 'text-white' : 'text-slate-900'} focus:outline-none focus:ring-1 transition-all`}
                                placeholder="••••••••"
                                required
                            />
                        </div>
                    </div>

                    <div className="flex justify-end">
                        <Link to="/forgot-password" className={`text-xs ${isDark ? 'text-violet-400 hover:text-white' : 'text-amber-600 hover:text-slate-900'} transition-colors`}>
                            Forgot Passkey?
                        </Link>
                    </div>

                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        disabled={isLoading}
                        className={`w-full ${isDark ? 'bg-gradient-to-r from-violet-600 to-cyan-500 text-white' : 'bg-gradient-to-r from-amber-500 to-rose-500 text-white'} font-bold py-3 rounded-lg flex items-center justify-center gap-2 ${isDark ? 'hover:from-violet-700 hover:to-cyan-600' : 'hover:from-amber-600 hover:to-rose-600'} transition-colors disabled:opacity-50 disabled:cursor-not-allowed`}
                    >
                        {isLoading ? 'AUTHENTICATING...' : (
                            <>
                                ACCESS CORE <ChevronRight className="w-4 h-4" />
                            </>
                        )}
                    </motion.button>
                </form>

                <div className={`mt-6 text-center text-sm ${isDark ? 'text-slate-400' : 'text-slate-600'}`}>
                    New Operator? <Link to="/signup" className={`${isDark ? 'text-violet-400 hover:text-white' : 'text-amber-600 hover:text-slate-900'} transition-colors`}>Initialize Protocol</Link>
                </div>
            </motion.div>
        </div>
    );
};

export default Login;
