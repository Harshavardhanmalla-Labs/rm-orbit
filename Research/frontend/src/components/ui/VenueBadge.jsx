export default function VenueBadge({ venue }) {
  const venueMap = {
    ieee:    { label: 'IEEE', color: 'bg-blue/10 text-blue-l border-blue/25' },
    acm:     { label: 'ACM', color: 'bg-red/10 text-red-l border-red/25' },
    arxiv:   { label: 'arXiv', color: 'bg-amber/10 text-amber-l border-amber/25' },
    nature:  { label: 'Nature', color: 'bg-emerald/10 text-emerald-l border-emerald/25' },
    springer:{ label: 'Springer', color: 'bg-accent/10 text-accent border-accent/25' },
    custom:  { label: 'Custom', color: 'bg-slate/10 text-slate-l border-slate/25' },
  }

  const key = (venue || 'custom').toLowerCase()
  const config = venueMap[key] || venueMap.custom

  return (
    <span className={`inline-flex items-center text-[11px] font-semibold px-2.5 py-1 rounded-full border ${config.color}`}>
      {config.label}
    </span>
  )
}
