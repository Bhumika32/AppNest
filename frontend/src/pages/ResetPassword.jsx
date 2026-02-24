import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore.js';
import { Lock, Mail, ChevronRight, Activity, ShieldCheck } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const ResetPassword = () => {
    const location = useLocation();
    const [formData, setFormData] = useState({
        email: location.state?.email || '',
        otp: '',
        newPassword: '',
        confirmPassword: ''
    });

    const { resetPassword, isLoading, error } = useAuthStore();
    const { isDark } = useTheme();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (formData.newPassword !== formData.confirmPassword) {
            useAuthStore.setState({ error: 'Passwords do not match.' });
            return;
        }

        const success = await resetPassword(formData.email, formData.otp, formData.newPassword);
        if (success) {
            navigate('/login', { state: { message: 'Password reset successful. Please login.' } });
        }
    };

    return (
        <div className={`min-h-screen ${isDark ? 'bg-[#05060d] text-slate-100' : 'bg-[#fbf7f0] text-slate-900'} flex items-center justify-center p-4 relative overflow-hidden`}>
            {/* Background */}
            <div className="absolute inset-0 pointer-events-none">
                <div className={`absolute inset-0 ${isDark ? 'bg-gradient-to-b from-[#060719] via-[#040510] to-[#02030a]' : 'bg-gradient-to-b from-[#fff7e8] via-[#fbf7f0] to-[#f6f1ff]'}`} />
            </div>

            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className={`w-full max-w-md ${isDark ? 'bg-white/5' : 'bg-white/70'} backdrop-blur-xl border ${isDark ? 'border-white/10' : 'border-white/20'} p-8 rounded-2xl shadow-2xl relative z-10`}
            >
                <div className="text-center mb-8">
                    <div className={`w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 ${isDark ? 'bg-cyan-500/20' : 'bg-cyan-500/10'}`}>
                        <ShieldCheck className="w-8 h-8 text-cyan-500" />
                    </div>
                    <h1 className={`text-3xl font-bold ${isDark ? 'text-slate-100' : 'text-slate-900'}`}>RESET PROTOCOL</h1>
                    <p className={`${isDark ? 'text-slate-400' : 'text-slate-600'} mt-2 text-sm uppercase tracking-wider`}>Update Identity Credentials</p>
                </div>

                {error && (
                    <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-3 rounded mb-4 text-sm text-center">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="relative">
                        <Mail className={`absolute left-3 top-3 ${isDark ? 'text-slate-500' : 'text-slate-400'} w-5 h-5`} />
                        <input
                            type="email"
                            placeholder="Comms Channel (Email)"
                            className={`w-full ${isDark ? 'bg-black/40 border-white/10 text-white placeholder-slate-500' : 'bg-white/40 border-white/20 text-slate-900 placeholder-slate-600'} border rounded-lg py-3 pl-10 pr-4 focus:outline-none ${isDark ? 'focus:border-violet-500' : 'focus:border-amber-500'}`}
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            required
                        />
                    </div>

                    <div className="relative">
                        <Activity className={`absolute left-3 top-3 ${isDark ? 'text-slate-500' : 'text-slate-400'} w-5 h-5`} />
                        <input
                            type="text"
                            placeholder="OTP CODE"
                            className={`w-full ${isDark ? 'bg-black/40 border-white/10 text-white placeholder-slate-500' : 'bg-white/40 border-white/20 text-slate-900 placeholder-slate-600'} border rounded-lg py-3 pl-10 pr-4 focus:outline-none text-center tracking-widest ${isDark ? 'focus:border-violet-500' : 'focus:border-amber-500'}`}
                            value={formData.otp}
                            onChange={(e) => setFormData({ ...formData, otp: e.target.value })}
                            required
                        />
                    </div>

                    <div className="relative">
                        <Lock className={`absolute left-3 top-3 ${isDark ? 'text-slate-500' : 'text-slate-400'} w-5 h-5`} />
                        <input
                            type="password"
                            placeholder="New Passkey"
                            className={`w-full ${isDark ? 'bg-black/40 border-white/10 text-white placeholder-slate-500' : 'bg-white/40 border-white/20 text-slate-900 placeholder-slate-600'} border rounded-lg py-3 pl-10 pr-4 focus:outline-none ${isDark ? 'focus:border-violet-500' : 'focus:border-amber-500'}`}
                            value={formData.newPassword}
                            onChange={(e) => setFormData({ ...formData, newPassword: e.target.value })}
                            required
                        />
                    </div>

                    <div className="relative">
                        <Lock className={`absolute left-3 top-3 ${isDark ? 'text-slate-500' : 'text-slate-400'} w-5 h-5`} />
                        <input
                            type="password"
                            placeholder="Confirm New Passkey"
                            className={`w-full ${isDark ? 'bg-black/40 border-white/10 text-white placeholder-slate-500' : 'bg-white/40 border-white/20 text-slate-900 placeholder-slate-600'} border rounded-lg py-3 pl-10 pr-4 focus:outline-none ${isDark ? 'focus:border-violet-500' : 'focus:border-amber-500'}`}
                            value={formData.confirmPassword}
                            onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                            required
                        />
                    </div>

                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className={`w-full ${isDark ? 'bg-gradient-to-r from-emerald-600 to-cyan-500' : 'bg-gradient-to-r from-emerald-500 to-blue-500'} text-white font-bold py-3 rounded-lg hover:opacity-90 transition-opacity`}
                        disabled={isLoading}
                    >
                        {isLoading ? 'RESTRICTING ACCESS...' : 'APPLY NEW CREDENTIALS'}
                    </motion.button>
                </form>

                <div className={`mt-6 text-center text-xs ${isDark ? 'text-slate-400' : 'text-slate-600'}`}>
                    Didn't get an OTP? <Link to="/forgot-password" className="text-violet-400 hover:text-white transition-colors">Resend Request</Link>
                </div>
            </motion.div>
        </div>
    );
};

export default ResetPassword;
