import React, { useState } from 'react';

const rates = {
    USD: 1, EUR: 0.92, GBP: 0.79, INR: 83.12, JPY: 149.50, AUD: 1.53, CAD: 1.35
};

const CurrencyConverter = ({ showSystemDialog, completeTool }) => {
    const [amount, setAmount] = useState('100');
    const [from, setFrom] = useState('USD');
    const [to, setTo] = useState('EUR');
    const [result, setResult] = useState(null);

    const handleConvert = () => {
        if (!amount || isNaN(amount)) {
            showSystemDialog('TOOL_ERROR', 'error');
            return;
        }

        const base = parseFloat(amount) / rates[from];
        const converted = (base * rates[to]).toFixed(2);
        setResult(converted);

        completeTool({
            duration: 10,
            score: 50,
            metadata: { from, to, amount, result: converted },
            eventCategory: 'TOOL_SUCCESS'
        });
    };

    return (
        <div className="space-y-6 text-white max-w-sm mx-auto">
            <h3 className="text-xl font-black uppercase tracking-widest text-center mb-8">Exchange <span className="text-neon-blue">Matrix</span></h3>
            
            <div className="space-y-4">
                <div>
                    <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">Amount</label>
                    <input 
                        type="number" 
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold focus:border-neon-blue focus:outline-none transition-colors"
                    />
                </div>
                
                <div className="flex gap-4">
                    <div className="flex-1">
                        <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">From</label>
                        <select 
                            value={from} 
                            onChange={(e) => setFrom(e.target.value)}
                            className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold focus:border-neon-pink focus:outline-none transition-colors appearance-none"
                        >
                            {Object.keys(rates).map(c => <option key={c} value={c}>{c}</option>)}
                        </select>
                    </div>
                    <div className="flex-1">
                        <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">To</label>
                        <select 
                            value={to} 
                            onChange={(e) => setTo(e.target.value)}
                            className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold focus:border-neon-blue focus:outline-none transition-colors appearance-none"
                        >
                            {Object.keys(rates).map(c => <option key={c} value={c}>{c}</option>)}
                        </select>
                    </div>
                </div>
            </div>

            <button 
                onClick={handleConvert}
                className="w-full py-4 mt-8 bg-white/5 border border-white/20 rounded-xl font-black uppercase tracking-widest hover:bg-white/10 hover:border-neon-pink transition-all"
            >
                Convert Variables
            </button>

            {result && (
                <div className="mt-8 p-6 bg-neon-pink/10 border border-neon-pink/30 rounded-xl text-center">
                    <span className="text-xs font-black uppercase tracking-widest text-gray-400">Converted Output</span>
                    <div className="text-4xl font-black text-neon-pink mt-2 drop-shadow-[0_0_10px_rgba(255,0,128,0.5)]">
                        {result} <span className="text-sm opacity-50">{to}</span>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CurrencyConverter;
