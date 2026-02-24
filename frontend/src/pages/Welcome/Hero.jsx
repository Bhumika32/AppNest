import { motion } from 'framer-motion';
import { ArrowRight, ShieldCheck, Zap, Sparkles, Sun, Moon } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import { useNavigate } from 'react-router-dom';
import { Chip } from './Chip';

export function Hero() {
  const { isDark } = useTheme();
  const navigate = useNavigate();

  return (
    <div className="mt-16 grid gap-10 lg:grid-cols-2 lg:items-center">
      <div>
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-xs font-semibold ring-1 ${
            isDark
              ? "bg-white/5 text-slate-200 ring-white/10"
              : "bg-white/70 text-slate-700 ring-slate-900/10"
          }`}
        >
          {isDark ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
          {isDark ? "Welcome to the Realm" : "Welcome to the Shrine"}
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mt-5 text-4xl font-black tracking-tight sm:text-5xl"
        >
          Step into
          <span
            className={`block text-transparent bg-clip-text ${
              isDark
                ? "bg-gradient-to-r from-violet-400 via-fuchsia-400 to-cyan-300"
                : "bg-gradient-to-r from-amber-500 via-rose-500 to-fuchsia-500"
            }`}
          >
            AppNest
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className={`mt-4 max-w-xl text-base ${
            isDark ? "text-slate-300" : "text-slate-700"
          }`}
        >
          Mini tools, mini games, and mentors with personality. Whether you seek
          peaceful guidance or brutal honesty — AppNest adapts to your world.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-6 flex flex-wrap gap-3"
        >
          <button
            onClick={() => navigate('/login')}
            className={`group relative overflow-hidden rounded-2xl px-5 py-3 text-sm font-semibold text-white shadow-sm ${
              isDark
                ? "bg-gradient-to-r from-violet-600 via-fuchsia-600 to-cyan-500"
                : "bg-gradient-to-r from-amber-500 via-rose-500 to-fuchsia-500"
            }`}
          >
            <span className="relative inline-flex items-center gap-2">
              Enter AppNest <ArrowRight className="h-4 w-4" />
            </span>
          </button>

          <button
            onClick={() => navigate('/dashboard')}
            className={`rounded-2xl px-5 py-3 text-sm font-semibold ring-1 transition ${
              isDark
                ? "bg-white/5 ring-white/10 hover:bg-white/10"
                : "bg-white/80 ring-slate-900/10 hover:bg-white"
            }`}
          >
            Preview Tools
          </button>
        </motion.div>

        {/* Feature Chips */}
        <div className="mt-8 flex flex-wrap gap-3">
          <Chip icon={<ShieldCheck className="h-4 w-4" />} label="Secure Login" isDark={isDark} />
          <Chip icon={<Zap className="h-4 w-4" />} label="Instant Tools" isDark={isDark} />
          <Chip icon={<Sparkles className="h-4 w-4" />} label="Mentor System" isDark={isDark} />
        </div>
      </div>

      {/* Visual Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6 }}
        className="relative"
      >
        <div
          className={`rounded-[32px] p-6 shadow-sm ring-1 ${
            isDark
              ? "bg-white/5 ring-white/10"
              : "bg-white/70 ring-slate-900/10"
          }`}
        >
          <div className="text-sm font-black">Choose Your World</div>
          <div
            className={`mt-2 text-xs ${
              isDark ? "text-slate-400" : "text-slate-600"
            }`}
          >
            Light or dark — same tools, different vibe.
          </div>

          <div
            className={`mt-4 h-[260px] rounded-3xl grid place-items-center text-sm font-semibold ${
              isDark
                ? "bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 text-slate-300"
                : "bg-gradient-to-br from-amber-200 via-rose-200 to-fuchsia-200 text-slate-700"
            }`}
          >
            {isDark ? "🌙 Dark Moon Realm" : "🌸 Fantasy Shrine World"}
          </div>
        </div>
      </motion.div>
    </div>
  );
}
