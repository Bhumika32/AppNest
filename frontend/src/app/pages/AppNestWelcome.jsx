import React, { useEffect, useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useNavigate } from "react-router-dom";
import {
    ArrowRight,
    Sparkles,
    ShieldCheck,
    Zap,
    Radar,
    Moon,
    Sun,
    Skull,
    Gamepad2,
    Calculator,
    CloudMoon,
    Smile,
    MapPinned,
    Menu,
    X,
    User,
    LogOut
} from "lucide-react";

import { useZoneStore, ZONES } from "../../store/zoneStore";
import { useAuthStore } from "../../store/authStore.js";
import ZoneCard from "../../components/ZoneCard";

// Map Lucide icons from string names in store
const iconMap = {
    CloudMoon: <CloudMoon size={24} />,
    Calculator: <Calculator size={24} />,
    Sparkles: <Sparkles size={24} />,
    Zap: <Zap size={24} />,
    Gamepad2: <Gamepad2 size={24} />,
    Smile: <Smile size={24} />,
};

export default function AppNestWelcomePage() {
    const navigate = useNavigate();
    const [theme, setTheme] = useState("dark"); // 'dark' | 'light'
    const isDark = theme === "dark";
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const { getAllZones } = useZoneStore();
    const allZones = getAllZones();
    const { isAuthenticated, logout, user } = useAuthStore();

    const [roastMode, setRoastMode] = useState(true);
    const [intensity, setIntensity] = useState(78);
    const [typingDone, setTypingDone] = useState(false);

    const roastLabel = useMemo(() => {
        if (!roastMode) return "Off";
        if (intensity <= 35) return "Soft 😏";
        if (intensity <= 75) return "Medium 😈";
        return "Savage 💀";
    }, [roastMode, intensity]);

    const mentorLines = useMemo(
        () => [
            "Welcome, rookie. AppNest isn't a toolbox… it's a trial.",
            "Pick a tool. Get results. Lose dignity. Repeat.",
            "This world runs on logic. Your excuses won't load here.",
            "Enter the dashboard. Don't embarrass yourself.",
        ],
        []
    );

    const [lineIndex, setLineIndex] = useState(0);

    useEffect(() => {
        const t = setInterval(() => {
            setTypingDone(false);
            setLineIndex((i) => (i + 1) % mentorLines.length);
        }, 5200);
        return () => clearInterval(t);
    }, [mentorLines.length]);

    const toggleTheme = () => setTheme(isDark ? "light" : "dark");

    // Persist welcome theme selection so auth pages can pick it up
    useEffect(() => {
        try {
            localStorage.setItem('appnest-theme', isDark ? 'dark-moon' : 'fantasy-shrine');
        } catch (e) {
            // ignore storage errors
        }
    }, [isDark]);

    const handleZoneClick = (zoneId) => {
        // Arcade Nest goes to Games Realm
        if (zoneId === ZONES.ARCADE) {
            navigate('/dashboard/games');
        } else {
            // Other zones (Climate, Health, etc.) go to Tool Realm with deep link
            navigate(`/dashboard/tools/${zoneId}`);
        }
    }

    return (
        <div
            className={`min-h-screen w-full transition-colors duration-500 overflow-x-hidden ${isDark ? "bg-[#05060d] text-slate-100" : "bg-[#fbf7f0] text-slate-900"
                }`}
        >
            {/* Background */}
            <div className="pointer-events-none fixed inset-0 overflow-hidden">
                {isDark ? <DarkBackground /> : <LightBackground />}
                <Portal isDark={isDark} />
            </div>

            <div className="relative mx-auto max-w-6xl px-4 py-8 sm:py-10">
                {/* HUD Header */}
                <header className="flex items-center justify-between relative z-50">
                    <div className="flex items-center gap-3">
                        <div
                            className={`h-10 w-10 sm:h-11 sm:w-11 rounded-2xl grid place-items-center ring-1 shadow-lg ${isDark
                                ? "bg-white/5 ring-white/10 shadow-violet-500/10"
                                : "bg-white/80 ring-slate-900/10 shadow-slate-200"
                                }`}
                        >
                            🪺
                        </div>
                        <div>
                            <div className="text-lg font-black tracking-tight">AppNest</div>
                            <div className={`text-[10px] sm:text-xs font-medium tracking-wide opacity-80 ${isDark ? "text-slate-400" : "text-slate-600"}`}>
                                {isDark ? "Dark Moon Realm" : "Fantasy Shrine World"}
                            </div>
                        </div>
                    </div>

                    {/* Desktop Nav */}
                    <div className="hidden md:flex items-center gap-3">
                        {isAuthenticated ? (
                            <div className="flex items-center gap-2 mr-2">
                                <span className="text-sm font-medium opacity-80">Hello, {user?.username || 'User'}</span>
                                <button
                                    onClick={logout}
                                    className={`rounded-2xl px-4 py-2 text-sm font-bold ring-1 transition-all ${isDark
                                        ? "bg-red-500/10 text-red-400 ring-red-500/20 hover:bg-red-500/20"
                                        : "bg-red-50 text-red-600 ring-red-200 hover:bg-red-100"
                                        }`}
                                >
                                    <LogOut size={16} />
                                </button>
                            </div>
                        ) : (
                            <>
                                <button
                                    onClick={() => navigate('/login')}
                                    className={`rounded-2xl px-5 py-2.5 text-sm font-bold ring-1 transition-all ${isDark
                                        ? "bg-white/5 text-slate-200 ring-white/10 hover:bg-white/10 hover:scale-105"
                                        : "bg-white text-slate-700 ring-slate-900/10 hover:bg-slate-50 hover:scale-105"
                                        }`}
                                >
                                    Login
                                </button>
                                <button
                                    onClick={() => navigate('/signup')}
                                    className={`rounded-2xl px-5 py-2.5 text-sm font-bold text-white shadow-lg transition-all hover:scale-105 hover:shadow-xl ${isDark
                                        ? "bg-gradient-to-r from-violet-600 via-fuchsia-600 to-cyan-500"
                                        : "bg-gradient-to-r from-amber-500 via-rose-500 to-fuchsia-500"
                                        }`}
                                >
                                    Sign up
                                </button>
                            </>
                        )}

                        <button
                            onClick={toggleTheme}
                            className={`h-10 w-10 rounded-2xl grid place-items-center ring-1 transition-all hover:scale-110 ${isDark
                                ? "bg-white/5 ring-white/10 hover:bg-white/10"
                                : "bg-white ring-slate-900/10 hover:bg-slate-50"
                                }`}
                        >
                            {isDark ? <Sun size={18} /> : <Moon size={18} />}
                        </button>
                    </div>

                    {/* Mobile Menu Toggle */}
                    <button
                        onClick={() => setIsMenuOpen(true)}
                        className="md:hidden p-2 rounded-xl bg-white/10 backdrop-blur-md"
                    >
                        <Menu size={24} />
                    </button>
                </header>

                {/* Mobile Drawer */}
                <AnimatePresence>
                    {isMenuOpen && (
                        <motion.div
                            initial={{ x: "100%" }}
                            animate={{ x: 0 }}
                            exit={{ x: "100%" }}
                            transition={{ type: "spring", stiffness: 300, damping: 30 }}
                            className={`fixed inset-y-0 right-0 z-[100] w-64 shadow-2xl p-6 flex flex-col gap-6 ${isDark ? "bg-[#0a0b14] border-l border-white/10" : "bg-white border-l border-slate-200"
                                }`}
                        >
                            <div className="flex justify-between items-center">
                                <span className="font-black text-xl">Menu</span>
                                <button onClick={() => setIsMenuOpen(false)} className="p-2 rounded-lg hover:bg-white/10">
                                    <X size={24} />
                                </button>
                            </div>

                            <div className="flex flex-col gap-3">
                                {isAuthenticated ? (
                                    <>
                                        <div className="p-4 rounded-xl bg-white/5 border border-white/10 mb-2">
                                            <div className="flex items-center gap-3">
                                                <div className="h-10 w-10 rounded-full bg-gradient-to-r from-violet-500 to-fuchsia-500 grid place-items-center text-white font-bold text-lg">
                                                    {user?.username?.[0] || 'U'}
                                                </div>
                                                <div>
                                                    <div className="font-bold">{user?.username || 'User'}</div>
                                                    <div className="text-xs opacity-60">Logged In</div>
                                                </div>
                                            </div>
                                        </div>
                                        <button
                                            onClick={logout}
                                            className="w-full py-3 rounded-xl font-bold bg-red-500/10 text-red-500 hover:bg-red-500/20 transition-colors flex items-center justify-center gap-2"
                                        >
                                            <LogOut size={18} /> Logout
                                        </button>
                                    </>
                                ) : (
                                    <>
                                        <button
                                            onClick={() => navigate('/login')}
                                            className={`w-full py-3 rounded-xl font-bold border transition-all ${isDark ? "border-white/20 hover:bg-white/5" : "border-slate-200 hover:bg-slate-50"
                                                }`}
                                        >
                                            Login
                                        </button>
                                        <button
                                            onClick={() => navigate('/signup')}
                                            className={`w-full py-3 rounded-xl font-bold text-white shadow-lg transition-all ${isDark
                                                ? "bg-gradient-to-r from-violet-600 via-fuchsia-600 to-cyan-500"
                                                : "bg-gradient-to-r from-amber-500 via-rose-500 to-fuchsia-500"
                                                }`}
                                        >
                                            Sign Up
                                        </button>
                                    </>
                                )}

                                <div className="h-px bg-white/10 my-2" />

                                <button
                                    onClick={toggleTheme}
                                    className={`w-full py-3 rounded-xl font-bold flex items-center justify-center gap-2 border transition-all ${isDark ? "border-white/20 hover:bg-white/5" : "border-slate-200 hover:bg-slate-50"
                                        }`}
                                >
                                    {isDark ? <Sun size={18} /> : <Moon size={18} />}
                                    {isDark ? "Light Mode" : "Dark Mode"}
                                </button>
                            </div>
                        </motion.div>
                    )}

                </AnimatePresence>


                {/* MAIN CONTENT */}
                <div className="mt-12 lg:mt-20 grid gap-12 lg:grid-cols-2 lg:items-center">
                    {/* Left Column: Hero Text */}
                    <div className="relative z-10">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6 }}
                            className={`inline-flex items-center gap-2 rounded-full px-4 py-1.5 text-xs font-bold tracking-wide ring-1 ${isDark
                                ? "bg-white/5 text-slate-200 ring-white/10"
                                : "bg-white/70 text-slate-700 ring-slate-900/10"
                                }`}
                        >
                            <Sparkles className="h-3.5 w-3.5" />
                            Next-Gen AI Platform
                        </motion.div>

                        <motion.h1
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.1 }}
                            className="mt-6 text-5xl sm:text-6xl lg:text-7xl font-black leading-[0.9] tracking-tight"
                        >
                            Step into <br />
                            <span
                                className={`text-transparent bg-clip-text ${isDark
                                    ? "bg-gradient-to-r from-violet-400 via-fuchsia-400 to-cyan-300"
                                    : "bg-gradient-to-r from-amber-500 via-rose-500 to-fuchsia-500"
                                    }`}
                            >
                                AppNest
                            </span>
                        </motion.h1>

                        <motion.p
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                            className={`mt-6 max-w-lg text-lg leading-relaxed ${isDark ? "text-slate-400" : "text-slate-600"}`}
                        >
                            A unified realm of intelligence. Tools that feel like magic,
                            games that test your wit, and a dashboard that thrives on your energy.
                        </motion.p>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.3 }}
                            className="mt-8 flex flex-wrap gap-2"
                        >
                            <HudChip isDark={isDark} icon={<ShieldCheck />} label="Secure" />
                            <HudChip isDark={isDark} icon={<Zap />} label="Instant" />
                            <HudChip isDark={isDark} icon={<Radar />} label="World Map" />
                            <HudChip isDark={isDark} icon={<Skull />} label={`Roast: ${roastLabel}`} />
                        </motion.div>

                        {/* Mentor Box */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.6, delay: 0.4 }}
                            className={`mt-8 max-w-md rounded-[24px] p-6 ring-1 backdrop-blur-md ${isDark
                                ? "bg-white/5 ring-white/10 shadow-xl shadow-violet-900/10"
                                : "bg-white/80 ring-slate-900/10 shadow-xl shadow-slate-200"
                                }`}
                        >
                            <TypewriterText
                                key={lineIndex}
                                text={`“${mentorLines[lineIndex]}”`}
                                speed={22}
                                onDone={() => setTypingDone(true)}
                                isDark={isDark}
                            />

                            <div className="mt-5 flex items-center justify-between pt-4 border-t border-white/5">
                                <label className="flex items-center gap-2 text-xs font-bold cursor-pointer select-none">
                                    <input
                                        type="checkbox"
                                        className="accent-violet-500 h-4 w-4"
                                        checked={roastMode}
                                        onChange={(e) => setRoastMode(e.target.checked)}
                                    />
                                    <span>Roast Mode</span>
                                </label>

                                <motion.button
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    onClick={() => {
                                        if (isAuthenticated) {
                                            navigate('/dashboard');
                                        } else {
                                            navigate('/login');
                                        }
                                    }}
                                    className={`rounded-xl px-5 py-2.5 text-sm font-bold text-white shadow-lg ${isDark
                                        ? "bg-gradient-to-r from-violet-600 via-fuchsia-600 to-cyan-500 shadow-violet-500/20"
                                        : "bg-gradient-to-r from-amber-500 via-rose-500 to-fuchsia-500 shadow-orange-500/20"
                                        }`}
                                >
                                    Enter Dashboard <ArrowRight className="h-4 w-4 inline ml-1" />
                                </motion.button>
                            </div>
                        </motion.div>
                    </div>

                    {/* Right Column: Dynamic Zone Grid */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                        className="relative z-10"
                    >
                        <div
                            className={`rounded-[32px] p-6 sm:p-8 ring-1 backdrop-blur-xl ${isDark
                                ? "bg-white/5 ring-white/10 shadow-2xl shadow-black/50"
                                : "bg-white/60 ring-slate-900/5 shadow-2xl shadow-slate-200/50"
                                }`}
                        >
                            <div className="flex items-center justify-between mb-6">
                                <div>
                                    <div className="text-sm font-black uppercase tracking-widest">World Map</div>
                                    <div className={`text-xs mt-1 ${isDark ? "text-slate-400" : "text-slate-500"}`}>
                                        Select a Zone to Explore
                                    </div>
                                </div>
                                <span
                                    className={`px-3 py-1 rounded-full text-[10px] font-bold border ${isDark ? "bg-white/5 border-white/10" : "bg-white border-slate-200"}`}
                                >
                                    {allZones.length} Active Zones
                                </span>
                            </div>

                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                                {allZones.map((zone, idx) => (
                                    <ZoneCard
                                        key={zone.id}
                                        title={zone.name}
                                        subtitle={zone.description}
                                        icon={iconMap[zone.emoji] || <Sparkles size={24} />}
                                        hint={zone.hint}
                                        color={isDark ? zone.gradient.dark : zone.gradient.light}
                                        isDark={isDark}
                                        delay={idx * 0.1}
                                        onClick={() => handleZoneClick(zone.id)}
                                    />
                                ))}
                            </div>

                        </div>
                    </motion.div>

                </div>
            </div>
        </div>
    );
}

