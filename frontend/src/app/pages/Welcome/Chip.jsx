export function Chip({ icon, label, isDark }) {
  return (
    <span
      className={`inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-[11px] font-semibold ring-1 ${
        isDark
          ? "bg-white/5 text-slate-200 ring-white/10"
          : "bg-white/70 text-slate-800 ring-slate-900/10"
      }`}
    >
      <span
        className={`inline-flex h-6 w-6 items-center justify-center rounded-full ring-1 ${
          isDark ? "bg-white/5 ring-white/10" : "bg-white ring-slate-900/10"
        }`}
      >
        {icon}
      </span>
      {label}
    </span>
  );
}
