import React from 'react';
import { motion } from 'framer-motion';

const ZoneCard = ({
    title,
    subtitle,
    icon,
    hint,
    color, // string (Tailwind classes for gradient like "from-blue-600 to-cyan-500")
    delay = 0,
    onClick,
    isDark = true, // pass from parent context or store
}) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay, duration: 0.5 }}
            whileHover={{ y: -5, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onClick}
            className={`group relative overflow-hidden rounded-3xl p-5 ring-1 transition-all duration-300 cursor-pointer ${isDark
                    ? "bg-white/5 ring-white/10 hover:bg-white/10 hover:ring-white/20 hover:shadow-2xl hover:shadow-violet-900/20"
                    : "bg-white/80 ring-slate-900/10 hover:bg-white hover:ring-slate-900/20 hover:shadow-xl hover:shadow-slate-200"
                }`}
        >
            {/* Background Glow on Hover */}
            <div
                className={`absolute -right-12 -top-12 h-32 w-32 rounded-full blur-3xl transition-opacity duration-500 group-hover:opacity-100 opacity-0 ${isDark ? "bg-white/10" : "bg-slate-400/20"
                    }`}
            />

            <div className="relative z-10 flex items-start justify-between">
                <div
                    className={`h-12 w-12 rounded-2xl grid place-items-center text-white shadow-lg transition-transform duration-300 group-hover:scale-110 bg-gradient-to-br ${color}`}
                >
                    {icon} {/* Expecting a React Node (Lucide Icon) */}
                </div>
                <span className={`text-[10px] uppercase tracking-wider font-bold ${isDark ? "text-slate-500" : "text-slate-400"}`}>
                    Travel
                </span>
            </div>

            <div className="relative z-10 mt-5">
                <h3 className={`text-lg font-black tracking-tight ${isDark ? "text-slate-100" : "text-slate-800"}`}>
                    {title}
                </h3>
                <p className={`text-sm font-medium ${isDark ? "text-slate-400" : "text-slate-500"}`}>
                    {subtitle}
                </p>

                <div className={`mt-3 flex items-center gap-2 text-[11px] font-semibold ${isDark ? "text-slate-500 group-hover:text-slate-300" : "text-slate-500 group-hover:text-slate-600"} transition-colors`}>
                    <span className="italic">“{hint}”</span>
                </div>
            </div>
        </motion.div>
    );
};

export default ZoneCard;
