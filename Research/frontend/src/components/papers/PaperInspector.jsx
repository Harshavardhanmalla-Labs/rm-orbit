import { useState, useEffect } from 'react'
import { X, Copy, CheckCircle, Play, Square, Download } from 'lucide-react'
import toast from 'react-hot-toast'
import { api } from '../../api/client'
import VenueBadge from '../ui/VenueBadge'
import StatusBadge from '../ui/StatusBadge'
import Spinner from '../ui/Spinner'

function LivePipelineSection({ paperId, status }) {
  const [stages, setStages] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchStatus() {
      try {
        const res = await api.get(`/api/pipeline/${paperId}/status`)
        setStages(res.data.stages || [])
      } catch (e) {
        console.error('Failed to fetch pipeline status:', e)
      } finally {
        setLoading(false)
      }
    }

    if (status !== 'intake') {
      fetchStatus()
      const interval = setInterval(fetchStatus, 2000)
      return () => clearInterval(interval)
    }
  }, [paperId, status])

  if (status === 'intake' || loading) {
    return (
      <div className="space-y-2">
        <div className="h-3 bg-raised rounded-full animate-pulse-dot" />
        <div className="h-3 bg-raised rounded-full animate-pulse-dot" style={{ animationDelay: '0.1s' }} />
      </div>
    )
  }

  return (
    <div className="space-y-2">
      {stages.map((stage, i) => {
        const done = stage.status === 'complete'
        const active = stage.status === 'running'
        return (
          <div key={i} className="flex items-center gap-2 text-[11px]">
            <div className={`w-1.5 h-1.5 rounded-full ${done ? 'bg-emerald' : active ? 'bg-accent animate-pulse' : 'bg-border'}`} />
            <span className={done ? 'text-emerald-l' : active ? 'text-accent' : 'text-muted'}>
              {stage.name}
            </span>
          </div>
        )
      })}
    </div>
  )
}

