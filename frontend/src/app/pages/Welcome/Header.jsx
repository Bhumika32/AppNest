import { motion } from 'framer-motion';
import { Sun, Moon, User, BarChart3 } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import useAuthStore from '../../store/authStore';
import { useNavigate } from 'react-router-dom';
import { MobileMenu } from '../../components/MobileMenu';

export function Header() {
  const { isDark, toggleTheme, themeName } = useTheme();
  const { isAuthenticated } = useAuthStore();
  const navigate = useNavigate();

  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div
          className={`h-11 w-11 rounded-2xl grid place-items-center ring-1 ${
            isDark
              ? "bg-white/5 ring-white/10"
              : "bg-white/70 ring-slate-900/10"
          }`}
        >
          🪺
        </div>
        <div>
          <div className="text-lg font-black">AppNest</div>
          <div
            className={`text-xs ${
              isDark ? "text-slate-400" : "text-slate-600"
            }`}
          >
            {themeName}
          </div>
        </div>
      </div>

      {/* Desktop Controls */}
      <div className="hidden lg:flex items-center gap-3">
        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className={`group relative flex h-10 w-10 items-center justify-center rounded-2xl ring-1 transition-all duration-300 ${
            isDark
              ? "bg-white/5 ring-white/10 hover:bg-white/10"
              : "bg-white ring-slate-900/10 hover:bg-slate-50"
          }`}
          aria-label="Toggle theme"
          title={isDark ? "Switch to Fantasy Shrine" : "Switch to Dark Moon"}
        >
          <span
            className={`absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition ${
              isDark
                ? "bg-gradient-to-br from-violet-600/20 via-fuchsia-600/10 to-cyan-500/10"
                : "bg-gradient-to-br from-amber-400/25 via-rose-400/20 to-fuchsia-400/20"
            }`}
          />
          <span className="relative">
            {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </span>
        </button>

        {/* Profile / Login Buttons */}
        {isAuthenticated ? (
          <button
            onClick={() => navigate('/profile')}
            className={`group relative flex h-10 w-10 items-center justify-center rounded-2xl ring-1 transition-all duration-300 ${
              isDark
                ? "bg-violet-600/20 ring-violet-500/50 hover:bg-violet-600/30"
                : "bg-amber-500/20 ring-amber-500/50 hover:bg-amber-500/30"
            }`}
            title="Profile"
          >
            <User className="h-5 w-5" />
          </button>
        ) : (
          <>
            <button
              onClick={() => navigate('/login')}
              className={`rounded-2xl px-4 py-2 text-sm font-semibold ${
                isDark
                  ? "text-slate-200 border border-white/20 hover:bg-white/5"
                  : "text-slate-700 border border-slate-300 hover:bg-slate-100"
              }`}
            >
              Login
            </button>
            <button
              onClick={() => navigate('/signup')}
              className={`rounded-2xl px-4 py-2 text-sm font-semibold text-white shadow-sm ${
                isDark
                  ? "bg-gradient-to-r from-violet-600 via-fuchsia-600 to-cyan-500"
                  : "bg-gradient-to-r from-amber-500 via-rose-500 to-fuchsia-500"
              }`}
            >
              Sign up
            </button>
          </>
        )}
      </div>

      {/* Mobile Menu */}
      <div className="lg:hidden">
        <MobileMenu />
      </div>
    </div>
  );
}
