import { useEffect, useState } from 'react'
import { api } from '../api/client.js'

const STATUS = {
  ready:     { label: 'Brain ready',    color: 'text-green-l',  dot: 'bg-green' },
  degraded:  { label: 'Brain degraded', color: 'text-amber-l',  dot: 'bg-amber', pulse: true },
  not_ready: { label: 'Brain offline',  color: 'text-red-l',    dot: 'bg-red',   pulse: true },
}

export default function BrainStatus({ compact }) {
  const [brain, setBrain] = useState(null)

  useEffect(() => {
    let on = true
    const load = () => api.get('/api/system/brain')
      .then(r => { if (on) setBrain(r.data) })
      .catch(() => { if (on) setBrain({ status: 'not_ready' }) })
    load()
    const t = setInterval(load, 30000)
    return () => { on = false; clearInterval(t) }
  }, [])

  const s = STATUS[brain?.status] || STATUS.not_ready
  const missing = brain?.optional_missing?.length
    ? `Missing: ${brain.optional_missing.join(', ')}`
    : s.label

  return (
    <div className="flex items-center gap-2" title={missing}>
      <span className={`w-[7px] h-[7px] rounded-full shrink-0 ${s.dot} ${s.pulse ? 'animate-pulse-dot' : ''}`} />
      <span className={`text-[11px] font-medium ${s.color}`}>{s.label}</span>
    </div>
  )
}
