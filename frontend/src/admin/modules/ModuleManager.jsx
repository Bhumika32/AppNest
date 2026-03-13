import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Search, Edit2, Trash2, Power, LayoutGrid, List, AlertCircle, CheckCircle, X } from 'lucide-react';
import api from '../../api/apiClient';

const ModuleManager = () => {
    const [modules, setModules] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [view, setView] = useState('grid');
    const [showModal, setShowModal] = useState(false);
    const [editingModule, setEditingModule] = useState(null);
    const [formData, setFormData] = useState({
        name: '', type: 'tool', slug: '', description: '',
        icon: '🛠️', component_key: '', category: '', difficulty: 'Simple'
    });

    const fetchModules = async () => {
        try {
            const { data } = await api.get('/modules');
            setModules(data);
        } catch (err) {
            console.error('Fetch failed', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchModules(); }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (editingModule) {
                await api.patch(`/admin/modules/${editingModule.id}`, formData);
            } else {
                await api.post('/admin/modules', formData);
            }
            setShowModal(false);
            setEditingModule(null);
            fetchModules();
        } catch (err) {
            alert(err.response?.data?.error || 'Operation failed');
        }
    };

    const toggleStatus = async (module) => {
        try {
            await api.patch(`/admin/modules/${module.id}`, { is_active: !module.is_active });
            fetchModules();
        } catch (err) {
            console.error('Toggle failed', err);
        }
    };

    const deleteModule = async (id) => {
        if (!window.confirm('Erase this module from the neural core?')) return;
        try {
            await api.delete(`/admin/modules/${id}`);
            fetchModules();
        } catch (err) {
            console.error('Delete failed', err);
        }
    };

    const filtered = modules.filter(m =>
        m.name.toLowerCase().includes(search.toLowerCase()) ||
        m.slug.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="space-y-8 p-4">
            {/* Admin Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div>
                    <h1 className="text-4xl font-black uppercase tracking-tighter">Module <span className="text-neon-blue">Control</span></h1>
                    <p className="text-gray-500 text-sm font-medium">Neural Registry & Extension Management</p>
                </div>

                <div className="flex items-center gap-4">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={16} />
                        <input
                            type="text"
                            placeholder="Search Registry..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            className="bg-white/5 border border-white/10 rounded-xl py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-neon-blue/50 w-64"
                        />
                    </div>
                    <button
                        onClick={() => { setEditingModule(null); setFormData({ name: '', type: 'tool', slug: '', description: '', icon: '🛠️', component_key: '', category: '', difficulty: 'Simple' }); setShowModal(true); }}
                        className="bg-neon-blue text-black font-black uppercase text-xs px-6 py-3 rounded-xl hover:scale-105 transition-all flex items-center gap-2"
                    >
                        <Plus size={16} strokeWidth={3} /> Register New
                    </button>
                </div>
            </div>

            {/* Modules Display */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filtered.map(mod => (
                    <motion.div
                        key={mod.id}
                        layout
                        className={`bg-dark-surface/40 border border-white/5 rounded-3xl p-6 relative overflow-hidden ${!mod.is_active ? 'opacity-50 grayscale' : ''}`}
                    >
                        <div className="flex items-start justify-between mb-6">
                            <div className="flex items-center gap-4">
                                <div className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-2xl">
                                    {mod.icon}
                                </div>
                                <div>
                                    <h3 className="font-black uppercase tracking-tight">{mod.name}</h3>
                                    <div className="text-[10px] text-neon-blue font-bold uppercase tracking-widest">{mod.type} | {mod.category}</div>
                                </div>
                            </div>
                            <div className="flex gap-1">
                                <button onClick={() => { setEditingModule(mod); setFormData(mod); setShowModal(true); }} className="p-2 hover:bg-white/10 rounded-lg text-gray-400 hover:text-white transition-colors">
                                    <Edit2 size={14} />
                                </button>
                                <button onClick={() => deleteModule(mod.id)} className="p-2 hover:bg-red-500/10 rounded-lg text-gray-400 hover:text-red-500 transition-colors">
                                    <Trash2 size={14} />
                                </button>
                            </div>
                        </div>

                        <p className="text-gray-500 text-xs mb-8 line-clamp-2">{mod.description}</p>

                        <div className="flex items-center justify-between border-t border-white/5 pt-4">
                            <div className="text-[10px] font-black uppercase tracking-widest text-gray-700">Slug: {mod.slug}</div>
                            <button
                                onClick={() => toggleStatus(mod)}
                                className={`flex items-center gap-2 px-3 py-1 rounded-full text-[9px] font-black uppercase transition-all ${mod.is_active ? 'bg-neon-green/10 text-neon-green border border-neon-green/20' : 'bg-red-500/10 text-red-500 border border-red-500/20'}`}
                            >
                                <Power size={10} /> {mod.is_active ? 'Online' : 'Offline'}
                            </button>
                        </div>
                    </motion.div>
                ))}
            </div>

            {/* Registration Modal */}
            <AnimatePresence>
                {showModal && (
                    <div className="fixed inset-0 z-[1000] flex items-center justify-center p-4">
                        <motion.div
                            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                            className="absolute inset-0 bg-black/80 backdrop-blur-md"
                            onClick={() => setShowModal(false)}
                        />
                        <motion.div
                            initial={{ scale: 0.9, opacity: 0, y: 20 }} animate={{ scale: 1, opacity: 1, y: 0 }} exit={{ scale: 0.9, opacity: 0, y: 20 }}
                            className="relative bg-[#0d0d12] border border-white/10 rounded-[40px] w-full max-w-2xl p-10 overflow-hidden"
                        >
                            <div className="absolute top-0 right-0 w-64 h-64 bg-neon-blue/5 blur-[80px] -mr-32 -mt-32 rounded-full" />

                            <div className="flex items-center justify-between mb-8 relative">
                                <h2 className="text-2xl font-black uppercase tracking-tighter">
                                    {editingModule ? 'Update' : 'Initialize'} <span className="text-neon-blue">Neural Module</span>
                                </h2>
                                <button onClick={() => setShowModal(false)} className="p-2 hover:bg-white/5 rounded-xl text-gray-500 hover:text-white transition-all">
                                    <X size={24} />
                                </button>
                            </div>

                            <form onSubmit={handleSubmit} className="space-y-6 relative">
                                <div className="grid grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black uppercase tracking-widest text-gray-500 ml-1">Module Name</label>
                                        <input
                                            required value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })}
                                            className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-sm focus:border-neon-blue/50 transition-all font-medium"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black uppercase tracking-widest text-gray-500 ml-1">Universal Slug</label>
                                        <input
                                            required value={formData.slug} onChange={e => setFormData({ ...formData, slug: e.target.value })}
                                            className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-sm focus:border-neon-blue/50 transition-all font-medium"
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black uppercase tracking-widest text-gray-500 ml-1">Module Type</label>
                                        <select
                                            value={formData.type} onChange={e => setFormData({ ...formData, type: e.target.value })}
                                            className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-sm focus:border-neon-blue/50 transition-all font-black uppercase"
                                        >
                                            <option value="tool" className="bg-dark-bg">🛠️ Utility Tool</option>
                                            <option value="game" className="bg-dark-bg">🎮 Simulation Game</option>
                                        </select>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black uppercase tracking-widest text-gray-500 ml-1">Registry Key (Component)</label>
                                        <input
                                            required value={formData.component_key} onChange={e => setFormData({ ...formData, component_key: e.target.value })}
                                            className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-sm focus:border-neon-blue/50 transition-all font-mono"
                                        />
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <label className="text-[10px] font-black uppercase tracking-widest text-gray-500 ml-1">Neural Narrative (Description)</label>
                                    <textarea
                                        required value={formData.description} onChange={e => setFormData({ ...formData, description: e.target.value })}
                                        className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-sm focus:border-neon-blue/50 transition-all font-medium h-24 resize-none"
                                    />
                                </div>

                                <div className="grid grid-cols-3 gap-6">
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black uppercase tracking-widest text-gray-500 ml-1">Icon (Emoji)</label>
                                        <input
                                            value={formData.icon} onChange={e => setFormData({ ...formData, icon: e.target.value })}
                                            className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-center text-xl focus:border-neon-blue/50"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black uppercase tracking-widest text-gray-500 ml-1">Category</label>
                                        <input
                                            value={formData.category} onChange={e => setFormData({ ...formData, category: e.target.value })}
                                            className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-sm focus:border-neon-blue/50 transition-all font-medium"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black uppercase tracking-widest text-gray-500 ml-1">Difficulty</label>
                                        <input
                                            value={formData.difficulty} onChange={e => setFormData({ ...formData, difficulty: e.target.value })}
                                            className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-sm focus:border-neon-blue/50 transition-all font-medium"
                                        />
                                    </div>
                                </div>

                                <button
                                    type="submit"
                                    className="w-full bg-neon-blue text-black font-black uppercase tracking-[0.2em] py-5 rounded-3xl hover:shadow-[0_0_40px_rgba(0,243,255,0.3)] transition-all mt-4"
                                >
                                    {editingModule ? 'Finalize Updates' : 'Inject Module Into Core'}
                                </button>
                            </form>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default ModuleManager;
