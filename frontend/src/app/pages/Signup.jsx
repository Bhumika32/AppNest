import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore.js';
import { User, Lock, Mail, ChevronRight, Activity } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

const Signup = () => {
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({ username: '', email: '', password: '' });
    const [otp, setOtp] = useState('');

    const { register, verifyOtp, isLoading, error } = useAuthStore();
    const { isDark, setTheme } = useTheme();
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        const success = await register(formData.username, formData.email, formData.password);
        if (success) setStep(2);
    };

    const handleVerify = async (e) => {
        e.preventDefault();
        const success = await verifyOtp(formData.email, otp);
        if (success) navigate('/login');
    };

    // Apply welcome theme if present
    React.useEffect(() => {
        try {
            const saved = localStorage.getItem('appnest-theme');
            if (saved) setTheme(saved);
        } catch (e) { }
    }, [setTheme]);

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
                className={`w-full max-w-md ${isDark ? 'bg-white/5' : 'bg-white/70'} backdrop-blur-xl border ${isDark ? 'border-white/10' : 'border-white/20'} p-8 rounded-2xl shadow-2xl relative z-10`}
            >
                <div className="text-center mb-8">
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className={`w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 ${isDark ? 'bg-violet-600/20' : 'bg-amber-500/20'}`}
                    >
                        <Activity className={`w-8 h-8 ${isDark ? 'text-violet-400' : 'text-amber-600'}`} />
                    </motion.div>
                    <h1 className={`text-3xl font-bold ${isDark ? 'text-slate-100' : 'text-slate-900'}`}>INITIALIZE PROTOCOL</h1>
                    <p className={`${isDark ? 'text-slate-400' : 'text-slate-600'} mt-2 text-sm`}>CREATE NEW OPERATOR IDENTITY</p>
                </div>

                {error && (
                    <div className={`bg-red-500/10 border border-red-500/50 text-red-500 p-3 rounded mb-4 text-sm text-center`}>
                        {error}
                    </div>
                )}

                {step === 1 ? (
                    <form onSubmit={handleRegister} className="space-y-4">
                        <div className="relative">
                            <User className={`absolute left-3 top-3 ${isDark ? 'text-slate-500' : 'text-slate-400'} w-5 h-5`} />
                            <input
                                type="text"
                                placeholder="Codename"
                                className={`w-full ${isDark ? 'bg-black/40 border-white/10 text-white placeholder-slate-500' : 'bg-white/40 border-white/20 text-slate-900 placeholder-slate-600'} border rounded-lg py-3 pl-10 pr-4 focus:outline-none ${isDark ? 'focus:border-violet-500' : 'focus:border-amber-500'}`}
                                value={formData.username}
                                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                                required
                            />
                        </div>
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
                            <Lock className={`absolute left-3 top-3 ${isDark ? 'text-slate-500' : 'text-slate-400'} w-5 h-5`} />
                            <input
                                type="password"
                                placeholder="Passkey"
                                className={`w-full ${isDark ? 'bg-black/40 border-white/10 text-white placeholder-slate-500' : 'bg-white/40 border-white/20 text-slate-900 placeholder-slate-600'} border rounded-lg py-3 pl-10 pr-4 focus:outline-none ${isDark ? 'focus:border-violet-500' : 'focus:border-amber-500'}`}
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                required
                            />
                        </div>
                        <motion.button
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            className={`w-full ${isDark ? 'bg-gradient-to-r from-violet-600 to-cyan-500' : 'bg-gradient-to-r from-amber-500 to-rose-500'} text-white font-bold py-3 rounded-lg hover:opacity-90 transition-opacity`}
                            disabled={isLoading}
                        >
                            {isLoading ? 'PROCESSING...' : 'INITIATE REGISTRATION'}
                        </motion.button>
                    </form>
                ) : (
                    <form onSubmit={handleVerify} className="space-y-4">
                        <p className={`text-center text-sm ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>Enter the verification code sent to your email.</p>
                        <input
                            type="text"
                            placeholder="OTP CODE"
                            className={`w-full ${isDark ? 'bg-black/40 border-white/10 text-white placeholder-slate-500' : 'bg-white/40 border-white/20 text-slate-900 placeholder-slate-600'} border rounded-lg py-3 text-center text-2xl tracking-widest focus:outline-none ${isDark ? 'focus:border-violet-500' : 'focus:border-amber-500'}`}
                            value={otp}
                            onChange={(e) => setOtp(e.target.value)}
                            required
                        />
                        <motion.button
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            className={`w-full ${isDark ? 'bg-gradient-to-r from-emerald-600 to-cyan-500' : 'bg-gradient-to-r from-emerald-500 to-blue-500'} text-white font-bold py-3 rounded-lg hover:opacity-90 transition-opacity`}
                            disabled={isLoading}
                        >
                            {isLoading ? 'VERIFYING...' : 'CONFIRM IDENTITY'}
                        </motion.button>

                        <button
                            type="button"
                            onClick={async () => {
                                await useAuthStore.getState().resendOtp(formData.email);
                            }}
                            className={`w-full text-xs ${isDark ? 'text-slate-400 hover:text-violet-400' : 'text-slate-600 hover:text-amber-600'} transition-colors mt-2`}
                        >
                            Resend Code
                        </button>
                    </form>
                )}

                <div className={`mt-6 text-center text-sm ${isDark ? 'text-slate-400' : 'text-slate-600'}`}>
                    Already operational? <Link to="/login" className={`${isDark ? 'text-violet-400 hover:text-white' : 'text-amber-600 hover:text-slate-900'} transition-colors`}>System Access</Link>
                </div>
            </motion.div>
        </div>
    );
};

export default Signup;
