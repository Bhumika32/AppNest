import { Leaf } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

export function Footer() {
  const { isDark } = useTheme();

  return (
    <div
      className={`mt-16 border-t pt-6 flex items-center justify-between ${
        isDark ? "border-white/10" : "border-slate-900/10"
      }`}
    >
      <div
        className={`text-xs ${
          isDark ? "text-slate-400" : "text-slate-600"
        }`}
      >
        © {new Date().getFullYear()} AppNest
      </div>
      <div
        className={`flex items-center gap-2 text-xs ${
          isDark ? "text-slate-400" : "text-slate-600"
        }`}
      >
        <Leaf className="h-4 w-4" /> Adaptive Theme UI
      </div>
    </div>
  );
}