export default function PaperInspector({ paperId, onClose, onAction }) {
  const [paper, setPaper] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [copied, setCopied] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    async function fetchPaper() {
      setLoading(true)
      try {
        const res = await api.get(`/api/papers/${paperId}`)
        setPaper(res.data)
        setError(null)
      } catch (e) {
        setError(e.response?.data?.detail || e.message || 'Failed to load paper')
      } finally {
        setLoading(false)
      }
    }

    if (paperId) {
      fetchPaper()
    }
  }, [paperId])

  function copyError() {
    if (error) {
      navigator.clipboard.writeText(error)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  async function handleAction(action) {
    setSubmitting(true)
    try {
      if (action === 'start') {
        await api.post(`/api/pipeline/${paperId}/start`)
        toast.success('✓ Pipeline restarted')
      } else if (action === 'cancel') {
        await api.post(`/api/pipeline/${paperId}/cancel`)
        toast.success('✓ Pipeline cancelled')
      }
      onAction?.(action)
    } catch (e) {
      const errorMsg = e.response?.data?.detail || e.message || 'Action failed'
      setError(errorMsg)
      toast.error(errorMsg)
    } finally {
      setSubmitting(false)
    }
  }

  if (!paperId) return null

  const isRunning = paper && ['processing', 'running'].includes(paper.status)
  const isFailed = paper && paper.status === 'failed'
  const isComplete = paper && paper.status === 'complete'
  const isIntake = paper && paper.status === 'intake'

  return (
    <div className="w-80 bg-panel border-l border-border flex flex-col h-full animate-slide-in-right">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-border shrink-0">
        <div className="flex-1 min-w-0">
          {loading ? (
            <div className="h-4 bg-raised rounded w-3/4 animate-pulse-dot" />
          ) : (
            <h3 className="text-[13px] font-bold text-text line-clamp-1">{paper?.title || paper?.topic || 'Paper'}</h3>
          )}
        </div>
        <button
          onClick={onClose}
          className="p-1.5 rounded-lg hover:bg-raised text-muted hover:text-text transition-colors shrink-0 ml-2"
        >
          <X size={14} />
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-5 space-y-5">
          {/* Badges */}
          {!loading && paper && (
            <div className="flex gap-2">
              <VenueBadge venue={paper.target_venue} />
              <StatusBadge status={paper.status} />
            </div>
          )}

          {/* Metadata */}
          {loading ? (
            <div className="space-y-3">
              {Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="space-y-1">
                  <div className="h-3 bg-raised rounded w-1/3 animate-pulse-dot" />
                  <div className="h-3 bg-raised rounded w-full animate-pulse-dot" style={{ animationDelay: '0.1s' }} />
                </div>
              ))}
            </div>
          ) : paper ? (
            <div className="space-y-3 text-[12px]">
              {paper.topic && (
                <div>
                  <p className="text-muted mb-1">Topic</p>
                  <p className="text-text">{paper.topic}</p>
                </div>
              )}
              {paper.niche && (
                <div>
                  <p className="text-muted mb-1">Domain</p>
                  <p className="text-text">{paper.niche}</p>
                </div>
              )}
              {paper.paper_type && (
                <div>
                  <p className="text-muted mb-1">Type</p>
                  <p className="text-text capitalize">{paper.paper_type.replace(/_/g, ' ')}</p>
                </div>
              )}
              {paper.author_name && (
                <div>
                  <p className="text-muted mb-1">Author</p>
                  <p className="text-text">{paper.author_name}</p>
                </div>
              )}
              {paper.author_affiliation && (
                <div>
                  <p className="text-muted mb-1">Affiliation</p>
                  <p className="text-text">{paper.author_affiliation}</p>
                </div>
              )}
              {paper.word_count_target && (
                <div>
                  <p className="text-muted mb-1">Target Length</p>
                  <p className="text-text">{paper.word_count_target.toLocaleString()} words</p>
                </div>
              )}
              {paper.created_at && (
                <div>
                  <p className="text-muted mb-1">Created</p>
                  <p className="text-text">
                    {new Date(paper.created_at).toLocaleDateString('en-US', {
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric',
                    })}
                  </p>
                </div>
              )}
            </div>
          ) : null}

          {/* Pipeline status if running */}
          {!loading && paper && (
            <>
              <div className="border-t border-border pt-4">
                <p className="text-[11px] font-semibold text-muted uppercase tracking-wider mb-2">Pipeline</p>
                <LivePipelineSection paperId={paperId} status={paper.status} />
              </div>
            </>
          )}

          {/* Error block */}
          {error && (
            <div className="p-3 rounded-lg bg-red/10 border border-red/25 space-y-2">
              <p className="text-[11px] text-red-l">{error}</p>
              <button
                onClick={copyError}
                className="flex items-center gap-1 text-[10px] text-red-l hover:text-red-l/80 transition-colors"
              >
                {copied ? <CheckCircle size={12} /> : <Copy size={12} />}
                {copied ? 'Copied' : 'Copy error'}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Footer: action buttons */}
      {!loading && paper && (
        <div className="px-5 py-4 border-t border-border shrink-0 space-y-2">
          {isIntake && (
            <button
              onClick={() => window.location.href = `/paper/${paperId}/upload`}
              className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-accent/10 text-accent hover:bg-accent/15 text-[12px] font-medium transition-colors"
            >
              <Play size={12} /> Upload Documents
            </button>
          )}

          {isRunning && (
            <>
              <button
                onClick={() => window.location.href = `/paper/${paperId}/pipeline`}
                className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-accent/10 text-accent hover:bg-accent/15 text-[12px] font-medium transition-colors"
              >
                <Play size={12} /> View Pipeline
              </button>
              <button
                onClick={() => handleAction('cancel')}
                disabled={submitting}
                className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-red/10 text-red-l hover:bg-red/15 text-[12px] font-medium transition-colors disabled:opacity-50"
              >
                {submitting ? <Spinner size={12} color="#ef4444" /> : <Square size={12} />}
                {submitting ? 'Cancelling...' : 'Cancel'}
              </button>
            </>
          )}

          {isComplete && (
            <>
              <button
                onClick={() => window.location.href = `/paper/${paperId}/preview`}
                className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-emerald/10 text-emerald-l hover:bg-emerald/15 text-[12px] font-medium transition-colors"
              >
                Preview
              </button>
              <button
                onClick={() => window.location.href = `/paper/${paperId}/export`}
                className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-accent/10 text-accent hover:bg-accent/15 text-[12px] font-medium transition-colors"
              >
                <Download size={12} /> Export
              </button>
            </>
          )}

          {isFailed && (
            <>
              <button
                onClick={() => window.location.href = `/paper/${paperId}/pipeline`}
                className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-red/10 text-red-l hover:bg-red/15 text-[12px] font-medium transition-colors"
              >
                View Error
              </button>
              <button
                onClick={() => handleAction('start')}
                disabled={submitting}
                className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-accent/10 text-accent hover:bg-accent/15 text-[12px] font-medium transition-colors disabled:opacity-50"
              >
                {submitting ? <Spinner size={12} color="#6366f1" /> : <Play size={12} />}
                {submitting ? 'Starting...' : 'Retry'}
              </button>
            </>
          )}
        </div>
      )}
    </div>
  )
}
