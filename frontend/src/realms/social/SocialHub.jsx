import React from 'react';
import { motion } from 'framer-motion';
import { Users, MessageSquare, Heart, Share2, Search, Send, Activity } from 'lucide-react';

const PostCard = ({ author, content, likes, comments, time, color }) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="bg-white/5 border border-white/5 rounded-3xl p-6 hover:bg-white/[0.07] transition-all group"
    >
        <div className="flex justify-between items-start mb-4">
            <div className="flex items-center gap-3">
                <div className={`w-10 h-10 rounded-xl bg-${color}/10 border border-${color}/20 flex items-center justify-center text-${color} font-black`}>
                    {author[0]}
                </div>
                <div>
                    <h4 className="text-sm font-black text-white uppercase">{author}</h4>
                    <span className="text-[8px] text-gray-500 font-bold uppercase tracking-widest">{time}</span>
                </div>
            </div>
            <Activity size={14} className="text-gray-700" />
        </div>
        <p className="text-sm text-gray-400 font-medium leading-[1.6] mb-6">
            {content}
        </p>
        <div className="flex items-center gap-6">
            <button className="flex items-center gap-2 text-[10px] font-black text-gray-500 hover:text-neon-pink transition-colors">
                <Heart size={14} /> {likes}
            </button>
            <button className="flex items-center gap-2 text-[10px] font-black text-gray-500 hover:text-neon-blue transition-colors">
                <MessageSquare size={14} /> {comments}
            </button>
            <button className="ml-auto text-gray-600 hover:text-white transition-colors">
                <Share2 size={14} />
            </button>
        </div>
    </motion.div>
);

const SocialHub = () => {
    const feeds = [
        { author: 'AG_ZERO', content: 'Just cracked the neural pattern in the high-stakes sector. 125k XP and climbing! Who\'s next?', likes: 24, comments: 8, time: '2h ago', color: 'neon-blue' },
        { author: 'OPERATOR_K', content: 'New Forge tools are operational. The Biometric Analysis module is showing some interesting deviations today.', likes: 15, comments: 3, time: '4h ago', color: 'neon-pink' },
        { author: 'VOID_X', content: 'Seeking partners for the local arcade challenge. Need agents with high reflex sync.', likes: 42, comments: 12, time: '6h ago', color: 'neon-green' },
    ];

    return (
        <div className="space-y-12 pb-20">
            <header className="relative p-12 rounded-[2rem] overflow-hidden bg-dark-surface/30 border border-white/5">
                <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-neon-blue/5 blur-[120px] -mr-48 -mt-48 rounded-full" />
                <div className="relative z-10 max-w-2xl">
                    <div className="w-fit p-3 rounded-2xl bg-neon-blue/10 border border-neon-blue/20 text-neon-blue mb-8">
                        <Users size={32} />
                    </div>
                    <h1 className="text-6xl font-black mb-6 tracking-tighter leading-[0.9]">
                        THE SOCIAL <br />
                        <span className="text-neon-blue">SUB-LINK</span>
                    </h1>
                    <p className="text-gray-400 text-lg leading-relaxed font-medium">
                        Synchronize with other operatives across the matrix. Share performance logs, form squads, and dominate the boards.
                    </p>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <section className="lg:col-span-2 space-y-8">
                    {/* Create Post */}
                    <div className="bg-white/5 border border-white/5 rounded-[2rem] p-8">
                        <div className="flex items-center gap-4 mb-6">
                            <div className="w-10 h-10 rounded-xl bg-neon-blue/10 flex items-center justify-center text-neon-blue font-black border border-neon-blue/20">
                                Z
                            </div>
                            <input
                                type="text"
                                placeholder="Transmit data to the network..."
                                className="flex-1 bg-transparent border-b border-white/10 py-2 text-sm font-medium focus:outline-none focus:border-neon-blue transition-all"
                            />
                            <button className="p-3 bg-neon-blue/10 text-neon-blue rounded-xl hover:bg-neon-blue hover:text-black transition-all">
                                <Send size={20} />
                            </button>
                        </div>
                        <div className="flex gap-4">
                            <button className="text-[10px] font-black text-gray-500 hover:text-white uppercase tracking-widest flex items-center gap-2">
                                <Activity size={14} /> Attach Metrics
                            </button>
                            <button className="text-[10px] font-black text-gray-500 hover:text-white uppercase tracking-widest flex items-center gap-2">
                                <Users size={14} /> Tag Squad
                            </button>
                        </div>
                    </div>

                    {/* Feed */}
                    <div className="space-y-6">
                        <div className="flex items-center justify-between mb-8 px-4">
                            <h2 className="text-xl font-black tracking-tight uppercase flex items-center gap-3">
                                <div className="w-1.5 h-6 bg-neon-blue rounded-full" />
                                Transmissions
                            </h2>
                            <div className="flex gap-4 text-[10px] font-black text-gray-500 uppercase tracking-widest">
                                <span className="text-neon-blue cursor-pointer">Trending</span>
                                <span className="cursor-pointer hover:text-white transition-colors">Recent</span>
                            </div>
                        </div>
                        {feeds.map((post, i) => <PostCard key={i} {...post} />)}
                    </div>
                </section>

                <aside className="space-y-8">
                    <div className="bg-dark-surface/40 border border-white/5 rounded-3xl p-8 backdrop-blur-md">
                        <h3 className="text-sm font-black text-white uppercase tracking-widest mb-8">Active Operatives</h3>
                        <div className="space-y-6">
                            {[
                                { name: 'CYBER_PULSE', status: 'In Game: Neon Runner', color: 'neon-pink' },
                                { name: 'NEO_GHOST', status: 'Online', color: 'neon-green' },
                                { name: 'QUANTUM_RAY', status: 'Consulting Forge', color: 'neon-blue' }
                            ].map((user, i) => (
                                <div key={i} className="flex items-center gap-4">
                                    <div className={`relative w-10 h-10 rounded-xl bg-${user.color}/10 border border-${user.color}/20 flex items-center justify-center text-${user.color} font-black`}>
                                        {user.name[0]}
                                        <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-neon-green border-2 border-[#0a0a0c] rounded-full" />
                                    </div>
                                    <div>
                                        <div className="text-xs font-black text-white uppercase">{user.name}</div>
                                        <div className="text-[9px] text-gray-500 font-bold uppercase">{user.status}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <button className="w-full mt-10 py-3 border border-white/5 hover:bg-white/5 rounded-xl text-[10px] font-black text-gray-500 uppercase tracking-widest transition-all">
                            Find Agents
                        </button>
                    </div>

                    <div className="bg-neon-pink/5 border border-neon-pink/20 rounded-3xl p-8">
                        <h3 className="text-sm font-black text-neon-pink uppercase tracking-widest mb-4">Pulse Alert</h3>
                        <p className="text-[10px] text-gray-400 font-medium leading-relaxed mb-6">
                            Localized tournament starting in Sector 7-B. Prize pool of 500 Credits and exclusive neural badges.
                        </p>
                        <button className="w-full py-2 bg-neon-pink/10 text-neon-pink border border-neon-pink/30 rounded-lg text-[9px] font-black uppercase tracking-widest hover:bg-neon-pink hover:text-black transition-all">
                            Join Briefing
                        </button>
                    </div>
                </aside>
            </div>
        </div>
    );
};

export default SocialHub;
