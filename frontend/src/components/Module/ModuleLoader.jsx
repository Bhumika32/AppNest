import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useModuleStore } from '../../store/moduleStore.js';
import { moduleRegistry } from '../../registry/moduleRegistry.js';
import { Loader2, AlertCircle } from 'lucide-react';

const ModuleLoader = () => {
    const { slug } = useParams();
    const navigate = useNavigate();
    const { getModuleBySlug, fetchModules, modules, loading } = useModuleStore();
    const [entryId, setEntryId] = React.useState(null);
    const [startTime] = React.useState(Date.now());

    React.useEffect(() => {
        if (modules.length === 0) {
            fetchModules();
        }
    }, [modules.length, fetchModules]);

    const moduleData = getModuleBySlug(slug);
    const Component = moduleData ? moduleRegistry[moduleData.component_key] : null;

    // Track launch
    React.useEffect(() => {
        if (moduleData && !entryId) {
            const initiateTrack = async () => {
                const id = await useModuleStore.getState().trackLaunch(moduleData.id);
                setEntryId(id);
            };
            initiateTrack();
        }
    }, [moduleData, entryId]);

    // Track cleanup
    React.useEffect(() => {
        return () => {
            if (entryId) {
                const duration = Math.floor((Date.now() - startTime) / 1000);
                useModuleStore.getState().trackEnd(entryId, duration);
            }
        };
    }, [entryId, startTime]);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center h-[60vh]">
                <Loader2 className="animate-spin text-neon-blue mb-4" size={48} />
                <p className="text-gray-500 font-bold uppercase tracking-[0.2em] animate-pulse">Synchronizing Neural Link...</p>
            </div>
        );
    }

    if (!moduleData) {
        return (
            <div className="flex flex-col items-center justify-center h-[60vh] text-center px-4">
                <AlertCircle className="text-red-500 mb-6" size={64} />
                <h2 className="text-2xl font-black mb-2 uppercase tracking-tighter text-white">Access Denied</h2>
                <p className="text-gray-500 max-w-md mb-8">The requested module slug '{slug}' is not registered in the current sector.</p>
                <button
                    onClick={() => navigate('/dashboard')}
                    className="px-8 py-3 bg-white/5 border border-white/10 hover:bg-white/10 rounded-xl font-black text-white uppercase tracking-tighter transition-all"
                >
                    Back to Gateway
                </button>
            </div>
        );
    }

    if (!Component) {
        return (
            <div className="flex flex-col items-center justify-center h-[60vh] text-center px-4">
                <AlertCircle className="text-neon-pink mb-6" size={64} />
                <h2 className="text-2xl font-black mb-2 uppercase tracking-tighter text-white">Binary Missing</h2>
                <p className="text-gray-500 max-w-md mb-8">Registry key '{moduleData.component_key}' found, but the implementation is not mapped.</p>
                <button
                    onClick={() => navigate('/dashboard')}
                    className="px-8 py-3 bg-neon-pink/10 border border-neon-pink/20 text-neon-pink hover:bg-neon-pink/20 rounded-xl font-black uppercase tracking-tighter transition-all"
                >
                    Emergency Exit
                </button>
            </div>
        );
    }

    return (
        <React.Suspense fallback={
            <div className="flex items-center justify-center h-[60vh]">
                <Loader2 className="animate-spin text-neon-blue" size={32} />
            </div>
        }>
            <Component module={moduleData} />
        </React.Suspense>
    );
};

export default ModuleLoader;
