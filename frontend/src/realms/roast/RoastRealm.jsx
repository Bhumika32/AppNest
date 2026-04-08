import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Flame, Target, MessageSquare, History, ShieldAlert } from 'lucide-react';
import { RoastService } from '../../api/api';

const RoastRealm = () => {
    const [roastType, setRoastType] = useState('normal');
    const [name, setName] = useState('');
    const [roasts, setRoasts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const generateRoast = async () => {
        setError('');
        setLoading(true);
        try {
            let response;
            switch (roastType) {
                case 'normal': response = await RoastService.getNormal(); break;
                case 'personal':
                    if (!name.trim()) {
                        setError('TARGET IDENTITY REQUIRED');
                        setLoading(false);
                        return;
                    }
                    response = await RoastService.getPersonal(name);
                    break;
                case 'ultra': response = await RoastService.getUltra(); break;
                case 'random': response = await RoastService.getRandom(); break;
                default: response = await RoastService.getNormal();
            }
            setRoasts([{ roast: response.data.roast, type: roastType, timestamp: new Date() }, ...roasts.slice(0, 4)]);
        } catch (err) {
            setError(err.response?.data?.error || 'NEURAL LINK TIMEOUT');
        } finally {
            setLoading(false);
        }
    };

    const types = [
        { id: 'normal', label: 'SYSTEM_ERROR', icon: MessageSquare, color: 'neon-blue' },
        { id: 'personal', label: 'TARGET_SYNC', icon: Target, color: 'neon-pink' },
        { id: 'ultra', label: 'CRITICAL_BURN', icon: Flame, color: 'orange-500' },
        { id: 'random', label: 'CHAOS_MODE', icon: Zap, color: 'neon-green' },
    ];

    return (
        <div className="space-y-10 pb-20">
            {/* Header */}
            <header className="relative p-10 rounded-3xl overflow-hidden bg-dark-surface/30 border border-white/5">
                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-neon-green/5 blur-[100px] -mr-40 -mt-40 rounded-full" />
                <div className="relative z-10 flex flex-col md:flex-row items-center gap-10">
                    <div className="p-5 rounded-2xl bg-neon-green/10 border border-neon-green/20 text-neon-green animate-pulse">
                        <Flame size={48} />
                    </div>
                    <div>
                        <h1 className="text-5xl font-black mb-3 tracking-tighter uppercase">ROAST <span className="text-neon-green">ARENA</span></h1>
                        <p className="text-gray-400 max-w-xl text-sm leading-relaxed font-medium">
                            Execute verbal sub-routines against yourself or targets. Our AI models are trained on high-entropy humor and critical banter logic.
                        </p>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
                {/* Control Panel */}
                <section className="bg-dark-surface/40 border border-white/5 rounded-3xl p-8 backdrop-blur-md">
                    <h2 className="text-xl font-black mb-8 flex items-center gap-3">
                        <ShieldAlert size={22} className="text-neon-pink" />
                        BANTER PARAMETERS
                    </h2>

                    <div className="space-y-8">
                        <div className="grid grid-cols-2 gap-4">
                            {types.map((t) => (
                                <button
                                    key={t.id}
                                    onClick={() => setRoastType(t.id)}
                                    className={`p-4 rounded-xl border transition-all flex flex-col items-center gap-2 group ${roastType === t.id
                                        ? `bg-${t.color}/10 border-${t.color}/30 text-${t.color}`
                                        : 'bg-white/5 border-white/5 text-gray-500 hover:border-white/10'
                                        }`}
                                >
                                    <t.icon size={20} className={roastType === t.id ? 'animate-bounce' : 'group-hover:text-white'} />
                                    <span className="text-[10px] font-black tracking-widest uppercase">{t.label}</span>
                                </button>
                            ))}
                        </div>

                        {roastType === 'personal' && (
                            <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} className="space-y-3">
                                <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest">Target Neural Signature (Name)</label>
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    placeholder="Enter subject name..."
                                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-neon-pink/50 transition-all font-bold"
                                />
                            </motion.div>
                        )}

                        {error && (
                            <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-500 text-[10px] font-black uppercase tracking-widest rounded-xl flex items-center gap-2">
                                <ShieldAlert size={14} /> {error}
                            </div>
                        )}

                        <button
                            onClick={generateRoast}
                            disabled={loading}
                            className={`w-full py-4 rounded-xl font-black uppercase tracking-tighter transition-all shadow-lg ${loading
                                ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
                                : 'bg-neon-green text-black hover:shadow-[0_0_30px_rgba(57,255,20,0.4)] active:scale-95'
                                }`}
                        >
                            {loading ? 'CALCULATING BANTER...' : '⚡ EXECUTE ROAST'}
                        </button>
                    </div>
                </section>

                {/* History/Output */}
                <section className="bg-dark-surface/20 border border-white/5 rounded-3xl p-8 relative overflow-hidden group">
                    <h2 className="text-xl font-black mb-8 flex items-center gap-3">
                        <History size={22} className="text-neon-blue" />
                        OUTPUT FEED
                    </h2>

                    <div className="space-y-4">
                        <AnimatePresence mode="popLayout">
                            {roasts.map((r, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, x: 20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -20 }}
                                    className="bg-white/5 border-l-4 border-neon-green rounded-r-xl p-5 relative group"
                                >
                                    <p className="text-neon-green text-sm font-bold italic leading-relaxed mb-3">"{r.roast}"</p>
                                    <div className="flex justify-between items-center text-[8px] font-black text-gray-600 uppercase tracking-widest">
                                        <span>Type: {r.type}</span>
                                        <span>{r.timestamp.toLocaleTimeString()}</span>
                                    </div>
                                </motion.div>
                            ))}
                        </AnimatePresence>
                        {roasts.length === 0 && !loading && (
                            <div className="h-64 flex flex-col items-center justify-center text-gray-600 border-2 border-dashed border-white/5 rounded-2xl">
                                <MessageSquare size={32} className="mb-4 opacity-20" />
                                <span className="text-[10px] font-black uppercase tracking-[0.3em]">Stand-by for injection</span>
                            </div>
                        )}
                        {loading && (
                            <div className="animate-pulse space-y-4">
                                <div className="h-24 bg-white/5 rounded-xl" />
                                <div className="h-24 bg-white/5 rounded-xl opacity-50" />
                            </div>
                        )}
                    </div>
                </section>
            </div>
        </div>
    );
};

export default RoastRealm;
