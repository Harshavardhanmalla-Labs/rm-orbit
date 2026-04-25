import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import {
  Shield, UploadCloud, Map, Lightbulb, List, PenLine,
  CheckCircle, BookOpen, Download, XCircle, Eye,
  RefreshCw, AlertTriangle, Wifi, WifiOff,
} from 'lucide-react'
import { api } from '../api/client.js'
import { usePipeline } from '../hooks/usePipeline.js'
import VenueBadge from '../components/ui/VenueBadge.jsx'
import Spinner from '../components/ui/Spinner.jsx'

const STAGES = [
  { key: 'quality_gate',   label: 'Quality Gate',       Icon: Shield },
  { key: 'ingesting',      label: 'Ingest Documents',   Icon: UploadCloud },
  { key: 'knowledge_map',  label: 'Knowledge Map',      Icon: Map },
  { key: 'contribution',   label: 'Find Contribution',  Icon: Lightbulb },
  { key: 'outline',        label: 'Build Outline',      Icon: List },
  { key: 'drafting',       label: 'Draft Sections',     Icon: PenLine },
  { key: 'quality_passes', label: 'Quality Passes',     Icon: CheckCircle },
  { key: 'citations',      label: 'Resolve Citations',  Icon: BookOpen },
  { key: 'exporting',      label: 'Export Formats',     Icon: Download },
]

