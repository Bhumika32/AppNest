import React, { useState, useEffect } from 'react';
import { useModuleStore } from '../store/moduleStore.js';
import GameSetupModal from './GameSetupModal.jsx';
import BattleArenaLayout from './BattleArenaLayout.jsx';
import XPRewardOverlay from './XPRewardOverlay.jsx';
import { useUserStore } from '../store/userStore.js';
import RoastOverlay from './personality/RoastOverlay.jsx';
import { personalityEngine } from './personality/personalityEngine.js';
import ModuleExecutionService from '../services/moduleExecutionService.js';
import ErrorBoundary from '../components/ErrorBoundary.jsx';

const GameEngine = React.memo(({ module, children }) => {
    const trackLaunch = useModuleStore(state => state.trackLaunch);
    const trackEnd = useModuleStore(state => state.trackEnd);
    const fetchDashboard = useUserStore(state => state.fetchDashboard);

    const sessionStartedRef = React.useRef(false);
    const completedRef = React.useRef(false);
    const engineRef = React.useRef(null);
    const moduleInstanceRef = React.useRef(null);

    const [engineState, setEngineState] = useState('SETUP'); // SETUP, PLAYING, REWARD
    const [config, setConfig] = useState(null);
    const [xpData, setXpData] = useState(null);
    const [sessionStart, setSessionStart] = useState(null);
    const [entryId, setEntryId] = useState(null);
    const [roast, setRoast] = useState({ active: false, message: '' });

    const stableConfig = React.useMemo(() => config, [config]);

    useEffect(() => {
        if (sessionStartedRef.current) return;

        // If no setup needs to be done based on capabilities, skip directly to PLAYING
        const caps = module.capabilities || {};
        if (!caps.supportsDifficulty && !caps.supportsAI && !caps.supportsPVP) {
            handleStart({});
        }
    }, [module.id]); // Only depend on internal stable ID

    const handleStart = async (selectedConfig) => {
        if (sessionStartedRef.current && engineState !== 'SETUP') return;
        sessionStartedRef.current = true;

        setConfig(selectedConfig);
        setSessionStart(Date.now());
        const id = await trackLaunch(module.id);
        setEntryId(id);
        setEngineState('PLAYING');
    };

    const handleEndGame = React.useCallback(async (resultData) => {
        if (completedRef.current) return;
        completedRef.current = true;

        const duration = Math.floor((Date.now() - sessionStart) / 1000);

        // Finalize analytics tracking
        if (entryId) {
            await trackEnd(entryId, duration);
        }

        // Trigger lifecycle complete
        try {
            const res = await ModuleExecutionService.execute(module.slug, {
                module_id: module.id,
                duration: duration,
                score: resultData.score || 0,
                difficulty: config?.difficulty || 'EASY',
                result: resultData.win ? 'win' : (resultData.result || 'completed'),
                metadata: resultData.metadata,
                entry_id: entryId
            });

            if (res?.lifecycle?.xp_reward) {
                setXpData(res.lifecycle.xp_reward);
                setEngineState('REWARD');
                fetchDashboard(); // Refresh header user info
            } else {
                // If it doesn't give XP for some reason (maybe a tool?) just finish
                // Could route them or reset
                setEngineState('SETUP');
            }
        } catch (e) {
            console.error("Failed to complete module", e);
            // Handle error state or just return to setup
            setEngineState('SETUP');
        }
    }, [config, entryId, fetchDashboard, module.id, module.slug, sessionStart, trackEnd]);

    const showRoast = React.useCallback((eventCategory) => {
        const msg = personalityEngine.getGameRoast(eventCategory);
        if (!msg) return;
        setRoast({ active: true, message: msg });
        setTimeout(() => setRoast(prev => ({ ...prev, active: false })), 3500);
    }, []);

    const handleRewardClose = () => {
        // Reset refs for next potential session if they stay on page
        sessionStartedRef.current = false;
        completedRef.current = false;

        setEngineState('SETUP');
        setConfig(null);
        setXpData(null);
    };

    // We use React.Children.map to inject the "engine" context into the children
    // So the game itself can call engine.endGame({ score, win, etc.. })
    const engineContext = React.useMemo(() => ({
        config, // This is null until handleStart
        endGame: handleEndGame,
        showRoast: showRoast
    }), [config, handleEndGame, showRoast]);

    return (
        <div className="game-engine-root w-full h-full relative">
            {engineState === 'SETUP' && (
                <GameSetupModal module={module} onStart={handleStart} />
            )}

            {(engineState === 'PLAYING' || engineState === 'REWARD') && (
                <BattleArenaLayout module={module} config={stableConfig}>
                    <ErrorBoundary onReset={() => setEngineState('SETUP')}>
                        {(() => {
                            if (!moduleInstanceRef.current) {
                                moduleInstanceRef.current = React.Children.map(children, child => {
                                    if (React.isValidElement(child)) {
                                        return React.cloneElement(child, { engine: engineContext });
                                    }
                                    return child;
                                });
                            }
                            return moduleInstanceRef.current;
                        })()}
                    </ErrorBoundary>
                </BattleArenaLayout>
            )}

            {engineState === 'REWARD' && xpData && (
                <XPRewardOverlay xpData={xpData} onClose={handleRewardClose} />
            )}

            <RoastOverlay
                active={roast.active}
                message={roast.message}
                onClose={() => setRoast(prev => ({ ...prev, active: false }))}
            />
        </div>
    );
});

export default GameEngine;
