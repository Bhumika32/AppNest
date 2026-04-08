import { motion, AnimatePresence } from 'framer-motion';
import { X, Menu, Moon, Sun, LogIn, UserPlus, Explore } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import useAuthStore from '../store/authStore';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

export function MobileMenu() {
  const [isOpen, setIsOpen] = useState(false);
  const { isDark, toggleTheme } = useTheme();
  const { isAuthenticated, logout } = useAuthStore();
  const navigate = useNavigate();

  const menuItems = [
    {
      label: 'Explore Tools',
      icon: <Explore className="w-5 h-5" />,
      action: () => {
        navigate(isAuthenticated ? '/dashboard' : '/');
        setIsOpen(false);
      },
    },
    {
      label: isAuthenticated ? 'Profile' : 'Login',
      icon: isAuthenticated ? <UserPlus className="w-5 h-5" /> : <LogIn className="w-5 h-5" />,
      action: () => {
        if (isAuthenticated) {
          navigate('/profile');
        } else {
          navigate('/login');
        }
        setIsOpen(false);
      },
    },
    ...(isAuthenticated
      ? [
          {
            label: 'Logout',
            icon: <LogIn className="w-5 h-5 rotate-180" />,
            action: () => {
              logout();
              navigate('/');
              setIsOpen(false);
            },
          },
        ]
      : [
          {
            label: 'Sign Up',
            icon: <UserPlus className="w-5 h-5" />,
            action: () => {
              navigate('/signup');
              setIsOpen(false);
            },
          },
        ]),
  ];

  return (
    <>
      {/* Menu Button - visible on mobile only */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden relative z-50 p-2"
        aria-label="Toggle menu"
      >
        <AnimatePresence mode="wait">
          {isOpen ? (
            <motion.div
              key="close"
              initial={{ rotate: -90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: 90, opacity: 0 }}
              transition={{ duration: 0.2 }}
            >
              <X className={`w-6 h-6 ${isDark ? 'text-white' : 'text-slate-900'}`} />
            </motion.div>
          ) : (
            <motion.div
              key="menu"
              initial={{ rotate: 90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: -90, opacity: 0 }}
              transition={{ duration: 0.2 }}
            >
              <Menu className={`w-6 h-6 ${isDark ? 'text-white' : 'text-slate-900'}`} />
            </motion.div>
          )}
        </AnimatePresence>
      </button>

      {/* Overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsOpen(false)}
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* Drawer */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 20 }}
            className={`fixed right-0 top-0 bottom-0 w-3/4 max-w-sm z-40 lg:hidden ${
              isDark
                ? 'bg-[#05060d] border-l border-white/10'
                : 'bg-[#fbf7f0] border-l border-slate-200'
            }`}
          >
            <div className="p-6 space-y-6 h-full flex flex-col">
              {/* Header */}
              <div>
                <h2 className={`text-2xl font-black ${isDark ? 'text-white' : 'text-slate-900'}`}>
                  Menu
                </h2>
              </div>

              {/* Menu Items */}
              <nav className="space-y-2 flex-1">
                {menuItems.map((item, idx) => (
                  <motion.button
                    key={idx}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    onClick={item.action}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                      isDark
                        ? 'hover:bg-white/5 text-slate-100'
                        : 'hover:bg-slate-900/5 text-slate-900'
                    }`}
                  >
                    {item.icon}
                    <span className="font-semibold">{item.label}</span>
                  </motion.button>
                ))}
              </nav>

              {/* Theme Toggle */}
              <button
                onClick={toggleTheme}
                className={`w-full flex items-center justify-center gap-2 py-3 px-4 rounded-lg font-semibold transition-colors ${
                  isDark
                    ? 'bg-white/10 text-white hover:bg-white/20'
                    : 'bg-slate-900/10 text-slate-900 hover:bg-slate-900/20'
                }`}
              >
                {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                {isDark ? 'Fantasy Shrine' : 'Dark Moon'}
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
