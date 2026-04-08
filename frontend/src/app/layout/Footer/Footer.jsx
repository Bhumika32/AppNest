import React from 'react';
import { motion } from 'framer-motion';
import { Users, Wifi, Cpu, Zap } from 'lucide-react';

const Footer = () => {
    const [stats, setStats] = React.useState({
        latency: 24,
        online: 4291,
        server: 'Tokyo-North-1'
    });

    React.useEffect(() => {
        const interval = setInterval(() => {
            setStats(prev => ({
                ...prev,
                latency: Math.floor(Math.random() * 15) + 15,
                online: prev.online + (Math.random() > 0.5 ? 1 : -1)
            }));
        }, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <footer className="h-10 border-t border-white/10 bg-dark-bg/40 backdrop-blur-sm flex items-center justify-between px-6 text-[10px] uppercase tracking-widest text-gray-500 overflow-hidden relative">
            {/* Animated HUD line */}
            <motion.div
                animate={{ x: ['-100%', '100%'] }}
                transition={{ duration: 10, repeat: Infinity, ease: 'linear' }}
                className="absolute top-0 left-0 w-32 h-[1px] bg-gradient-to-r from-transparent via-neon-blue to-transparent"
            />

            {/* Left: System Status */}
            <div className="flex items-center gap-4 z-10">
                <div className="flex items-center gap-1.5 flex-nowrap">
                    <span className="w-1.5 h-1.5 rounded-full bg-neon-green animate-pulse" />
                    <span>Server: {stats.server}</span>
                </div>
                <div className="flex items-center gap-1.5">
                    <Zap size={12} className="text-neon-blue" />
                    <span>Latency: {stats.latency}ms</span>
                </div>
            </div>

            {/* Center: Seasonal Event */}
            <div className="hidden md:flex items-center gap-2 bg-neon-pink/10 px-3 py-0.5 rounded-full border border-neon-pink/20 text-neon-pink font-black">
                <Zap size={10} />
                <span>Seasonal Event: Cyber Nexus (Ends in 4d)</span>
            </div>

            {/* Right: Metadata */}
            <div className="flex items-center gap-6 z-10">
                <div className="flex items-center gap-2">
                    <Users size={12} />
                    <span>{stats.online.toLocaleString()} Online</span>
                </div>
                <div className="flex items-center gap-2 font-black">
                    <span>v2.8.5-beta</span>
                </div>
                <div className="flex items-center gap-1 text-neon-blue/50">
                    <span className="font-mono">[</span>
                    <Cpu size={12} />
                    <span className="font-mono">]</span>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
