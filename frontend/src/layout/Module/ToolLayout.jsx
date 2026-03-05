import React from 'react';
import { motion } from 'framer-motion';
import { ChevronLeft, Info, Settings2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import SystemDialogPanel from '../../game-engine/personality/SystemDialogPanel.jsx';
import { personalityEngine } from '../../game-engine/personality/personalityEngine.js';
import { useModuleStore } from '../../store/moduleStore.js';
import { useUserStore } from '../../store/userStore.js';
import ModuleExecutionService from '../../services/moduleExecutionService.js';

const ToolLayout = React.memo(({ children, module }) => {
    const navigate = useNavigate();
    const fetchDashboard = useUserStore(state => state.fetchDashboard);
    const trackLaunch = useModuleStore(state => state.trackLaunch);
    const trackEnd = useModuleStore(state => state.trackEnd);
    const [dialog, setDialog] = React.useState({ active: false, message: '', type: 'info' });
    const [entryId, setEntryId] = React.useState(null);
    const [sessionStart, setSessionStart] = React.useState(null);
    const completedRef = React.useRef(false);
    const instanceRef = React.useRef(null);
    const sessionStartedRef = React.useRef(false);

    React.useEffect(() => {
        if (sessionStartedRef.current) return;
        sessionStartedRef.current = true;

        const startSession = async () => {
            setSessionStart(Date.now());
            const id = await trackLaunch(module.id);
            setEntryId(id);
        };
        startSession();

        return () => {
            if (entryId) {
                const duration = Math.floor((Date.now() - (sessionStart || Date.now())) / 1000);
                trackEnd(entryId, duration);
            }
        };
    }, [module.id, entryId, sessionStart, trackEnd, trackLaunch]); // eslint-disable-line react-hooks/exhaustive-deps

    const showSystemDialog = React.useCallback((eventCategory, type = 'info') => {
        const msg = personalityEngine.getSystemDialog(eventCategory);
        if (!msg) return; // Respect cooldown
        setDialog({ active: true, message: msg, type });
        setTimeout(() => setDialog(prev => ({ ...prev, active: false })), 4000);
    }, []);

    const handleToolComplete = React.useCallback(async (payload) => {
        if (completedRef.current) return;
        completedRef.current = true;

        try {
            await ModuleExecutionService.execute(module.slug, {
                module_id: module.id,
                duration: payload.duration || 0,
                score: payload.score || 10,
                difficulty: 'EASY',
                result: 'completed',
                metadata: payload.metadata || {},
                entry_id: entryId
            });
            fetchDashboard(); // updating top bar xp
            if (payload.eventCategory) {
                showSystemDialog(payload.eventCategory, 'success');
            }
        } catch (e) {
            console.error("Tool completion failed", e);
            completedRef.current = false; // Allow retry on failure
        }
    }, [entryId, fetchDashboard, module.id, module.slug, showSystemDialog]);

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

            {/* Tool Surface: Arcane Device Interface */}
            <motion.div
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-black/40 border border-neon-blue/30 rounded-[40px] p-8 lg:p-12 relative overflow-hidden backdrop-blur-md shadow-[0_0_30px_rgba(0,255,255,0.05)]"
            >
                {/* Holographic grid and scanlines */}
                <div className="absolute inset-0 bg-[linear-gradient(rgba(0,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,255,0.03)_1px,transparent_1px)] bg-[size:20px_20px] pointer-events-none" />
                <div className="absolute inset-0 bg-[linear-gradient(to_bottom,transparent_0%,rgba(0,255,255,0.1)_50%,transparent_100%)] animate-[scan_4s_linear_infinite] pointer-events-none opacity-50" />

                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-neon-blue to-transparent opacity-80" />

                <div className="relative z-10">
                    {(() => {
                        if (!instanceRef.current) {
                            instanceRef.current = React.Children.map(children, child => {
                                if (React.isValidElement(child)) {
                                    return React.cloneElement(child, {
                                        showSystemDialog,
                                        completeTool: handleToolComplete
                                    });
                                }
                                return child;
                            });
                        }
                        return instanceRef.current;
                    })()}
                </div>
            </motion.div>

            {/* Tool Footer (Optional Tip) */}
            <div className="bg-white/5 border border-white/5 rounded-2xl p-4 flex items-center gap-4 text-xs text-gray-500">
                <div className="w-8 h-8 rounded-lg bg-neon-blue/10 flex items-center justify-center text-neon-blue">
                    <Info size={14} />
                </div>
                <span>SYSTEM NOTIFICATION: Integration complete. Awaiting input.</span>
            </div>

            <SystemDialogPanel
                active={dialog.active}
                message={dialog.message}
                type={dialog.type}
                onClose={() => setDialog(prev => ({ ...prev, active: false }))}
            />
        </div>
    );
});

export default ToolLayout;
