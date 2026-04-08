//frontend/src/engine/GameEngine.jsx

import React, { useState, useEffect } from 'react';
import { useModuleStore } from '../store/moduleStore.js';
import GameSetupModal from './GameSetupModal.jsx';
import BattleArenaLayout from './BattleArenaLayout.jsx';
import XPRewardOverlay from './XPRewardOverlay.jsx';
import { useUserStore } from '../store/userStore.js';
import { useOverlayStore } from '../store/overlayStore.js';
import RoastOverlay from './personality/RoastOverlay.jsx';
import { personalityEngine } from './personality/personalityEngine.js';
import ModuleExecutionService from '../api/moduleExecutionService.js';
import ErrorBoundary from '../components/ErrorBoundary.jsx';

const GameEngine = React.memo(({ module, children }) => {
    const trackLaunch = useModuleStore(state => state.trackLaunch);
    const trackEnd = useModuleStore(state => state.trackEnd);
    const fetchDashboard = useUserStore(state => state.fetchDashboard);
    const showOverlay = useOverlayStore(state => state.showOverlay);

    const sessionStartedRef = React.useRef(false);
    const completedRef = React.useRef(false);
    const moduleInstanceRef = React.useRef(null);

    const [engineState, setEngineState] = useState('SETUP');
    const [config, setConfig] = useState(null);
    const [xpData, setXpData] = useState(null);
    const [sessionStart, setSessionStart] = useState(null);
    const [entryId, setEntryId] = useState(null);
    const [roast, setRoast] = useState({ active: false, message: '' });

    const stableConfig = React.useMemo(() => config, [config]);

    useEffect(() => {
        if (sessionStartedRef.current) return;

        const caps = module.capabilities || {};

        if (caps.requiresSetup === false) {
            handleStart({});
        } else {
            setEngineState('SETUP');
        }
    }, [module.id]);

    const handleStart = async (selectedConfig) => {
        if (sessionStartedRef.current && engineState !== 'SETUP') return;

        sessionStartedRef.current = true;

        setConfig(selectedConfig);
        setSessionStart(Date.now());

        const id = await trackLaunch(module.id);

        // 🚨 CRITICAL: ensure session exists
        if (!id) {
            console.error("Failed to create session");
            sessionStartedRef.current = false;
            return;
        }

        setEntryId(id);
        setEngineState('PLAYING');
    };

    const handleEndGame = React.useCallback(async (resultData) => {
        if (completedRef.current) return;
        completedRef.current = true;

        const duration = Math.floor((Date.now() - sessionStart) / 1000);

        try {
            if (entryId) {
                await trackEnd(entryId, duration);
            }

            const res = await ModuleExecutionService.execute(module.slug, {
                module_id: module.id,
                duration,
                score: resultData.score || 0,
                mode: (config?.mode || 'SOLO').toLowerCase(),
                difficulty: (config?.difficulty || 'EASY').toLowerCase(),
                result: resultData.win ? 'win' : (resultData.result || 'completed'),
                metadata: resultData.metadata,
                entry_id: entryId,
                completed: true,
            });

            if (res?.lifecycle?.xp_reward) {
                setXpData(res.lifecycle.xp_reward);
                setEngineState('REWARD');
            } else {
                setEngineState('SETUP');
            }

            fetchDashboard();

            if (res?.roast) {
                setRoast({ active: true, message: res.roast });
                setTimeout(() => setRoast(prev => ({ ...prev, active: false })), 5000);
            }

            if (res?.advice) {
                setTimeout(() => {
                    showOverlay({
                        type: 'mentor_tip',
                        delivery: 'overlay',
                        message: res.advice,
                        icon: 'Lightbulb',
                        color: 'neon-blue',
                    });
                }, res?.roast ? 5500 : 0);
            }

        } catch (e) {
            console.error("Failed to complete module", e);
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
        sessionStartedRef.current = false;
        completedRef.current = false;

        setEngineState('SETUP');
        setConfig(null);
        setXpData(null);
    };

    const engineContext = React.useMemo(() => ({
        config,
        endGame: handleEndGame,
        showRoast,
        completedRef,
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
