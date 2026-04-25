import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useDropzone } from 'react-dropzone'
import { UploadCloud, X, FileText, FileCode, Database, Image, File, Play, CheckCircle2, AlertTriangle } from 'lucide-react'
import { api } from '../api/client.js'
import VenueBadge from '../components/ui/VenueBadge.jsx'
import Spinner from '../components/ui/Spinner.jsx'

const ICONS = {
  'application/pdf': FileText,
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': FileText,
  'text/plain': FileText, 'text/markdown': FileCode,
  'text/csv': Database, 'application/json': FileCode,
  'image/png': Image, 'image/jpeg': Image,
}
const fmt = b => b < 1024 ? `${b}B` : b < 1048576 ? `${(b/1024).toFixed(1)}KB` : `${(b/1048576).toFixed(1)}MB`

function Zone({ onDrop, accept }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: useCallback(a => onDrop(a), [onDrop]), accept, multiple: true,
  })
  return (
    <div {...getRootProps()} className={`p-10 rounded-2xl border-2 border-dashed text-center cursor-pointer transition-all
      ${isDragActive ? 'border-accent bg-accent/5' : 'border-border hover:border-border-bright hover:bg-raised/50'}`}>
      <input {...getInputProps()} />
      <div className="w-12 h-12 rounded-2xl bg-accent/10 border border-accent/20 flex items-center justify-center mx-auto mb-3">
        <UploadCloud size={22} className={isDragActive ? 'text-accent' : 'text-accent'} />
      </div>
      <p className="text-sm font-bold text-text mb-1">{isDragActive ? 'Drop files here' : 'Drop research files here'}</p>
      <p className="text-[12px] text-muted">PDF, DOCX, TXT, MD, CSV, JSON, PNG, JPG · max 50 MB each</p>
    </div>
  )
}

function FileRow({ file, onRemove }) {
  const Icon = ICONS[file.type] || File
  return (
    <div className="flex items-center gap-3 p-3 rounded-xl bg-raised border border-border group">
      <div className="w-8 h-8 rounded-lg bg-surface flex items-center justify-center shrink-0">
        <Icon size={14} className="text-accent" />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-[13px] font-semibold text-text truncate">{file.name}</p>
        <p className="text-[11px] text-muted">{fmt(file.size)}</p>
      </div>
      <button onClick={() => onRemove(file.name)}
        className="w-7 h-7 rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity text-muted hover:text-red-l hover:bg-red/10">
        <X size={13} />
      </button>
    </div>
  )
}

