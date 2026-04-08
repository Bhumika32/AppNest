import { create } from 'zustand';

export const ZONES = {
    ARCADE: "arcade",
    CLIMATE: "climate",
    HEALTH: "health",
    SOCIAL: "social"
};

export const useZoneStore = create((set) => ({
    zoneData: {
        [ZONES.CLIMATE]: {
            id: ZONES.CLIMATE,
            name: "Climate Nexus",
            description: "Manage environmental variables and sensory atmospheric data.",
            emoji: "CloudMoon",
            hint: "Control the sky",
            gradient: {
                dark: "from-blue-600 to-indigo-900",
                light: "from-blue-400 to-cyan-200"
            }
        },
        [ZONES.HEALTH]: {
            id: ZONES.HEALTH,
            name: "Vitality Core",
            description: "Optimize your biological vessel's telemetry and health stats.",
            emoji: "Smile",
            hint: "Purity of form",
            gradient: {
                dark: "from-emerald-600 to-teal-900",
                light: "from-emerald-400 to-green-200"
            }
        },
        [ZONES.ARCADE]: {
            id: ZONES.ARCADE,
            name: "Arcade Nest",
            description: "High-stakes neural simulations and interactive games.",
            emoji: "Gamepad2",
            hint: "High score is destiny",
            gradient: {
                dark: "from-purple-600 to-pink-900",
                light: "from-purple-400 to-rose-200"
            }
        },
        [ZONES.SOCIAL]: {
            id: ZONES.SOCIAL,
            name: "Social Mesh",
            description: "Connect with the collective and verify your neural links.",
            emoji: "Sparkles",
            hint: "Join the swarm",
            gradient: {
                dark: "from-amber-600 to-orange-900",
                light: "from-amber-400 to-yellow-200"
            }
        }
    },
    getAllZones: () => {
        const state = useZoneStore.getState();
        return Object.values(state.zoneData);
    }
}));
