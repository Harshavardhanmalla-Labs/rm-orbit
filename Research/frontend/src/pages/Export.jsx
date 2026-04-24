import { useState, useEffect, useCallback } from 'react'
import { useParams } from 'react-router-dom'
import {
  Download,
  FileCode,
  FileText,
  File,
  RefreshCw,
  CheckCircle,
  Info,
  RotateCcw,
} from 'lucide-react'
import { api } from '../api/client.js'
import VenueBadge from '../components/VenueBadge.jsx'
import Spinner from '../components/Spinner.jsx'
import ErrorCard from '../components/ErrorCard.jsx'

const VENUES = [
  { label: 'IEEE', value: 'ieee' },
  { label: 'ACM', value: 'acm' },
  { label: 'arXiv', value: 'arxiv' },
  { label: 'Nature', value: 'nature' },
  { label: 'Springer', value: 'springer' },
  { label: 'Custom', value: 'custom' },
]

const FORMAT_CONFIGS = [
  {
    format: 'latex',
    label: 'LaTeX',
    ext: '.tex',
    icon: FileCode,
    description: 'For journal submission via LaTeX workflow',
    detail: 'Includes .bib file and all formatting commands',
    iconColor: '#f59e0b',
    iconBg: 'rgba(245, 158, 11, 0.12)',
  },
  {
    format: 'pdf',
    label: 'PDF',
    ext: '.pdf',
    icon: FileText,
    description: 'Print-ready formatted document',
    detail: 'Fully typeset with bibliography and figures',
    iconColor: '#ef4444',
    iconBg: 'rgba(239, 68, 68, 0.12)',
  },
  {
    format: 'docx',
    label: 'DOCX',
    ext: '.docx',
    icon: File,
    description: 'Microsoft Word compatible',
    detail: 'Editable document with styles and references',
    iconColor: '#3b82f6',
    iconBg: 'rgba(59, 130, 246, 0.12)',
  },
]

function FormatCard({ config, paperId, disabled }) {
  const [downloading, setDownloading] = useState(false)
  const [downloaded, setDownloaded] = useState(false)
  const [error, setError] = useState(null)
  const Icon = config.icon

  async function handleDownload() {
    try {
      setDownloading(true)
      setError(null)
      const res = await api.get(`/api/export/${paperId}/${config.format}`, {
        responseType: 'blob',
      })
      const url = URL.createObjectURL(res.data)
      const a = document.createElement('a')
      a.href = url
      a.download = `paper${config.ext}`
      a.click()
      URL.revokeObjectURL(url)
      setDownloaded(true)
      setTimeout(() => setDownloaded(false), 3000)
    } catch (err) {
      setError('Download failed. The file may not be ready yet.')
    } finally {
      setDownloading(false)
    }
  }

  return (
    <div className="card p-6 flex flex-col gap-4 card-hover">
      {/* Icon */}
      <div
        className="w-12 h-12 rounded-xl flex items-center justify-center"
        style={{ backgroundColor: config.iconBg }}
      >
        <Icon size={22} style={{ color: config.iconColor }} />
      </div>

      {/* Info */}
      <div className="flex-1">
        <div className="flex items-center gap-2 mb-1">
          <h3 className="text-base font-semibold text-text">
            {config.label}
          </h3>
          <span className="text-xs px-1.5 py-0.5 rounded font-mono bg-surface text-faint">
            {config.ext}
          </span>
        </div>
        <p className="text-sm text-muted">{config.description}</p>
        <p className="text-xs mt-1 text-faint">{config.detail}</p>
      </div>

      {/* Error */}
      {error && (
        <p className="text-xs text-red-l">{error}</p>
      )}

      {/* Download button */}
      <button
        type="button"
        onClick={handleDownload}
        disabled={disabled || downloading}
        className={`w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-medium transition-all ${
          downloaded
            ? 'bg-green/10 text-green-l border border-green/25'
            : 'bg-accent/10 text-accent border border-accent/25 hover:bg-accent/15'
        } disabled:opacity-40 disabled:cursor-not-allowed`}
      >
        {downloading ? (
          <Spinner size={15} color="currentColor" />
        ) : downloaded ? (
          <CheckCircle size={15} />
        ) : (
          <Download size={15} />
        )}
        {downloading ? 'Downloading...' : downloaded ? 'Downloaded' : `Download ${config.label}`}
      </button>
    </div>
  )
}

