import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useModuleStore } from '../../store/moduleStore.js';
import { moduleRegistry } from '../../registry/moduleRegistry.js';
import { Loader2, AlertCircle } from 'lucide-react';
import ToolLayout from '../../layout/Module/ToolLayout.jsx';
import GameEngine from '../../game-engine/GameEngine.jsx';

const ModuleLoader = () => {
    const { slug } = useParams();
    const navigate = useNavigate();
    const getModuleBySlug = useModuleStore(state => state.getModuleBySlug);
    const fetchModules = useModuleStore(state => state.fetchModules);
    const modules = useModuleStore(state => state.modules);
    const loading = useModuleStore(state => state.loading);

    // Instance isolation
    const moduleRef = React.useRef(null);
    const currentSlugRef = React.useRef(null);

    React.useEffect(() => {
        if (modules.length === 0) {
            fetchModules();
        }
    }, [modules.length, fetchModules]);

    const moduleData = getModuleBySlug(slug);
    const Component = moduleData ? moduleRegistry[moduleData.component_key] : null;

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
        // Fallback for when the registry doesn't have the component
        const SafeFallback = () => (
            <div className="flex flex-col items-center justify-center p-12 text-center h-full bg-dark-surface/50 border-2 border-dashed border-neon-pink/30 rounded-3xl">
                <AlertCircle className="text-neon-pink mb-4" size={48} />
                <h3 className="text-xl font-black mb-2 uppercase tracking-tight text-white">Module Unavailable</h3>
                <p className="text-gray-400 max-w-sm mb-6 text-sm">
                    This module (<code>{moduleData.component_key}</code>) is registered in the sector database but the binary payload is not mapped in the frontend chassis.
                </p>
                <div className="flex gap-4">
                    <button
                        onClick={() => navigate('/dashboard')}
                        className="px-6 py-2 bg-white/5 border border-white/10 hover:bg-white/10 rounded-lg text-xs font-black text-white uppercase tracking-wider transition-all"
                    >
                        Return to Dashboard
                    </button>
                </div>
            </div>
        );

        moduleRef.current = <SafeFallback />;
        return <SafeFallback />;
    }

    return (
        <React.Suspense fallback={
            <div className="flex items-center justify-center h-[60vh]">
                <Loader2 className="animate-spin text-neon-blue" size={32} />
            </div>
        }>
            {(() => {
                // If the slug changed, we must reset the persistent instance
                if (currentSlugRef.current !== slug) {
                    moduleRef.current = null;
                    currentSlugRef.current = slug;
                }

                if (!moduleRef.current) {
                    const content = moduleData.type === 'game' ? (
                        <GameEngine key={moduleData.slug} module={moduleData}>
                            <Component />
                        </GameEngine>
                    ) : moduleData.type === 'tool' ? (
                        <ToolLayout key={moduleData.slug} module={moduleData}>
                            <Component />
                        </ToolLayout>
                    ) : (
                        <Component key={moduleData.slug} module={moduleData} />
                    );

                    moduleRef.current = content;
                }

                return moduleRef.current;
            })()}
        </React.Suspense>
    );
};

export default React.memo(ModuleLoader);
