import { useState } from 'react'
import { Trash2, ChevronRight } from 'lucide-react'
import VenueBadge from '../ui/VenueBadge'
import StatusBadge from '../ui/StatusBadge'
import ProgressBar from '../ui/ProgressBar'
import { useNavigate } from 'react-router-dom'
import { api } from '../../api/client'

export default function PaperCard({ paper, onSelect, selected = false }) {
  const navigate = useNavigate()
  const [hovered, setHovered] = useState(false)
  const [confirmDelete, setConfirmDelete] = useState(false)
  const [deleting, setDeleting] = useState(false)

  const isRunning = ['processing', 'running'].includes(paper.status)
  const isFailed = paper.status === 'failed'
  const isComplete = paper.status === 'complete'
  const isIntake = paper.status === 'intake'

  const createdDate = paper.created_at
    ? new Date(paper.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    : '—'

  async function handleDelete() {
    setDeleting(true)
    try {
      await api.delete(`/api/papers/${paper.id}`)
      // Parent component handles removal from list
      onSelect?.(null)
    } catch (e) {
      console.error('Delete failed:', e)
    } finally {
      setDeleting(false)
      setConfirmDelete(false)
    }
  }

  function handleActionClick(e) {
    e.stopPropagation()
    if (isIntake) navigate(`/paper/${paper.id}/upload`)
    else if (isRunning) navigate(`/paper/${paper.id}/pipeline`)
    else if (isComplete) navigate(`/paper/${paper.id}/preview`)
    else if (isFailed) navigate(`/paper/${paper.id}/pipeline`)
  }

  return (
    <div
      onClick={() => onSelect?.(paper)}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className={`relative bg-surface rounded-xl border p-5 transition-all duration-150 cursor-pointer ${
        selected
          ? 'border-accent/40 bg-accent/5'
          : hovered
            ? 'border-border-bright'
            : 'border-border'
      }`}
    >
      {/* Running indicator */}
      {isRunning && (
        <div className="absolute top-3 right-3 flex items-center gap-1.5 bg-accent/10 px-2.5 py-1.5 rounded-lg border border-accent/25">
          <span className="w-2 h-2 bg-accent rounded-full animate-pulse-dot"></span>
          <span className="text-[11px] text-accent font-semibold">Running</span>
        </div>
      )}
      {/* Top row: badges + delete */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex gap-2">
          <VenueBadge venue={paper.target_venue} />
          <StatusBadge status={paper.status} />
        </div>
        {hovered && (
          <div>
            {!confirmDelete ? (
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  setConfirmDelete(true)
                }}
                className="p-1.5 rounded-lg hover:bg-red/10 text-muted hover:text-red-l transition-colors"
              >
                <Trash2 size={13} />
              </button>
            ) : (
              <div className="flex gap-1">
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    handleDelete()
                  }}
                  disabled={deleting}
                  className="px-2 py-1 text-[10px] font-bold rounded bg-red/20 text-red-l hover:bg-red/30 disabled:opacity-50"
                >
                  {deleting ? 'Deleting...' : 'Confirm'}
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    setConfirmDelete(false)
                  }}
                  className="p-1 rounded hover:bg-raised text-muted hover:text-text"
                >
                  ✕
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Title */}
      <h3 className="text-[14px] font-bold text-text line-clamp-2 leading-snug">
        {paper.title || paper.topic || 'Untitled Paper'}
      </h3>

      {/* Domain */}
      {paper.niche && (
        <p className="text-[12px] text-muted line-clamp-1 mt-1">{paper.niche}</p>
      )}

      {/* Progress bar if running */}
      {isRunning && (
        <div className="mt-3">
          <ProgressBar
            value={paper.stage_progress || 0}
            color="accent"
            label={paper.current_stage}
            showPct
          />
        </div>
      )}

      {/* Error highlight if failed */}
      {isFailed && (
        <div className="mt-3 px-3 py-2 rounded-lg bg-red/10 border border-red/25 text-[11px] text-red-l font-medium">
          Pipeline failed — view error
        </div>
      )}

      {/* Footer: date + action button */}
      <div className="flex items-center justify-between pt-3 border-t border-border mt-3">
        <span className="text-[11px] text-muted flex items-center gap-1">
          <span>📅</span>
          {createdDate}
        </span>
        <button
          onClick={handleActionClick}
          className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-[12px] font-medium transition-colors ${
            isIntake
              ? 'bg-accent/10 text-accent hover:bg-accent/15'
              : isRunning
                ? 'bg-accent/10 text-accent hover:bg-accent/15'
                : isComplete
                  ? 'bg-emerald/10 text-emerald-l hover:bg-emerald/15'
                  : isFailed
                    ? 'bg-red/10 text-red-l hover:bg-red/15'
                    : 'bg-accent/10 text-accent hover:bg-accent/15'
          }`}
        >
          {isIntake && 'Start'}
          {isRunning && 'View'}
          {isComplete && 'Open'}
          {isFailed && 'View'}
          {!isIntake && !isRunning && !isComplete && !isFailed && 'Open'}
          <ChevronRight size={12} />
        </button>
      </div>
    </div>
  )
}
