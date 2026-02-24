import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Users, Search, Filter, MoreVertical, Shield, UserX, CheckCircle, Mail } from 'lucide-react';

const UserManagement = () => {
    const [searchTerm, setSearchTerm] = useState('');

    // Mock users - in a real app, this would be fetched from the adminService
    const users = [
        { id: 1, username: 'neo_coder', email: 'neo@appnest.io', role: 'admin', status: 'active', joined: '2025-01-12' },
        { id: 2, username: 'trinity', email: 'trinity@zion.net', role: 'user', status: 'active', joined: '2025-02-01' },
        { id: 3, username: 'cypher_9', email: 'cypher@traitor.com', role: 'user', status: 'flagged', joined: '2025-02-15' },
        { id: 4, username: 'morpheus', email: 'dream@neb.io', role: 'admin', status: 'active', joined: '2024-12-20' },
        { id: 5, username: 'agent_smith', email: 'smith@matrix.com', role: 'user', status: 'banned', joined: '2025-01-05' },
    ];

    const filteredUsers = users.filter(u =>
        u.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
        u.email.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="space-y-8 max-w-7xl mx-auto">
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div>
                    <h1 className="text-3xl font-black mb-1 tracking-tighter uppercase">USER <span className="text-neon-blue">MANAGEMENT</span></h1>
                    <p className="text-gray-500 text-[10px] uppercase tracking-[0.3em] font-black">Neural Population Control • Role Orchestration</p>
                </div>
                <div className="flex items-center gap-3">
                    <div className="relative group">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-neon-blue transition-colors" size={14} />
                        <input
                            type="text"
                            placeholder="Search Agents..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="bg-white/5 border border-white/10 rounded-xl py-2.5 pl-10 pr-4 text-xs font-bold focus:outline-none focus:border-neon-blue/50 focus:bg-white/10 transition-all w-64"
                        />
                    </div>
                    <button className="p-2.5 bg-white/5 border border-white/10 rounded-xl text-gray-400 hover:text-white hover:bg-white/10 transition-all">
                        <Filter size={18} />
                    </button>
                </div>
            </header>

            <section className="bg-dark-surface/40 border border-white/10 rounded-3xl overflow-hidden backdrop-blur-sm">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="border-b border-white/5 bg-white/2">
                            <th className="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-gray-500">Agent Details</th>
                            <th className="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-gray-500">Neural Role</th>
                            <th className="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-gray-500">Status</th>
                            <th className="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-gray-500">Sync Date</th>
                            <th className="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-gray-500 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                        {filteredUsers.map((user) => (
                            <motion.tr
                                key={user.id}
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="hover:bg-white/2 transition-colors group"
                            >
                                <td className="px-6 py-5">
                                    <div className="flex items-center gap-4">
                                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-neon-blue/20 to-neon-pink/20 flex items-center justify-center border border-white/5 text-xs font-black">
                                            {user.username.charAt(0).toUpperCase()}
                                        </div>
                                        <div>
                                            <div className="text-sm font-bold text-gray-200 group-hover:text-white transition-colors">{user.username}</div>
                                            <div className="text-[10px] text-gray-500 font-medium flex items-center gap-1">
                                                <Mail size={10} /> {user.email}
                                            </div>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-5">
                                    <span className={`text-[10px] font-black px-2 py-1 rounded-lg border ${user.role === 'admin'
                                            ? 'bg-neon-pink/10 border-neon-pink/20 text-neon-pink'
                                            : 'bg-neon-blue/10 border-neon-blue/20 text-neon-blue'
                                        } uppercase tracking-widest`}>
                                        {user.role}
                                    </span>
                                </td>
                                <td className="px-6 py-5">
                                    <div className="flex items-center gap-2">
                                        <div className={`w-1.5 h-1.5 rounded-full ${user.status === 'active' ? 'bg-neon-green' :
                                                user.status === 'flagged' ? 'bg-yellow-500' : 'bg-neon-pink'
                                            }`} />
                                        <span className="text-[10px] font-black uppercase tracking-widest text-gray-400">{user.status}</span>
                                    </div>
                                </td>
                                <td className="px-6 py-5 text-xs font-bold text-gray-500">
                                    {user.joined}
                                </td>
                                <td className="px-6 py-5 text-right">
                                    <button className="p-2 text-gray-500 hover:text-white transition-colors">
                                        <MoreVertical size={18} />
                                    </button>
                                </td>
                            </motion.tr>
                        ))}
                    </tbody>
                </table>
            </section>

            <footer className="flex items-center justify-between px-6">
                <span className="text-[10px] font-black text-gray-600 uppercase tracking-widest">
                    Showing {filteredUsers.length} of {users.length} unique signatures
                </span>
                <div className="flex gap-2">
                    <button className="px-4 py-2 bg-white/5 border border-white/5 rounded-lg text-[10px] font-black uppercase text-gray-500 cursor-not-allowed">Previous</button>
                    <button className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-[10px] font-black uppercase text-gray-300 hover:bg-white/10 transition-all">Next Segment</button>
                </div>
            </footer>
        </div>
    );
};

export default UserManagement;
