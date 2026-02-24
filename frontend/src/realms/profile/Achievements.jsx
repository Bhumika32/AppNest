import React from 'react';
import { motion } from 'framer-motion';
import { Trophy, Shield, Zap, Target, Star, Lock, CheckCircle2 } from 'lucide-react';

const AchievementCard = ({ title, description, progress, total, icon: Icon, color, isUnlocked }) => (
    <div className={`relative p-6 rounded-3xl border transition-all ${isUnlocked ? `bg-${color}/5 border-${color}/20` : 'bg-white/5 border-white/5 opacity-60'}`}>
        {!isUnlocked && <div className="absolute inset-0 flex items-center justify-center z-10 bg-black/40 backdrop-blur-[1px] rounded-3xl"><Lock size={24} className="text-gray-600" /></div>}

        <div className="flex items-start justify-between mb-6">
            <div className={`p-4 rounded-2xl ${isUnlocked ? `bg-${color}/20 text-${color}` : 'bg-gray-800 text-gray-600'} border ${isUnlocked ? `border-${color}/30` : 'border-white/5'}`}>
                <Icon size={24} />
            </div>
            {isUnlocked && <CheckCircle2 size={16} className={`text-${color}`} />}
        </div>

        <h4 className="text-sm font-black uppercase tracking-tight mb-2">{title}</h4>
        <p className="text-[10px] text-gray-500 font-medium leading-relaxed mb-6">{description}</p>

        <div className="space-y-2">
            <div className="flex justify-between text-[8px] font-black uppercase tracking-widest text-gray-600">
                <span>Progress</span>
                <span>{progress}/{total}</span>
            </div>
            <div className="h-1 bg-white/5 rounded-full overflow-hidden">
                <div className={`h-full ${isUnlocked ? `bg-${color}` : 'bg-gray-700'}`} style={{ width: `${(progress / total) * 100}%` }} />
            </div>
        </div>
    </div>
);

const Achievements = () => {
    const categories = [
        { id: 'progression', label: 'Ecosystem Growth', icon: Trophy, color: 'neon-blue' },
        { id: 'mastery', label: 'Skill Mastery', icon: Star, color: 'neon-pink' },
        { id: 'social', label: 'Network Reach', icon: Zap, color: 'neon-green' },
    ];

    const achievementList = [
        { category: 'progression', title: 'Neural Link Established', description: 'Complete your first synchronization session.', progress: 1, total: 1, icon: Zap, color: 'neon-blue', isUnlocked: true },
        { category: 'progression', title: 'Level 10 Agent', description: 'Amass enough XP to reach clearance level 10.', progress: 1150, total: 5000, icon: Shield, color: 'neon-blue', isUnlocked: false },
        { category: 'mastery', title: 'Tic-Tac-Toe Conqueror', description: 'Defeat the adaptive AI 10 times.', progress: 8, total: 10, icon: Target, color: 'neon-pink', isUnlocked: false },
        { category: 'mastery', title: 'Neon Sprinter', description: 'Achieve a score of 500 in Neon Runner.', progress: 500, total: 500, icon: Star, color: 'neon-pink', isUnlocked: true },
        { category: 'social', title: 'Network Hub', description: 'Interact with 5 different agents in the Social Hub.', progress: 2, total: 5, icon: Zap, color: 'neon-green', isUnlocked: false },
    ];

    return (
        <div className="space-y-12 pb-20">
            <header className="relative p-12 rounded-[2rem] overflow-hidden bg-dark-surface/30 border border-white/5">
                <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-neon-pink/5 blur-[120px] -mr-48 -mt-48 rounded-full" />
                <div className="relative z-10 max-w-2xl">
                    <div className="w-fit p-3 rounded-2xl bg-neon-pink/10 border border-neon-pink/20 text-neon-pink mb-8">
                        <Star size={32} />
                    </div>
                    <h1 className="text-6xl font-black mb-6 tracking-tighter leading-[0.9]">
                        NEURAL <span className="text-neon-pink">BADGES</span><br />
                        AND MERIT
                    </h1>
                    <p className="text-gray-400 text-lg leading-relaxed font-medium">
                        Your operational milestones mapped to the global matrix. Unlock restricted sectors by proving your utility.
                    </p>
                </div>
            </header>

            <div className="space-y-12">
                {categories.map(cat => (
                    <section key={cat.id}>
                        <div className="flex items-center gap-4 mb-8">
                            <div className={`p-2 rounded-lg bg-${cat.color}/10 text-${cat.color}`}>
                                <cat.icon size={18} />
                            </div>
                            <h2 className="text-xl font-black uppercase tracking-tighter">{cat.label}</h2>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {achievementList.filter(a => a.category === cat.id).map((a, i) => (
                                <AchievementCard key={i} {...a} />
                            ))}
                        </div>
                    </section>
                ))}
            </div>
        </div>
    );
};

export default Achievements;
