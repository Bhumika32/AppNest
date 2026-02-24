import React from 'react';
import ToolLayout from '../../layout/Module/ToolLayout.jsx';
import { motion } from 'framer-motion';

const BMICalculator = ({ module }) => {
    const [weight, setWeight] = React.useState(70);
    const [height, setHeight] = React.useState(170);

    const bmi = (weight / ((height / 100) ** 2)).toFixed(1);

    const getCategory = (val) => {
        if (val < 18.5) return { label: 'Underweight', color: 'text-yellow-400' };
        if (val < 25) return { label: 'Optimal', color: 'text-neon-green' };
        if (val < 30) return { label: 'Overweight', color: 'text-orange-400' };
        return { label: 'Critical', color: 'text-red-500' };
    };

    const category = getCategory(parseFloat(bmi));

    return (
        <ToolLayout module={module}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                <div className="space-y-10">
                    <div className="space-y-4">
                        <div className="flex justify-between items-end">
                            <label className="text-[10px] font-black uppercase tracking-widest text-gray-500">Body Mass Index: {height}cm</label>
                        </div>
                        <input
                            type="range" min="100" max="220" value={height}
                            onChange={(e) => setHeight(e.target.value)}
                            className="w-full h-1.5 bg-white/10 rounded-lg appearance-none cursor-pointer accent-neon-pink"
                        />
                    </div>

                    <div className="space-y-4">
                        <div className="flex justify-between items-end">
                            <label className="text-[10px] font-black uppercase tracking-widest text-gray-500">Neural Weight: {weight}kg</label>
                        </div>
                        <input
                            type="range" min="30" max="150" value={weight}
                            onChange={(e) => setWeight(e.target.value)}
                            className="w-full h-1.5 bg-white/10 rounded-lg appearance-none cursor-pointer accent-neon-pink"
                        />
                    </div>
                </div>

                <div className="flex flex-col items-center justify-center p-8 bg-black/40 border border-white/10 rounded-[32px] text-center">
                    <motion.div
                        key={bmi}
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        className="text-6xl font-black mb-2 tracking-tighter"
                    >
                        {bmi}
                    </motion.div>
                    <div className={`text-[10px] font-black uppercase tracking-[0.3em] ${category.color}`}>
                        Status: {category.label}
                    </div>

                    <div className="w-full mt-8 h-1 bg-white/5 rounded-full overflow-hidden">
                        <motion.div
                            animate={{ width: `${Math.min(100, (bmi / 40) * 100)}%` }}
                            className={`h-full bg-gradient-to-r from-neon-pink to-neon-blue`}
                        />
                    </div>
                </div>
            </div>
        </ToolLayout>
    );
};

export default BMICalculator;
