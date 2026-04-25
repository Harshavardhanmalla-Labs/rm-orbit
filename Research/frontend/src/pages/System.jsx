import { useEffect, useState } from 'react'
import { CheckCircle, XCircle, AlertTriangle, RefreshCw } from 'lucide-react'
import { api } from '../api/client.js'

function InfoRow({ label, value, mono, status }) {
  return (
    <div className="flex items-center justify-between py-2.5 border-b border-border last:border-0">
      <span className="text-[12px] text-muted">{label}</span>
      <span className={`text-[12px] font-semibold ${mono ? 'font-mono' : ''}
        ${status === 'ok' ? 'text-green-l' : status === 'bad' ? 'text-red-l' : 'text-text'}`}>
        {value ?? '—'}
      </span>
    </div>
  )
}

function AreaBar({ area }) {
  const c = area.percent >= 80 ? 'bg-green' : area.percent >= 60 ? 'bg-accent' : 'bg-amber'
  const t = area.percent >= 80 ? 'text-green-l' : area.percent >= 60 ? 'text-accent' : 'text-amber-l'
  return (
    <div className="flex items-center gap-3">
      <span className="text-[12px] text-muted w-[145px] shrink-0">{area.label}</span>
      <div className="flex-1 h-1.5 bg-border rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${c} transition-all duration-700`} style={{ width: `${area.percent}%` }} />
      </div>
      <span className={`text-[12px] font-bold tabular-nums w-8 text-right ${t}`}>{area.percent}%</span>
    </div>
  )
}

function CompRow({ comp }) {
  const ok = comp.status === 'ready'
  const Icon = ok ? CheckCircle : comp.required ? XCircle : AlertTriangle
  return (
    <div className="flex items-center gap-3 py-2.5 border-b border-border last:border-0">
      <Icon size={13} className={ok ? 'text-green-l' : comp.required ? 'text-red-l' : 'text-amber-l'} />
      <span className="text-[13px] text-text flex-1">{comp.name}</span>
      {comp.required && <span className="text-[10px] text-red bg-red/10 px-1.5 py-px rounded font-bold">REQ</span>}
      <span className={`text-[11px] font-semibold ${ok ? 'text-green-l' : 'text-muted'}`}>{comp.status}</span>
    </div>
  )
}

export default function System() {
  const [progress, setProgress] = useState(null)
  const [settings, setSettings] = useState(null)
  const [loading, setLoading] = useState(true)

  async function load() {
    setLoading(true)
    try {
      const [p, s] = await Promise.all([api.get('/api/system/progress'), api.get('/api/system/settings')])
      setProgress(p.data); setSettings(s.data)
    } catch (e) { console.error(e) }
    finally { setLoading(false) }
  }
  useEffect(() => { load() }, [])

  const brain = progress?.brain
  const pct = progress?.overall_percent || 0
  const oc  = pct >= 80 ? '#10b981' : pct >= 60 ? '#6366f1' : '#f59e0b'
  const r = 36
  const circ = 2 * Math.PI * r

  return (
    <div className="p-8 max-w-[960px]">
      <div className="flex items-center justify-between mb-7">
        <div>
          <h1 className="text-xl font-bold text-text">System Status</h1>
          <p className="text-[13px] text-muted mt-1">Platform readiness and configuration</p>
        </div>
        <button className="btn btn-ghost text-[12px]" onClick={load} disabled={loading}>
          <RefreshCw size={12} className={loading ? 'animate-spin' : ''} />
          Refresh
        </button>
      </div>

      {progress && (
        <div className="grid grid-cols-[140px_1fr] gap-5 mb-5">
          {/* Ring gauge */}
          <div className="card flex flex-col items-center justify-center p-5">
            <svg viewBox="0 0 90 90" className="w-20 h-20 -rotate-90">
              <circle cx="45" cy="45" r={r} fill="none" stroke="var(--color-border)" strokeWidth="7" />
              <circle cx="45" cy="45" r={r} fill="none" stroke={oc} strokeWidth="7"
                strokeLinecap="round"
                strokeDasharray={circ}
                strokeDashoffset={circ * (1 - pct / 100)}
                style={{ transition: 'stroke-dashoffset 0.8s ease' }}
              />
            </svg>
            <p className="text-lg font-bold mt-2" style={{ color: oc }}>{pct}%</p>
            <p className="text-[10px] text-muted">overall</p>
          </div>

          {/* Area bars */}
          <div className="card p-5 space-y-3.5">
            {progress.areas?.map(a => <AreaBar key={a.key} area={a} />)}
          </div>
        </div>
      )}

      <div className="grid grid-cols-2 gap-5">
        {brain?.components && (
          <div className="card p-5">
            <p className="section-title">Brain Components</p>
            {brain.components.map(c => <CompRow key={c.name} comp={c} />)}
            {brain.optional_missing?.length > 0 && (
              <p className="text-[11px] text-muted mt-3">Missing optional: {brain.optional_missing.join(', ')}</p>
            )}
          </div>
        )}

        {settings && (
          <div className="space-y-4">
            <div className="card p-5">
              <p className="section-title">LLM Configuration</p>
              <InfoRow label="Provider" value={settings.llm.provider} />
              <InfoRow label="Model" value={settings.llm.model} mono />
              <InfoRow label="Base URL" value={settings.llm.base_url} mono />
              <InfoRow label="Timeout" value={`${settings.llm.timeout_seconds}s`} />
              <InfoRow label="JSON repair" value={settings.llm.json_repair_attempts} />
              <InfoRow label="API key" value={settings.llm.api_key_set ? 'configured' : 'using default'} status={settings.llm.api_key_set ? 'ok' : ''} />
            </div>
            <div className="card p-5">
              <p className="section-title">Service URLs</p>
              <InfoRow label="GROBID" value={settings.services.grobid_url} mono />
              <InfoRow label="LanguageTool" value={settings.services.languagetool_url} mono />
              <InfoRow label="Nougat" value={settings.services.nougat_url} mono />
            </div>
          </div>
        )}
      </div>

      {progress?.blockers?.length > 0 && (
        <div className="card p-5 mt-5">
          <p className="section-title">Blockers to 100%</p>
          <ul className="space-y-2.5">
            {progress.blockers.map((b, i) => (
              <li key={i} className="flex items-start gap-3 text-[13px] text-muted">
                <span className="w-1.5 h-1.5 rounded-full bg-amber shrink-0 mt-2" />
                {b}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
