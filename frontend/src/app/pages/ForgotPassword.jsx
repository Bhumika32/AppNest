import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore.js';
import { Mail, ChevronRight, Activity, ArrowLeft } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [submitted, setSubmitted] = useState(false);
    const { forgotPassword, isLoading, error, clearError } = useAuthStore();
    const { isDark } = useTheme();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const success = await forgotPassword(email);
        if (success) {
            setSubmitted(true);
            setTimeout(() => {
                navigate('/reset-password', { state: { email } });
            }, 2000);
        }
    };

    return (
        <div className={`min-h-screen ${isDark ? 'bg-[#05060d] text-slate-100' : 'bg-[#fbf7f0] text-slate-900'} flex items-center justify-center p-4 relative overflow-hidden`}>
            {/* Background */}
            <div className="absolute inset-0 pointer-events-none">
                <div className={`absolute inset-0 ${isDark ? 'bg-gradient-to-b from-[#060719] via-[#040510] to-[#02030a]' : 'bg-gradient-to-b from-[#fff7e8] via-[#fbf7f0] to-[#f6f1ff]'}`} />
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`w-full max-w-md ${isDark ? 'bg-white/5' : 'bg-white/70'} backdrop-blur-xl border ${isDark ? 'border-white/10' : 'border-white/20'} p-8 rounded-2xl shadow-2xl relative z-10`}
            >
                <Link to="/login" className={`inline-flex items-center text-xs ${isDark ? 'text-slate-400 hover:text-white' : 'text-slate-600 hover:text-slate-900'} mb-6 transition-colors`}>
                    <ArrowLeft className="w-3 h-3 mr-1" /> BACK TO LOGIN
                </Link>

                <div className="text-center mb-8">
                    <h1 className={`text-3xl font-bold ${isDark ? 'text-slate-100' : 'text-slate-900'}`}>RECOVERY MODE</h1>
                    <p className={`${isDark ? 'text-slate-400' : 'text-slate-600'} mt-2 text-sm uppercase tracking-wider`}>Initiate Identity Restoration</p>
                </div>

                {error && (
                    <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-3 rounded mb-4 text-sm text-center">
                        {error}
                    </div>
                )}

                {submitted ? (
                    <div className="text-center py-8">
                        <div className={`w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 ${isDark ? 'bg-emerald-500/20' : 'bg-emerald-500/10'}`}>
                            <Activity className="w-8 h-8 text-emerald-500" />
                        </div>
                        <p className={`${isDark ? 'text-slate-300' : 'text-slate-700'}`}>If an account exists, a recovery code has been transmitted.</p>
                        <p className="text-xs text-slate-500 mt-4 uppercase">Redirecting to Reset Module...</p>
                    </div>
                ) : (
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="relative">
                            <Mail className={`absolute left-3 top-3 ${isDark ? 'text-slate-500' : 'text-slate-400'} w-5 h-5`} />
                            <input
                                type="email"
                                placeholder="Comms Channel (Email)"
                                className={`w-full ${isDark ? 'bg-black/40 border-white/10 text-white placeholder-slate-500' : 'bg-white/40 border-white/20 text-slate-900 placeholder-slate-600'} border rounded-lg py-3 pl-10 pr-4 focus:outline-none ${isDark ? 'focus:border-violet-500' : 'focus:border-amber-500'}`}
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <motion.button
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            className={`w-full ${isDark ? 'bg-gradient-to-r from-violet-600 to-cyan-500' : 'bg-gradient-to-r from-amber-500 to-rose-500'} text-white font-bold py-3 rounded-lg hover:opacity-90 transition-opacity flex items-center justify-center`}
                            disabled={isLoading}
                        >
                            {isLoading ? 'SEARCHING...' : (
                                <>
                                    TRANSMIT OTP <ChevronRight className="w-4 h-4 ml-2" />
                                </>
                            )}
                        </motion.button>
                    </form>
                )}
            </motion.div>
        </div>
    );
};

export default ForgotPassword;
