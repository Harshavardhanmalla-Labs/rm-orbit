import BrainStatus from '../BrainStatus'

export default function MetricsStrip({ papers = [], brain = null }) {
  const counts = {
    total:     papers.length,
    complete:  papers.filter(p => p.status === 'complete').length,
    running:   papers.filter(p => ['processing', 'running'].includes(p.status)).length,
    failed:    papers.filter(p => p.status === 'failed').length,
    draft:     papers.filter(p => p.status === 'intake').length,
    cancelled: papers.filter(p => p.status === 'cancelled').length,
  }

  const metrics = [
    { key: 'total', label: 'Total', value: counts.total, color: 'text-text' },
    { key: 'complete', label: 'Complete', value: counts.complete, color: 'text-emerald-l' },
    { key: 'running', label: 'Running', value: counts.running, color: 'text-accent' },
    { key: 'failed', label: 'Failed', value: counts.failed, color: 'text-red-l' },
    { key: 'draft', label: 'Draft', value: counts.draft, color: 'text-slate-l' },
    { key: 'cancelled', label: 'Cancelled', value: counts.cancelled, color: 'text-blue-l' },
  ]

  return (
    <div className="flex gap-3 items-stretch">
      {metrics.map(metric => (
        <div
          key={metric.key}
          className="flex-1 bg-surface rounded-xl border border-border px-4 py-3 flex flex-col items-center justify-center"
        >
          <p className={`text-2xl font-bold ${metric.color}`}>{metric.value}</p>
          <p className="text-[10px] text-muted uppercase tracking-wider mt-1">{metric.label}</p>
        </div>
      ))}

      {/* Brain status indicator */}
      <div className="bg-surface rounded-xl border border-border px-4 py-3 flex items-center gap-2 shrink-0">
        <BrainStatus compact />
      </div>
    </div>
  )
}