export default function Export() {
  const { paperId } = useParams()
  const [paper, setPaper] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedVenue, setSelectedVenue] = useState('')
  const [reformatting, setReformatting] = useState(false)
  const [reformatError, setReformatError] = useState(null)
  const [reformatSuccess, setReformatSuccess] = useState(false)

  const loadPaper = useCallback(async function loadPaper() {
    try {
      setLoading(true)
      setError(null)
      const res = await api.get(`/api/papers/${paperId}`)
      setPaper(res.data)
      setSelectedVenue((res.data.target_venue || res.data.venue || 'arxiv').toLowerCase())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [paperId])

  useEffect(() => {
    loadPaper()
  }, [loadPaper])

  async function handleReformat() {
    try {
      setReformatting(true)
      setReformatError(null)
      setReformatSuccess(false)
      await api.post(`/api/export/${paperId}/reformat`, { venue: selectedVenue })
      setReformatSuccess(true)
      // Reload paper to get updated format info
      const res = await api.get(`/api/papers/${paperId}`)
      setPaper(res.data)
    } catch (err) {
      setReformatError(err.message)
    } finally {
      setReformatting(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="flex flex-col items-center gap-4">
          <Spinner size={32} />
          <p className="text-sm text-faint">Loading export options...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-xl mx-auto px-6 py-16">
        <ErrorCard message={error} onRetry={loadPaper} />
      </div>
    )
  }

  const isComplete = paper?.status === 'complete'

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-text">
          Export Paper
        </h1>
        <p className="text-sm mt-1 text-muted">
          Download your research paper in multiple formats.
        </p>
      </div>

      {!isComplete && (
        <div className="mb-8 p-4 rounded-xl border border-amber/25 bg-amber/5 flex items-start gap-3">
          <Info size={15} className="text-amber shrink-0 mt-0.5" />
          <p className="text-sm text-muted">
            The paper pipeline has not completed yet. Export files will be available once processing is finished.
          </p>
        </div>
      )}

      {/* Paper metadata */}
      {paper && (
        <div className="card mb-8 p-5">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div>
              <p className="text-xs text-faint">Title</p>
              <p className="text-sm font-medium mt-1 truncate text-text">
                {paper.title || paper.topic || '—'}
              </p>
            </div>
            <div>
              <p className="text-xs text-faint">Venue</p>
              <div className="mt-1">
                <VenueBadge venue={paper.target_venue} />
              </div>
            </div>
            <div>
              <p className="text-xs text-faint">Word Count</p>
              <p className="text-sm font-medium mt-1 text-text">
                {paper.confidence_report?.total_word_count
                  ? `~${paper.confidence_report.total_word_count.toLocaleString()}`
                  : '—'}
              </p>
            </div>
            <div>
              <p className="text-xs text-faint">References</p>
              <p className="text-sm font-medium mt-1 text-text">
                {paper.citations?.length ?? '—'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Format cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10">
        {FORMAT_CONFIGS.map((config) => (
          <FormatCard
            key={config.format}
            config={config}
            paperId={paperId}
            disabled={!isComplete}
          />
        ))}
      </div>

      {/* Reformat section */}
      <div className="card p-6">
        <div className="flex items-center gap-2 mb-2">
          <RotateCcw size={15} className="text-accent" />
          <h2 className="text-sm font-semibold text-text">
            Reformat for Different Venue
          </h2>
        </div>
        <p className="text-sm mb-5 text-faint">
          Regenerate the paper&apos;s formatting and citation style to match a different target venue.
        </p>

        <div className="flex flex-wrap items-center gap-3">
          <div className="flex flex-wrap gap-2 flex-1">
            {VENUES.map((venue) => (
              <button
                key={venue.value}
                type="button"
                onClick={() => setSelectedVenue(venue.value)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition-all ${
                  selectedVenue === venue.value
                    ? 'bg-accent/10 border-accent/40 text-accent'
                    : 'bg-surface border-border text-muted hover:text-text hover:border-border-bright'
                }`}
              >
                {venue.label}
              </button>
            ))}
          </div>

          <button
            type="button"
            onClick={handleReformat}
            disabled={reformatting || !isComplete || !selectedVenue}
            className="btn btn-primary text-sm py-2.5 px-5 flex items-center gap-2"
          >
            {reformatting ? <Spinner size={15} color="white" /> : <RefreshCw size={15} />}
            {reformatting ? 'Reformatting...' : 'Reformat'}
          </button>
        </div>

        {reformatSuccess && (
          <div className="mt-4 flex items-center gap-2 text-sm text-green-l">
            <CheckCircle size={14} />
            Successfully reformatted for {VENUES.find(v => v.value === selectedVenue)?.label || selectedVenue}. Re-download to get updated files.
          </div>
        )}

        {reformatError && (
          <p className="mt-4 text-sm text-red-l">
            {reformatError}
          </p>
        )}
      </div>
    </div>
  )
}
