import React from 'react';
import { motion } from 'framer-motion';
import { Settings, Shield, Zap, Server, Key, Eye, RefreshCw, AlertOctagon } from 'lucide-react';

const SystemSettings = () => {
    return (
        <div className="space-y-8 pb-12">
            <header>
                <h1 className="text-3xl font-black mb-1 opacity-90 uppercase tracking-tighter">SYSTEM <span className="text-neon-pink">SETTINGS</span></h1>
                <p className="text-gray-500 text-[10px] uppercase tracking-[0.3em] font-black">Global Configuration • Neural Matrix Parameters</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Security & Access */}
                <div className="bg-dark-surface/40 border border-white/10 rounded-3xl p-8 backdrop-blur-sm">
                    <h3 className="font-black text-xs uppercase tracking-widest mb-8 flex items-center gap-3">
                        <Shield size={18} className="text-neon-blue" />
                        CORE SECURITY PROTOCOLS
                    </h3>
                    <div className="space-y-6">
                        {[
                            { label: 'Neural MFA Required', desc: 'Enforce multi-factor verification for all agents.', enabled: true },
                            { label: 'Platform Visibility', desc: 'Control public recruitment layer access.', enabled: true },
                            { label: 'Debug Verbosity', desc: 'Detailed log injection for development nodes.', enabled: false },
                        ].map((setting, i) => (
                            <div key={i} className="flex items-center justify-between gap-6 group">
                                <div className="space-y-1">
                                    <p className="text-sm font-bold text-gray-200">{setting.label}</p>
                                    <p className="text-[10px] text-gray-500 font-medium">{setting.desc}</p>
                                </div>
                                <button className={`w-12 h-6 rounded-full relative transition-all ${setting.enabled ? 'bg-neon-blue' : 'bg-gray-800'}`}>
                                    <div className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-all ${setting.enabled ? 'right-1' : 'left-1'}`} />
                                </button>
                            </div>
                        ))}
                    </div>
                </div>

                {/* API & Infrastructure */}
                <div className="bg-dark-surface/40 border border-white/10 rounded-3xl p-8 backdrop-blur-sm">
                    <h3 className="font-black text-xs uppercase tracking-widest mb-8 flex items-center gap-3">
                        <Zap size={18} className="text-neon-pink" />
                        INFRASTRUCTURE PARAMETERS
                    </h3>
                    <div className="space-y-8">
                        <div className="space-y-3">
                            <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest flex justify-between">
                                Global Telemetry Sync Interval <span>30s</span>
                            </label>
                            <input type="range" className="w-full accent-neon-pink opacity-50 hover:opacity-100 transition-opacity" />
                        </div>
                        <div className="space-y-3">
                            <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest flex justify-between">
                                API Rate Limit (Neural/Min) <span>1,200</span>
                            </label>
                            <input type="range" className="w-full accent-neon-pink opacity-50 hover:opacity-100 transition-opacity" />
                        </div>
                        <div className="pt-4 border-t border-white/5 flex gap-4">
                            <button className="flex-1 py-3 bg-white/5 border border-white/10 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-white/10 transition-all flex items-center justify-center gap-2">
                                <Key size={14} /> Rotate Keys
                            </button>
                            <button className="flex-1 py-3 bg-white/5 border border-white/10 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-white/10 transition-all flex items-center justify-center gap-2">
                                <RefreshCw size={14} /> Clear Cache
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Danger Zone */}
            <div className="bg-red-500/5 border border-red-500/10 rounded-3xl p-8">
                <h3 className="font-black text-xs uppercase tracking-widest mb-6 flex items-center gap-3 text-red-500">
                    <AlertOctagon size={18} />
                    CRITICAL OVERRIDE
                </h3>
                <div className="flex flex-col md:flex-row items-center justify-between gap-8">
                    <div className="space-y-2">
                        <p className="text-sm font-bold text-red-200">Maintenance Protocol (Sector 0)</p>
                        <p className="text-xs text-gray-500 max-w-xl">
                            Activating maintenance mode will sever all user links and lock down the neural grid. This action is recursive and cannot be undone without root-level clearance.
                        </p>
                    </div>
                    <button className="px-8 py-3 bg-red-500 text-white font-black rounded-xl hover:bg-red-600 transition-all uppercase tracking-tighter whitespace-nowrap">
                        Initiate Global Lockdown
                    </button>
                </div>
            </div>
        </div>
    );
};

export default SystemSettings;
