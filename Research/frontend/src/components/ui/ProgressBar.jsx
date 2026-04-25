export default function ProgressBar({ value = 0, color = 'accent', label, showPct = false }) {
  const pct = Math.max(0, Math.min(100, value))
  const colorClasses = {
    accent: 'bg-accent',
    emerald: 'bg-emerald',
    amber: 'bg-amber',
    red: 'bg-red',
  }
  const barColor = colorClasses[color] || colorClasses.accent
  const glowShadow = color === 'accent' ? '0 0 6px rgba(99,102,241,0.4)' : 'none'

  return (
    <div className="space-y-1">
      {(label || showPct) && (
        <div className="flex justify-between text-[10px] text-muted">
          {label && <span>{label}</span>}
          {showPct && <span className="font-mono">{pct}%</span>}
        </div>
      )}
      <div className="h-1.5 bg-border rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${barColor}`}
          style={{
            width: `${pct}%`,
            boxShadow: glowShadow,
          }}
        />
      </div>
    </div>
  )
}