function StageRow({ stage, state, message, completedAt, isLast }) {
  const { Icon } = stage
  const done   = state === 'complete'
  const run    = state === 'running'
  const fail   = state === 'failed'
  const pend   = !state || state === 'pending'

  return (
    <div className="flex gap-3 py-2.5">
      {/* Icon */}
      <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 border transition-all
        ${run  ? 'bg-accent/15 border-accent/40 shadow-[0_0_12px_rgba(99,102,241,0.2)]' : ''}
        ${done ? 'bg-green/10  border-green/30' : ''}
        ${fail ? 'bg-red/10    border-red/30' : ''}
        ${pend ? 'bg-raised    border-border' : ''}
      `}>
        {run  ? <Spinner size={13} color="#6366f1" />
          : done ? <CheckCircle size={13} className="text-green-l" />
          : fail ? <XCircle size={13} className="text-red-l" />
          : <Icon size={13} className={pend ? 'text-faint' : 'text-muted'} />}
      </div>

      {/* Text */}
      <div className="flex-1 min-w-0">
        <p className={`text-[13px] font-semibold leading-tight transition-colors
          ${run  ? 'text-text' : done ? 'text-muted' : fail ? 'text-red-l' : 'text-faint'}`}>
          {stage.label}
        </p>
        {run && message && (
          <p className="text-[11px] text-muted mt-0.5 truncate">{message}</p>
        )}
        {done && completedAt && (
          <p className="text-[10px] text-faint mt-0.5">
            {new Date(completedAt).toLocaleTimeString('en-US', { hour12: false })}
          </p>
        )}
      </div>

      {/* Status dot */}
      <div className={`w-1.5 h-1.5 rounded-full self-center shrink-0
        ${run ? 'bg-accent animate-pulse-dot' : done ? 'bg-green' : fail ? 'bg-red' : 'bg-faint'}`} />
    </div>
  )
}

function Terminal({ logs }) {
  const endRef = useRef(null)
  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [logs])

  return (
    <div className="flex flex-col bg-bg rounded-2xl border border-border overflow-hidden h-full">
      {/* Traffic light bar */}
      <div className="flex items-center gap-2 px-4 py-3 bg-surface border-b border-border">
        <div className="flex gap-1.5">
          {['bg-red/70','bg-amber/70','bg-green/70'].map((c,i) => (
            <div key={i} className={`w-2.5 h-2.5 rounded-full ${c}`} />
          ))}
        </div>
        <span className="text-[11px] text-muted ml-2 font-mono">pipeline.log</span>
        <span className="text-[11px] text-faint ml-auto font-mono">{logs.length} lines</span>
      </div>

      {/* Log content */}
      <div className="flex-1 overflow-y-auto p-4 font-mono text-[11px] leading-[1.8] space-y-0.5">
        {logs.length === 0
          ? <span className="text-faint">Waiting for pipeline to start…</span>
          : logs.map((log, i) => (
            <div key={i} className="flex gap-3">
              <span className="text-faint shrink-0 select-none">
                {log.timestamp
                  ? new Date(log.timestamp).toLocaleTimeString('en-US', { hour12: false })
                  : String(i).padStart(4, '0')}
              </span>
              <span className={
                log.level === 'error'   ? 'text-red-l' :
                log.level === 'warn'    ? 'text-amber-l' :
                log.level === 'success' ? 'text-green-l' : 'text-muted'
              }>{log.message || log}</span>
            </div>
          ))
        }
        <div ref={endRef} />
      </div>
    </div>
  )
}

export default function Pipeline() {
  const { paperId } = useParams()
  const navigate = useNavigate()
  const { status, connected, logs } = usePipeline(paperId)
  const [paper, setPaper] = useState(null)
  const [cancelling, setCancelling] = useState(false)

  const overall = status?.status
  const stages = status?.stages || {}
  const msgs   = status?.stage_messages || {}
  const times  = status?.stage_completed_at || {}

  const completedCount = STAGES.filter(s => stages[s.key] === 'complete').length
  const pct = Math.round((completedCount / STAGES.length) * 100)
  const isRunning = overall === 'processing'

  useEffect(() => {
    api.get(`/api/papers/${paperId}`).then(r => setPaper(r.data)).catch(() => {})
  }, [paperId])

  async function cancel() {
    setCancelling(true)
    try { await api.post(`/api/pipeline/${paperId}/cancel`) }
    finally { setCancelling(false) }
  }

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      {/* Top bar */}
      <div className="flex items-center gap-4 px-6 py-3.5 border-b border-border bg-surface shrink-0">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            {paper && <VenueBadge venue={paper.target_venue || paper.venue} />}
            <div className="flex items-center gap-1.5">
              {connected
                ? <Wifi size={11} className="text-green-l" />
                : <WifiOff size={11} className="text-faint" />}
              <span className={`text-[10px] font-semibold ${connected ? 'text-green-l' : 'text-faint'}`}>
                {connected ? 'live' : 'polling'}
              </span>
            </div>
          </div>
          <h1 className="text-[15px] font-bold text-text truncate">
            {paper?.title || paper?.topic || 'Processing…'}
          </h1>
        </div>

        {/* Progress bar + pct */}
        {!['complete','failed','cancelled'].includes(overall) && (
          <div className="flex items-center gap-4 shrink-0">
            <div className="w-[180px]">
              <div className="h-1.5 bg-border rounded-full overflow-hidden">
                <div className="h-full bg-accent rounded-full transition-all duration-700"
                  style={{ width: `${pct}%`, boxShadow: '0 0 8px rgba(99,102,241,0.4)' }} />
              </div>
              <p className="text-[10px] text-muted text-right mt-1 font-mono">
                {pct}% · {completedCount}/{STAGES.length}
              </p>
            </div>
            {isRunning && (
              <button className="btn btn-ghost text-[12px] py-1.5 px-3" onClick={cancel} disabled={cancelling}>
                {cancelling ? <Spinner size={11} /> : <XCircle size={12} />}
                Cancel
              </button>
            )}
          </div>
        )}

        {/* CTA for terminal states */}
        {overall === 'complete' && (
          <div className="flex gap-2 shrink-0">
            <Link to={`/paper/${paperId}/preview`} className="btn bg-green/10 text-green-l border border-green/25 hover:bg-green/20 text-[13px] py-1.5">
              <Eye size={13} /> View Paper
            </Link>
            <Link to={`/paper/${paperId}/export`} className="btn btn-primary text-[13px] py-1.5">
              <Download size={13} /> Export
            </Link>
          </div>
        )}
        {overall === 'failed' && (
          <button className="btn btn-danger text-[13px] py-1.5" onClick={() => navigate(`/paper/${paperId}/upload`)}>
            <RefreshCw size={12} /> Retry
          </button>
        )}
        {overall === 'cancelled' && (
          <button className="btn btn-ghost text-[13px] py-1.5" onClick={() => navigate(`/paper/${paperId}/upload`)}>
            <RefreshCw size={12} /> Restart
          </button>
        )}
      </div>

      {/* Status banners */}
      {overall === 'complete' && (
        <div className="mx-5 mt-4 p-4 rounded-xl bg-green/8 border border-green/20 flex items-center gap-3 animate-slide-up shrink-0">
          <CheckCircle size={18} className="text-green-l shrink-0" />
          <div>
            <p className="text-sm font-bold text-text">Paper drafted successfully</p>
            <p className="text-[12px] text-muted mt-0.5">All 9 stages complete. Ready for review.</p>
          </div>
        </div>
      )}
      {overall === 'failed' && (
        <div className="mx-5 mt-4 p-4 rounded-xl bg-red/8 border border-red/20 flex items-center gap-3 animate-slide-up shrink-0">
          <XCircle size={18} className="text-red-l shrink-0" />
          <div>
            <p className="text-sm font-bold text-text">Pipeline failed</p>
            <p className="text-[12px] text-muted mt-0.5">{status?.error || 'Check the log for details.'}</p>
          </div>
        </div>
      )}
      {overall === 'cancelled' && (
        <div className="mx-5 mt-4 p-4 rounded-xl bg-amber/8 border border-amber/20 flex items-center gap-3 animate-slide-up shrink-0">
          <AlertTriangle size={18} className="text-amber-l shrink-0" />
          <div>
            <p className="text-sm font-bold text-text">Pipeline cancelled</p>
            <p className="text-[12px] text-muted mt-0.5">Stopped cleanly. Adjust inputs and restart.</p>
          </div>
        </div>
      )}

      {/* Main split */}
      <div className="flex-1 flex gap-4 p-5 overflow-hidden min-h-0">
        {/* Stage list */}
        <div className="w-[270px] shrink-0 card overflow-y-auto py-2 px-1">
          <p className="section-title px-3 pt-1">PIPELINE STAGES</p>
          <div className="divide-y divide-border px-2">
            {STAGES.map(s => (
              <StageRow key={s.key} stage={s}
                state={stages[s.key]} message={msgs[s.key]}
                completedAt={times[s.key]} />
            ))}
          </div>
          {status && (
            <div className="mx-2 mt-3 p-3 rounded-xl bg-raised border border-border">
              <div className="grid grid-cols-3 gap-2 text-center">
                {[
                  [STAGES.filter(s => stages[s.key] === 'complete').length, 'Done',    'text-green-l'],
                  [STAGES.filter(s => stages[s.key] === 'running').length,  'Running', 'text-accent'],
                  [STAGES.filter(s => !stages[s.key] || stages[s.key] === 'pending').length, 'Pending', 'text-faint'],
                ].map(([n, label, cls]) => (
                  <div key={label}>
                    <p className={`text-lg font-bold ${cls}`}>{n}</p>
                    <p className="text-[10px] text-muted">{label}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Terminal */}
        <div className="flex-1 min-w-0 flex flex-col gap-3">
          <Terminal logs={logs} />
          {status?.run?.id && (
            <div className="shrink-0 flex items-center gap-2 px-3">
              <span className="text-[10px] text-faint font-mono uppercase tracking-wider">Run</span>
              <span className="text-[11px] text-muted font-mono">{status.run.id.slice(0, 16)}…</span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
