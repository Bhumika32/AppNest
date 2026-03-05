import React, { useState } from 'react';

const rashis = [
    { sign: 'Aries', element: 'Fire', trait: 'Courageous' },
    { sign: 'Taurus', element: 'Earth', trait: 'Reliable' },
    { sign: 'Gemini', element: 'Air', trait: 'Adaptable' },
    { sign: 'Cancer', element: 'Water', trait: 'Compassionate' },
    { sign: 'Leo', element: 'Fire', trait: 'Charismatic' },
    { sign: 'Virgo', element: 'Earth', trait: 'Analytical' },
    { sign: 'Libra', element: 'Air', trait: 'Diplomatic' },
    { sign: 'Scorpio', element: 'Water', trait: 'Intense' },
    { sign: 'Sagittarius', element: 'Fire', trait: 'Adventurous' },
    { sign: 'Capricorn', element: 'Earth', trait: 'Disciplined' },
    { sign: 'Aquarius', element: 'Air', trait: 'Innovative' },
    { sign: 'Pisces', element: 'Water', trait: 'Empathetic' }
];

const RashiGenerator = ({ showSystemDialog, completeTool }) => {
    const [name, setName] = useState('');
    const [rashi, setRashi] = useState(null);

    const generateRashi = () => {
        if (!name) {
            showSystemDialog('TOOL_ERROR', 'error');
            return;
        }

        // Deterministic but pseudo-random generation based on name length and first char
        const charCode = name.charCodeAt(0) || 0;
        const index = (charCode + name.length) % rashis.length;
        const result = rashis[index];
        
        setRashi(result);

        completeTool({
            duration: 8,
            score: 50,
            metadata: { sign: result.sign },
            eventCategory: 'TOOL_SUCCESS'
        });
    };

    return (
        <div className="space-y-6 text-white max-w-sm mx-auto">
            <h3 className="text-xl font-black uppercase tracking-widest text-center mb-8">Celestial <span className="text-yellow-500">Alignment</span></h3>
            
            <div className="space-y-4">
                <div>
                    <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">Subject Entity Name</label>
                    <input 
                        type="text" 
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold focus:border-yellow-500 focus:outline-none transition-colors"
                        placeholder="Enter name..."
                    />
                </div>
            </div>

            <button 
                onClick={generateRashi}
                className="w-full py-4 mt-8 bg-white/5 border border-white/20 rounded-xl font-black uppercase tracking-widest hover:bg-white/10 hover:border-yellow-500 transition-all"
            >
                Read Stars
            </button>

            {rashi && (
                <div className="mt-8 p-6 bg-yellow-500/10 border border-yellow-500/30 rounded-xl text-center">
                    <span className="text-xs font-black uppercase tracking-widest text-gray-400">Astrological Profile</span>
                    <div className="text-4xl font-black text-yellow-500 mt-2 mb-2 drop-shadow-[0_0_10px_rgba(234,179,8,0.5)]">
                        {rashi.sign}
                    </div>
                    <div className="flex justify-center gap-4 text-xs font-bold uppercase tracking-widest mt-4">
                        <span className="text-orange-400">[{rashi.element}]</span>
                        <span className="text-white">[{rashi.trait}]</span>
                    </div>
                </div>
            )}
        </div>
    );
};

export default RashiGenerator;
