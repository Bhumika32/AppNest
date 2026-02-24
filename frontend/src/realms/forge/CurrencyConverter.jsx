import React, { useState } from 'react';
import ToolLayout from '../../layout/Module/ToolLayout.jsx';
import { motion } from 'framer-motion';
import { RefreshCw, ArrowRightLeft } from 'lucide-react';

const CurrencyConverter = ({ module }) => {
    const [amount, setAmount] = useState(1);
    const [from, setFrom] = useState('USD');
    const [to, setTo] = useState('EUR');

    const rates = {
        'USD': 1.0,
        'EUR': 0.92,
        'GBP': 0.79,
        'JPY': 150.23,
        'BITCOIN': 0.000019
    };

    const result = (amount * rates[to] / rates[from]).toFixed(rates[to] > 10 ? 2 : 4);

    return (
        <ToolLayout module={module}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                <div className="space-y-8">
                    <div className="space-y-2">
                        <label className="text-[10px] font-black uppercase tracking-widest text-gray-500 ml-1">Source Amount</label>
                        <input
                            type="number" value={amount} onChange={e => setAmount(e.target.value)}
                            className="w-full bg-white/5 border border-white/10 rounded-2xl p-6 text-2xl font-black text-white focus:border-neon-blue/50 transition-all outline-none"
                        />
                    </div>

                    <div className="flex items-center gap-4">
                        <select
                            value={from} onChange={e => setFrom(e.target.value)}
                            className="bg-white/5 border border-white/10 rounded-2xl p-4 text-xs font-black uppercase flex-1 outline-none"
                        >
                            {Object.keys(rates).map(c => <option key={c} value={c} className="bg-dark-bg">{c}</option>)}
                        </select>
                        <div className="p-3 rounded-full bg-neon-blue/10 border border-neon-blue/20 text-neon-blue">
                            <ArrowRightLeft size={16} />
                        </div>
                        <select
                            value={to} onChange={e => setTo(e.target.value)}
                            className="bg-white/5 border border-white/10 rounded-2xl p-4 text-xs font-black uppercase flex-1 outline-none"
                        >
                            {Object.keys(rates).map(c => <option key={c} value={c} className="bg-dark-bg">{c}</option>)}
                        </select>
                    </div>
                </div>

                <div className="flex flex-col items-center justify-center p-10 bg-black/40 border border-white/10 rounded-[40px] text-center relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-32 h-32 bg-neon-blue/5 blur-3xl -mr-16 -mt-16" />

                    <motion.div
                        key={result}
                        initial={{ y: 10, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        className="text-5xl font-black mb-1 tracking-tighter"
                    >
                        {result}
                    </motion.div>
                    <div className="text-[10px] font-black uppercase tracking-[0.4em] text-neon-blue mb-8">
                        Synced {to} Result
                    </div>

                    <div className="grid grid-cols-2 gap-4 w-full">
                        <div className="p-4 bg-white/5 rounded-2xl border border-white/5 text-left">
                            <div className="text-[8px] font-black text-gray-600 uppercase mb-1">Exchange Logic</div>
                            <div className="text-[10px] font-black">Neural_X_09</div>
                        </div>
                        <div className="p-4 bg-white/5 rounded-2xl border border-white/5 text-left">
                            <div className="text-[8px] font-black text-gray-600 uppercase mb-1">Status</div>
                            <div className="text-[10px] font-black text-neon-green flex items-center gap-1">
                                <span className="w-1.5 h-1.5 rounded-full bg-neon-green animate-pulse" />
                                Optimal
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </ToolLayout>
    );
};

export default CurrencyConverter;