// --- Helper Components ---

function HudChip({ icon, label, isDark }) {
    return (
        <span
            className={`inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-[11px] font-bold tracking-wide ring-1 ${isDark
                ? "bg-white/5 text-slate-300 ring-white/10"
                : "bg-white/70 text-slate-700 ring-slate-900/10"
                }`}
        >
            <span className="h-5 w-5 grid place-items-center opacity-70">{icon}</span>
            {label}
        </span>
    );
}

function DarkBackground() {
    return (
        <>
            <div className="absolute inset-0 bg-gradient-to-b from-[#060719] via-[#040510] to-[#02030a]" />
            <div className="absolute top-[-10%] left-[20%] h-[600px] w-[600px] rounded-full bg-violet-600/20 blur-[120px]" />
            <div className="absolute bottom-[-10%] right-[10%] h-[500px] w-[500px] rounded-full bg-cyan-600/10 blur-[100px]" />
        </>
    );
}

function LightBackground() {
    return (
        <>
            <div className="absolute inset-0 bg-gradient-to-b from-[#fff7e8] via-[#fbf7f0] to-[#f6f1ff]" />
            <div className="absolute top-[-10%] left-[20%] h-[600px] w-[600px] rounded-full bg-amber-300/40 blur-[120px]" />
            <div className="absolute bottom-[-10%] right-[10%] h-[500px] w-[500px] rounded-full bg-rose-300/30 blur-[100px]" />
        </>
    );
}

