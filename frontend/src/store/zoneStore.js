import { create } from 'zustand';

// --- Realm Constants ---
export const REALMS = {
  TOOLS: 'tools_realm',
  GAMES: 'games_realm',
  ROAST: 'roast_realm',
  PROFILE: 'profile_realm',
};

// --- Zone Constants (Sub-Realms) ---
export const ZONES = {
  // Tools Realm Zones
  CLIMATE: 'climate_zone',
  HEALTH: 'health_district',
  FORTUNE: 'fortune_shrine',
  UTILITY: 'utility_hub',

  // Games Realm specific "Zones" or Categories
  ARCADE: 'arcade_nest',
};

// --- Roast Constants ---
export const ROAST_MODES = {
  SIMPLE: 'simple',
  PERSONAL: 'personal',
  ULTRA: 'ultra',
};

// --- Data Hierarchy ---
export const REALM_DATA = {
  [REALMS.TOOLS]: {
    id: REALMS.TOOLS,
    name: "Tool Realm",
    description: "Essential utilities for daily life",
    path: "/dashboard/tools",
    zones: [ZONES.CLIMATE, ZONES.HEALTH, ZONES.FORTUNE, ZONES.UTILITY]
  },
  [REALMS.GAMES]: {
    id: REALMS.GAMES,
    name: "Game Realm",
    description: "Relax and challenge yourself",
    path: "/dashboard/games",
    zones: [ZONES.ARCADE]
  },
  [REALMS.ROAST]: {
    id: REALMS.ROAST,
    name: "Roast Realm",
    description: "AI Combat Interface",
    path: "/dashboard/roast",
    zones: [] // No sub-zones, just modes
  },
  [REALMS.PROFILE]: {
    id: REALMS.PROFILE,
    name: "Profile",
    description: "Identity & Stats",
    path: "/dashboard/profile",
    zones: []
  }
};

export const ZONE_DATA = {
  // --- Tools Realm Zones ---
  [ZONES.CLIMATE]: {
    id: ZONES.CLIMATE,
    name: 'Climate Zone',
    emoji: 'CloudMoon',
    description: 'Weather forecasts & sky observation',
    hint: 'observe the sky',
    gradient: {
      dark: 'from-blue-600 via-cyan-600 to-sky-500',
      light: 'from-blue-400 via-cyan-400 to-sky-300',
    },
    tools: [
      {
        id: 'weather',
        name: 'Weather Checker',
        icon: '🌤️',
        path: '/tools/weather',
        description: 'Real-time atmospheric analysis'
      },
    ],
  },
  [ZONES.HEALTH]: {
    id: ZONES.HEALTH,
    name: 'Health District',
    emoji: 'Calculator',
    description: 'BMI, Age & Wellness trackers',
    hint: 'numbers react',
    gradient: {
      dark: 'from-emerald-600 via-green-600 to-teal-500',
      light: 'from-emerald-400 via-green-400 to-teal-300',
    },
    tools: [
      { id: 'bmi', name: 'BMI Calculator', icon: '⚖️', path: '/tools/bmi', description: 'Body Mass Index Analysis' },
      { id: 'age', name: 'Age Generator', icon: '🎂', path: '/tools/age', description: 'Chronological Calculation' },
    ],
  },
  [ZONES.FORTUNE]: {
    id: ZONES.FORTUNE,
    name: 'Fortune Shrine',
    emoji: 'Sparkles',
    description: 'Rashi, Astrology & Luck',
    hint: 'paths unfold',
    gradient: {
      dark: 'from-amber-600 via-orange-600 to-yellow-500',
      light: 'from-amber-400 via-orange-400 to-yellow-300',
    },
    tools: [
      { id: 'rashi', name: 'Rashi Converter', icon: '♈', path: '/tools/rashi', description: 'Zodiac Alignment' },
    ],
  },
  [ZONES.UTILITY]: {
    id: ZONES.UTILITY,
    name: 'Utility Hub',
    emoji: 'Zap',
    description: 'Converters & Daily Tools',
    hint: 'clarity matters',
    gradient: {
      dark: 'from-slate-600 via-gray-600 to-zinc-500',
      light: 'from-slate-400 via-gray-400 to-zinc-300',
    },
    tools: [
      { id: 'currency', name: 'Currency Converter', icon: '💱', path: '/tools/currency', description: 'Global Exchange Rates' },
      { id: 'units', name: 'Unit Converter', icon: '📏', path: '/tools/units', description: 'Measurement Translation' },
    ],
  },

  // --- Games Realm Zones ---
  [ZONES.ARCADE]: {
    id: ZONES.ARCADE,
    name: 'Arcade Nest',
    emoji: 'Gamepad2',
    description: 'Legacy & Neo Games',
    hint: 'play wisely',
    gradient: {
      dark: 'from-purple-600 via-fuchsia-600 to-pink-500',
      light: 'from-purple-400 via-fuchsia-400 to-pink-300',
    },
    games: [
      {
        id: 'tictactoe',
        name: 'Tic Tac Toe',
        icon: '⭕',
        description: 'Strategic Grid Combat',
        modes: ['Easy', 'Medium', 'Hard']
      },
      {
        id: 'snake',
        name: 'Hungry Snake',
        icon: '🐍',
        description: 'Infinite Consumption loop',
        modes: ['Slow', 'Normal', 'Fast']
      },
      {
        id: 'brick',
        name: 'Brick Breaker',
        icon: '🧱',
        description: 'Structural Demolition',
        modes: ['Standard', 'Chaos']
      },
      {
        id: 'flappy',
        name: 'Flappy Bird',
        icon: '🐦',
        description: 'Gravity Defiance',
        modes: ['Normal', 'Hard']
      },
    ],
  },
};

export const useZoneStore = create((set, get) => ({
  realms: REALM_DATA,
  zones: ZONE_DATA,

  // Actions
  getRealm: (id) => REALM_DATA[id],
  getZone: (id) => ZONE_DATA[id],
  getAllZones: () => Object.values(ZONE_DATA),

  // Helper to find a zone by ID across all data
  findZoneById: (zoneId) => ZONE_DATA[zoneId],

  // Helper to find tool by ID
  findToolById: (toolId) => {
    for (const zone of Object.values(ZONE_DATA)) {
      if (zone.tools) {
        const tool = zone.tools.find(t => t.id === toolId);
        if (tool) return { tool, zone };
      }
    }
    return null;
  }
}));
