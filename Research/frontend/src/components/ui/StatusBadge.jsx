export default function StatusBadge({ status }) {
  const configs = {
    intake:      { cls: 'bg-slate/10 text-slate-l border-slate/25',     label: 'Draft' },
    uploading:   { cls: 'bg-amber/10 text-amber-l border-amber/25',     label: 'Uploading' },
    processing:  { cls: 'bg-accent/10 text-accent border-accent/25',    label: 'Processing', pulse: true },
    running:     { cls: 'bg-accent/10 text-accent border-accent/25',    label: 'Running', pulse: true },
    complete:    { cls: 'bg-emerald/10 text-emerald-l border-emerald/25', label: 'Complete' },
    failed:      { cls: 'bg-red/10 text-red-l border-red/25',           label: 'Failed' },
    cancelled:   { cls: 'bg-blue/10 text-blue-l border-blue/25',        label: 'Cancelled' },
  }

  const key = (status || '').toLowerCase().replace('_', '')
  const config = configs[key] || configs.intake

  return (
    <span className={`inline-flex items-center gap-1.5 text-[11px] font-semibold px-2.5 py-1 rounded-full border ${config.cls}`}>
      {config.pulse && <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse-dot" />}
      {config.label}
    </span>
  )
}
