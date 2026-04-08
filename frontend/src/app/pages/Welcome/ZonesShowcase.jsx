import { motion } from 'framer-motion';
import { useTheme } from '../../context/ThemeContext';
import { useZoneStore, ZONES } from '../../store/zoneStore';
import { ZoneCard } from './ZoneCard';

export function ZonesShowcase() {
  const { isDark } = useTheme();
  const { zoneData } = useZoneStore();

  const zones = Object.values(ZONES);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="mt-20 py-12"
    >
      <div className="mb-12">
        <h2
          className={`text-3xl font-black mb-4 ${
            isDark ? 'text-slate-100' : 'text-slate-900'
          }`}
        >
          Explore Your World
        </h2>
        <p
          className={`text-lg max-w-2xl ${
            isDark ? 'text-slate-300' : 'text-slate-700'
          }`}
        >
          Each zone offers unique tools and experiences. Pick a zone to get started or explore all realms in your dashboard.
        </p>
      </div>

      {/* Zones Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {zones.map((zone) => (
          <ZoneCard
            key={zone}
            zone={zone}
            zoneData={zoneData[zone]}
            onClick={() => {
              // Will add navigation later
            }}
          />
        ))}
      </div>
    </motion.div>
  );
}
