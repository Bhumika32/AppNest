import { motion } from 'framer-motion';
import { useTheme } from '../../context/ThemeContext';

export function ZoneCard({ zone, zoneData, onClick }) {
  const { isDark } = useTheme();

  if (!zoneData) return null;

  const gradientClass = isDark ? zoneData.color.dark : zoneData.color.light;

  return (
    <motion.div
      whileHover={{ scale: 1.05, translateY: -8 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className="cursor-pointer"
    >
      <div
        className={`rounded-2xl overflow-hidden ${
          isDark
            ? 'bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-white/10'
            : 'bg-gradient-to-br from-white/80 to-slate-50/80 border border-slate-200/50'
        } p-6 shadow-lg hover:shadow-xl transition-all`}
      >
        {/* Background gradient */}
        <div
          className={`absolute inset-0 bg-gradient-to-br ${gradientClass} opacity-20`}
        />

        {/* Content */}
        <div className="relative z-10 space-y-4">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div className="text-4xl">{zoneData.emoji}</div>
            <span
              className={`px-3 py-1 rounded-full text-xs font-semibold ring-1 ${
                isDark
                  ? 'bg-white/10 text-slate-200 ring-white/20'
                  : 'bg-slate-900/10 text-slate-800 ring-slate-900/10'
              }`}
            >
              {isDark ? 'Realm' : 'Zone'}
            </span>
          </div>

          {/* Title and Description */}
          <div>
            <h3
              className={`text-xl font-bold mb-2 ${
                isDark ? 'text-white' : 'text-slate-900'
              }`}
            >
              {zoneData.name}
            </h3>
            <p
              className={`text-sm ${
                isDark ? 'text-slate-300' : 'text-slate-700'
              }`}
            >
              {zoneData.description}
            </p>
          </div>

          {/* Content Count */}
          <div className="flex gap-4 text-sm">
            {zoneData.tools && (
              <span className={isDark ? 'text-slate-400' : 'text-slate-600'}>
                {zoneData.tools.length} Tools
              </span>
            )}
            {zoneData.games && (
              <span className={isDark ? 'text-slate-400' : 'text-slate-600'}>
                {zoneData.games.length} Games
              </span>
            )}
          </div>

          {/* CTA */}
          <div className="pt-2">
            <button
              className={`w-full py-2 px-4 rounded-lg font-semibold text-sm transition-all ${
                isDark
                  ? `bg-gradient-to-r ${gradientClass} text-white hover:opacity-90`
                  : `bg-gradient-to-r ${gradientClass} text-white hover:opacity-90`
              }`}
            >
              Explore
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
