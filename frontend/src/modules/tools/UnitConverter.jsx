import React, { useState } from 'react';

const units = {
    Length: { m: 1, km: 0.001, cm: 100, mm: 1000, in: 39.37, ft: 3.28 },
    Weight: { kg: 1, g: 1000, mg: 1000000, lb: 2.204, oz: 35.27 },
};

const UnitConverter = ({ showSystemDialog, completeTool }) => {
    const [category, setCategory] = useState('Length');
    const [amount, setAmount] = useState('1');
    const [from, setFrom] = useState('m');
    const [to, setTo] = useState('ft');
    const [result, setResult] = useState(null);

    const handleCategoryChange = (e) => {
        const cat = e.target.value;
        setCategory(cat);
        const firstUnit = Object.keys(units[cat])[0];
        const secondUnit = Object.keys(units[cat])[1];
        setFrom(firstUnit);
        setTo(secondUnit);
        setResult(null);
    };

    const handleConvert = () => {
        if (!amount || isNaN(amount)) {
            showSystemDialog('TOOL_ERROR', 'error');
            return;
        }

        const base = parseFloat(amount) / units[category][from];
        const converted = (base * units[category][to]).toFixed(4);
        setResult(converted);

        completeTool({
            duration: 5,
            score: 50,
            metadata: { category, from, to, amount, result: converted },
            eventCategory: 'TOOL_SUCCESS'
        });
    };

    return (
        <div className="space-y-6 text-white max-w-sm mx-auto">
            <h3 className="text-xl font-black uppercase tracking-widest text-center mb-8">Metric <span className="text-neon-pink">Transformer</span></h3>
            
            <div className="space-y-4">
                <div>
                    <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">Dimension</label>
                    <select 
                        value={category} 
                        onChange={handleCategoryChange}
                        className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold focus:border-neon-pink focus:outline-none transition-colors appearance-none"
                    >
                        {Object.keys(units).map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                </div>
                
                <div>
                    <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">Value</label>
                    <input 
                        type="number" 
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold focus:border-neon-pink focus:outline-none transition-colors"
                    />
                </div>
                
                <div className="flex gap-4">
                    <div className="flex-1">
                        <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">From Base</label>
                        <select 
                            value={from} 
                            onChange={(e) => setFrom(e.target.value)}
                            className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold focus:border-neon-blue focus:outline-none transition-colors appearance-none"
                        >
                            {Object.keys(units[category]).map(c => <option key={c} value={c}>{c}</option>)}
                        </select>
                    </div>
                    <div className="flex-1">
                        <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">To Target</label>
                        <select 
                            value={to} 
                            onChange={(e) => setTo(e.target.value)}
                            className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold focus:border-neon-blue focus:outline-none transition-colors appearance-none"
                        >
                            {Object.keys(units[category]).map(c => <option key={c} value={c}>{c}</option>)}
                        </select>
                    </div>
                </div>
            </div>

            <button 
                onClick={handleConvert}
                className="w-full py-4 mt-8 bg-white/5 border border-white/20 rounded-xl font-black uppercase tracking-widest hover:bg-white/10 hover:border-neon-pink transition-all"
            >
                Execute Shift
            </button>

            {result && (
                <div className="mt-8 p-6 bg-neon-pink/10 border border-neon-pink/30 rounded-xl text-center">
                    <span className="text-xs font-black uppercase tracking-widest text-gray-400">Yield</span>
                    <div className="text-4xl font-black text-neon-pink mt-2 drop-shadow-[0_0_10px_rgba(255,0,128,0.5)]">
                        {result} <span className="text-sm opacity-50">{to}</span>
                    </div>
                </div>
            )}
        </div>
    );
};

export default UnitConverter;
