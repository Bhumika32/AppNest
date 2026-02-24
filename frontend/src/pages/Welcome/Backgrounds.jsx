// Background components for Welcome page

export function LightBackground() {
  return (
    <>
      <div className="absolute inset-0 bg-gradient-to-b from-[#fff7e8] via-[#fbf7f0] to-[#f6f1ff]" />
      <div className="absolute -top-40 -left-40 h-[520px] w-[520px] rounded-full bg-gradient-to-br from-amber-200/70 via-rose-200/50 to-fuchsia-200/40 blur-3xl" />
      <div className="absolute -bottom-44 -right-40 h-[560px] w-[560px] rounded-full bg-gradient-to-br from-emerald-200/50 via-sky-200/40 to-indigo-200/35 blur-3xl" />
    </>
  );
}

export function DarkBackground() {
  return (
    <>
      <div className="absolute inset-0 bg-gradient-to-b from-[#060719] via-[#040510] to-[#02030a]" />
      <div className="absolute -top-32 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-gradient-to-br from-violet-500/25 via-fuchsia-500/12 to-cyan-400/10 blur-3xl" />
      <div className="absolute -bottom-44 left-1/2 h-[560px] w-[960px] -translate-x-1/2 rounded-full bg-gradient-to-r from-slate-900/60 via-indigo-500/12 to-slate-900/60 blur-3xl" />
    </>
  );
}
