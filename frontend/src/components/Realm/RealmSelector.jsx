import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { USER_REALMS } from '../../app/realmConstants';

const RealmSelector = () => {
    const navigate = useNavigate();
    const location = useLocation();

    return (
        <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 px-6 py-3 bg-dark-surface/80 backdrop-blur-xl border border-white/10 rounded-full shadow-2xl flex items-center gap-2">
            {USER_REALMS.map((realm) => {
                const isActive = location.pathname === realm.path || (realm.path !== '/dashboard' && location.pathname.startsWith(realm.path));
                const Icon = realm.icon;

                return (
                    <motion.button
                        key={realm.id}
                        onClick={() => navigate(realm.path)}
                        className={`p-2 rounded-full transition-all relative group ${isActive ? 'text-neon-blue bg-neon-blue/10' : 'text-gray-400 hover:text-white hover:bg-white/5'
                            }`}
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                    >
                        <Icon size={20} />
                        <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-black text-[10px] font-bold uppercase tracking-widest rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap border border-white/10">
                            {realm.label}
                        </span>
                        {isActive && (
                            <motion.div
                                layoutId="activeRealm"
                                className="absolute inset-0 border-2 border-neon-blue rounded-full"
                                transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                            />
                        )}
                    </motion.button>
                );
            })}
        </div>
    );
};

export default RealmSelector;
