import React, { useState } from 'react';

const BMICalculator = ({ showSystemDialog, completeTool }) => {
    const [height, setHeight] = useState('');
    const [weight, setWeight] = useState('');
    const [bmi, setBmi] = useState(null);

    const calculateBMI = () => {
        if (!height || !weight) {
            showSystemDialog('TOOL_ERROR', 'error');
            return;
        }

        const h = parseFloat(height) / 100;
        const w = parseFloat(weight);
        const result = (w / (h * h)).toFixed(1);
        setBmi(result);

        const category = result < 18.5 ? "Underweight"
            : result < 25 ? "Normal"
                : result < 30 ? "Overweight"
                    : "Obese";

        completeTool({
            duration: 15,
            score: 50,
            metadata: { bmi: result, category, height, weight },
            eventCategory: 'TOOL_SUCCESS'
        });
    };

    return (
        <div className="space-y-6 text-white max-w-sm mx-auto">
            <h3 className="text-xl font-black uppercase tracking-widest text-center mb-8"><span className="text-neon-pink">BMI</span> Analysis</h3>

            <div className="space-y-4">
                <div>
                    <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">Height (cm)</label>
                    <input
                        type="number"
                        value={height}
                        onChange={(e) => setHeight(e.target.value)}
                        className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold text-lg focus:border-neon-blue focus:outline-none transition-colors"
                        placeholder="175"
                    />
                </div>
                <div>
                    <label className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2 block">Weight (kg)</label>
                    <input
                        type="number"
                        value={weight}
                        onChange={(e) => setWeight(e.target.value)}
                        className="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-center font-bold text-lg focus:border-neon-pink focus:outline-none transition-colors"
                        placeholder="70"
                    />
                </div>
            </div>

            <button
                onClick={calculateBMI}
                className="w-full py-4 mt-8 bg-white/5 border border-white/20 rounded-xl font-black uppercase tracking-widest hover:bg-white/10 hover:border-neon-blue transition-all"
            >
                Calculate Metrics
            </button>

            {bmi && (
                <div className="mt-8 p-6 bg-neon-blue/10 border border-neon-blue/30 rounded-xl text-center">
                    <span className="text-xs font-black uppercase tracking-widest text-gray-400">Result</span>
                    <div className="text-5xl font-black text-neon-blue mt-2 drop-shadow-[0_0_10px_rgba(0,255,255,0.5)]">{bmi}</div>
                </div>
            )}
        </div>
    );
};

export default BMICalculator;
