import React from 'react';
import { motion } from 'framer-motion';
import { ChevronLeft, Info, Settings2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ToolLayout = ({ children, module }) => {
    const navigate = useNavigate();

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Tool Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-6">
                    <button
                        onClick={() => navigate(-1)}
                        className="w-12 h-12 flex items-center justify-center bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 transition-all group"
                    >
                        <ChevronLeft size={24} className="text-gray-400 group-hover:text-white" />
                    </button>
                    <div>
                        <h2 className="text-3xl font-black uppercase tracking-tighter flex items-center gap-3">
                            <span className="w-10 h-10 rounded-xl bg-neon-pink/10 border border-neon-pink/20 flex items-center justify-center text-2xl">
                                {module.icon}
                            </span>
                            {module.name}
                        </h2>
                        <p className="text-gray-500 text-sm font-medium mt-1">{module.description}</p>
                    </div>
                </div>

                <div className="flex gap-2">
                    <button className="p-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all text-gray-400 hover:text-white">
                        <Info size={20} />
                    </button>
                    <button className="p-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all text-gray-400 hover:text-white">
                        <Settings2 size={20} />
                    </button>
                </div>
            </div>

            {/* Tool Surface */}
            <motion.div
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-dark-surface/30 border border-white/5 rounded-[40px] p-8 lg:p-12 relative overflow-hidden backdrop-blur-sm"
            >
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-neon-pink to-transparent opacity-30" />
                <div className="relative z-10">
                    {children}
                </div>
            </motion.div>

            {/* Tool Footer (Optional Tip) */}
            <div className="bg-white/5 border border-white/5 rounded-2xl p-4 flex items-center gap-4 text-xs text-gray-500">
                <div className="w-8 h-8 rounded-lg bg-neon-blue/10 flex items-center justify-center text-neon-blue">
                    <Info size={14} />
                </div>
                <span>PRO TIP: Precision measurements yield optimal neural results. Ensure all parameters are calibrated.</span>
            </div>
        </div>
    );
};

export default ToolLayout;