function Portal({ isDark }) {
    return (
        <motion.div
            className="absolute left-1/2 top-[30%] -translate-x-1/2 -z-10 opacity-60"
            animate={{ scale: [1, 1.1, 1], rotate: [0, 5, -5, 0] }}
            transition={{ repeat: Infinity, duration: 15, ease: "linear" }}
        >
            <div className="relative h-[600px] w-[600px] rounded-full">
                <div
                    className={`absolute inset-0 rounded-full blur-3xl ${isDark
                        ? "bg-gradient-to-br from-violet-500/20 via-fuchsia-500/10 to-transparent"
                        : "bg-gradient-to-br from-amber-400/20 via-rose-400/10 to-transparent"
                        }`}
                />
            </div>
        </motion.div>
    );
}

function TypewriterText({ text, speed = 20, onDone, isDark }) {
    const [out, setOut] = useState("");

    useEffect(() => {
        let i = 0;
        setOut("");
        const t = setInterval(() => {
            i++;
            setOut(text.slice(0, i));
            if (i >= text.length) {
                clearInterval(t);
                onDone?.();
            }
        }, speed);
        return () => clearInterval(t);
    }, [text, speed, onDone]);

    return (
        <div className={`text-sm font-medium leading-relaxed italic ${isDark ? "text-slate-300" : "text-slate-600"}`}>
            {out}
            <span className={`ml-1 inline-block h-4 w-[2px] animate-pulse ${isDark ? "bg-cyan-400" : "bg-fuchsia-500"}`} />
        </div>
    );
}
