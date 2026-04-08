import React, { useState } from 'react';

const AgeCalculator = ({ showSystemDialog, completeTool }) => {
    const [dob, setDob] = useState('');
    const [age, setAge] = useState(null);

    const calculateAge = () => {
        if (!dob) {
            showSystemDialog('TOOL_ERROR', 'error');
            return;
        }

        const birthDate = new Date(dob);
        const today = new Date();
        let years = today.getFullYear() - birthDate.getFullYear();
        let months = today.getMonth() - birthDate.getMonth();
        let days = today.getDate() - birthDate.getDate();

        if (months < 0 || (months === 0 && days < 0)) {
            years--;
            months += 12;
        }
        if (days < 0) {
            const prevMonth = new Date(today.getFullYear(), today.getMonth(), 0);
            days += prevMonth.getDate();
            months--;
        }

        setAge({ years, months, days });

        completeTool({
            duration: 10,
            score: 50,
            metadata: { calculatedAge: `${years}y ${months}m` },
            eventCategory: 'TOOL_SUCCESS'
        });
    };

    return (
        <div className="space-y-6 text-white max-w-sm mx-auto">
            <h3 className="text-xl font-black uppercase tracking-widest text-center mb-8">Temporal <span className="text-neon-green">Calculator</span></h3>
            
            <div className="space-y-4">
                <div>
                    <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">Origin Date</label>
                    <input 
                        type="date" 
                        value={dob}
                        onChange={(e) => setDob(e.target.value)}
                        className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold text-gray-300 focus:border-neon-green focus:outline-none transition-colors"
                    />
                </div>
            </div>

            <button 
                onClick={calculateAge}
                className="w-full py-4 mt-8 bg-white/5 border border-white/20 rounded-xl font-black uppercase tracking-widest hover:bg-white/10 hover:border-neon-green transition-all"
            >
                Compute Timespan
            </button>

            {age && (
                <div className="mt-8 p-6 bg-neon-green/10 border border-neon-green/30 rounded-xl text-center flex justify-around">
                    <div>
                        <div className="text-3xl font-black text-neon-green">{age.years}</div>
                        <div className="text-[10px] uppercase font-bold tracking-widest text-gray-400">Years</div>
                    </div>
                    <div>
                        <div className="text-3xl font-black text-neon-green">{age.months}</div>
                        <div className="text-[10px] uppercase font-bold tracking-widest text-gray-400">Months</div>
                    </div>
                    <div>
                        <div className="text-3xl font-black text-neon-green">{age.days}</div>
                        <div className="text-[10px] uppercase font-bold tracking-widest text-gray-400">Days</div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AgeCalculator;
