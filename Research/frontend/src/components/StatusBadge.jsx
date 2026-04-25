const C = {
  intake:     'text-muted  bg-raised     border-border',
  uploading:  'text-amber-l bg-amber/10  border-amber/25',
  processing: 'text-accent  bg-accent/10 border-accent/25',
  running:    'text-accent  bg-accent/10 border-accent/25',
  complete:   'text-green-l bg-green/10  border-green/25',
  failed:     'text-red-l   bg-red/10    border-red/25',
  cancelled:  'text-amber-l bg-amber/10  border-amber/25',
}
const LABELS = {
  intake: 'Draft', uploading: 'Uploading', processing: 'Running',
  running: 'Running', complete: 'Complete', failed: 'Failed', cancelled: 'Cancelled',
}
const PULSE = new Set(['processing', 'running', 'uploading'])

export default function StatusBadge({ status }) {
  const cls = C[status] || C.intake
  const label = LABELS[status] || 'Draft'
  return (
    <span className={`badge border ${cls}`}>
      {PULSE.has(status) && (
        <span className={`w-[5px] h-[5px] rounded-full animate-pulse-dot ${C[status]?.includes('accent') ? 'bg-accent' : C[status]?.includes('amber') ? 'bg-amber' : 'bg-red'}`} />
      )}
      {label}
    </span>
  )
}
