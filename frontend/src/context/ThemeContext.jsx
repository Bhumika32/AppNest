import React, { createContext, useContext, useState, useEffect } from 'react';
import useThemeStore from '../store/themeStore';

const ThemeContext = createContext();

export const THEMES = {
  DARK_MOON: 'dark-moon',      // Dark Mode
  FANTASY_SHRINE: 'fantasy-shrine', // Light Mode
};

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(THEMES.FANTASY_SHRINE);
  const [mounted, setMounted] = useState(false);

  // Dashboard store (proxied)
  const { currentThemeId, setTheme: setDashboardTheme, currentTheme, getAllThemes } = useThemeStore();

  // Load theme from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('appnest-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme) {
      // Accept both legacy short values and canonical ones
      if (savedTheme === 'dark' || savedTheme === 'dark-moon') setTheme(THEMES.DARK_MOON);
      else setTheme(THEMES.FANTASY_SHRINE);
    } else {
      setTheme(prefersDark ? THEMES.DARK_MOON : THEMES.FANTASY_SHRINE);
    }
    setMounted(true);
  }, []);

  // Save theme to localStorage whenever it changes
  useEffect(() => {
    if (mounted) {
      localStorage.setItem('appnest-theme', theme);
    }
  }, [theme, mounted]);

  const isDark = theme === THEMES.DARK_MOON;
  const themeName = isDark ? 'Dark Moon Realm' : 'Fantasy Shrine World';

  const toggleTheme = () => {
    setTheme(prev => 
      prev === THEMES.DARK_MOON ? THEMES.FANTASY_SHRINE : THEMES.DARK_MOON
    );
  };

  const value = {
    theme,
    setTheme,
    isDark,
    themeName,
    toggleTheme,

    // Dashboard theme proxied from Zustand store
    dashboard: {
      id: currentThemeId,
      setDashboardTheme,
      currentDashboardTheme: currentTheme,
      dashboardThemes: getAllThemes(),
    }
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};
