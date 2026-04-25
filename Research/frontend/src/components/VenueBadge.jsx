const MAP = {
  ieee:     { label: 'IEEE',    cls: 'text-blue-l   bg-blue/10   border-blue/25' },
  acm:      { label: 'ACM',    cls: 'text-red-l    bg-red/10    border-red/25' },
  arxiv:    { label: 'arXiv',  cls: 'text-[#fb923c] bg-[#f97316]/10 border-[#f97316]/25' },
  nature:   { label: 'Nature', cls: 'text-green-l  bg-green/10  border-green/25' },
  springer: { label: 'Springer',cls:'text-[#c084fc] bg-[#a855f7]/10 border-[#a855f7]/25' },
  custom:   { label: 'Custom', cls: 'text-muted    bg-raised     border-border' },
}

export default function VenueBadge({ venue }) {
  const key = String(venue || '').toLowerCase()
  const { label, cls } = MAP[key] || MAP.custom
  return <span className={`badge border ${cls}`}>{MAP[key]?.label || venue || '—'}</span>
}