export default function Upload() {
  const { paperId } = useParams()
  const navigate = useNavigate()
  const [paper, setPaper] = useState(null)
  const [files, setFiles] = useState([])
  const [report, setReport] = useState(null)
  const [starting, setStarting] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    api.get(`/api/papers/${paperId}`).then(r => setPaper(r.data)).catch(() => {})
    api.get(`/api/intake/${paperId}/ingestion-report`).then(r => setReport(r.data)).catch(() => {})
  }, [paperId])

  function add(accepted) {
    setFiles(p => { const ex = new Set(p.map(f => f.name)); return [...p, ...accepted.filter(f => !ex.has(f.name))] })
  }

  async function start() {
    setStarting(true); setError(null)
    try {
      if (files.length > 0) {
        await Promise.all(files.map(f => {
          const fd = new FormData(); fd.append('file', f)
          return api.post(`/api/intake/${paperId}/upload`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
        }))
      }
      await api.post(`/api/pipeline/${paperId}/start`)
      navigate(`/paper/${paperId}/pipeline`)
    } catch (e) { setError(e.message) }
    finally { setStarting(false) }
  }

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Left panel */}
      <div className="w-[260px] shrink-0 border-r border-border bg-sidebar flex flex-col gap-5 p-5 overflow-y-auto">
        {paper ? (
          <>
            <div>
              <p className="section-title">Paper</p>
              <p className="text-[14px] font-bold text-text leading-snug mb-3">{paper.topic}</p>
              <div className="flex flex-wrap gap-1.5">
                <VenueBadge venue={paper.target_venue || paper.venue} />
                <span className="badge border border-border text-muted">{paper.paper_type?.replace(/_/g, ' ')}</span>
              </div>
            </div>
            {paper.author_name && (
              <div className="border-t border-border pt-4">
                <p className="section-title">Author</p>
                <p className="text-[13px] font-semibold text-text">{paper.author_name}</p>
                {paper.author_affiliation && <p className="text-[11px] text-muted mt-1">{paper.author_affiliation}</p>}
              </div>
            )}
          </>
        ) : (
          <div className="h-24 rounded-xl bg-raised animate-pulse-dot" />
        )}

        <div className="border-t border-border pt-4">
          <div className="flex items-center gap-2 mb-3">
            {report?.ready_for_pipeline
              ? <CheckCircle2 size={12} className="text-green-l" />
              : <AlertTriangle size={12} className="text-amber-l" />}
            <p className="section-title mb-0">Ingestion</p>
          </div>
          {report?.upload_count > 0 ? (
            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 rounded-xl bg-raised border border-border text-center">
                <p className="text-lg font-bold text-text">{report.upload_count}</p>
                <p className="text-[10px] text-muted">files</p>
              </div>
              <div className="p-3 rounded-xl bg-raised border border-border text-center">
                <p className="text-lg font-bold text-text">{((report.total_extracted_words || 0) / 1000).toFixed(1)}k</p>
                <p className="text-[10px] text-muted">words</p>
              </div>
            </div>
          ) : (
            <p className="text-[12px] text-muted">No files uploaded yet</p>
          )}
        </div>

        <div className="border-t border-border pt-4">
          <p className="section-title">What to upload</p>
          {[['PDFs / DOCX','Prior work, references, notes'],['CSV / JSON','Experiment data, results'],['Raw text','Ideas, outlines, logs']].map(([t, d]) => (
            <div key={t} className="mb-3">
              <p className="text-[12px] font-semibold text-text">{t}</p>
              <p className="text-[11px] text-muted">{d}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Right upload area */}
      <div className="flex-1 flex flex-col gap-5 p-8 overflow-y-auto">
        <div>
          <h1 className="text-lg font-bold text-text mb-1">Upload Documents</h1>
          <p className="text-[13px] text-muted">Provide source material — or skip and start immediately.</p>
        </div>

        <Zone onDrop={add} accept={{
          'application/pdf': ['.pdf'],
          'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
          'text/plain': ['.txt'], 'text/markdown': ['.md'],
          'text/csv': ['.csv'], 'application/json': ['.json'],
          'image/png': ['.png'], 'image/jpeg': ['.jpg', '.jpeg'],
        }} />

        {files.length > 0 && (
          <div>
            <p className="text-[12px] text-muted mb-2">{files.length} file{files.length !== 1 ? 's' : ''} ready</p>
            <div className="space-y-2">
              {files.map(f => <FileRow key={f.name} file={f} onRemove={n => setFiles(p => p.filter(x => x.name !== n))} />)}
            </div>
          </div>
        )}

        {error && <div className="p-3.5 rounded-xl bg-red/10 border border-red/25 text-[13px] text-red-l">{error}</div>}

        <div className="mt-auto space-y-2">
          <button className="btn btn-primary w-full py-3.5 text-[15px] font-bold rounded-2xl justify-center"
            onClick={start} disabled={starting}
            style={{ boxShadow: starting ? 'none' : '0 6px 24px rgba(99,102,241,0.25)' }}>
            {starting ? <><Spinner size={16} color="white" /> Starting Pipeline…</> : <><Play size={16} /> Start AI Pipeline</>}
          </button>
          {files.length === 0 && (
            <p className="text-[11px] text-faint text-center">You can start without files — AI will discover references automatically.</p>
          )}
        </div>
      </div>
    </div>
  )
}
