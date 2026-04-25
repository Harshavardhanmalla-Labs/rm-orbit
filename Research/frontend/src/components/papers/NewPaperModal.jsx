import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChevronLeft, ChevronRight, CheckCircle, X, FlaskConical } from 'lucide-react'
import toast from 'react-hot-toast'
import { api } from '../../api/client'
import Spinner from '../ui/Spinner'
import VenueBadge from '../ui/VenueBadge'

const PAPER_TYPES = [
  { value: 'original_research', label: 'Original Research', desc: 'Novel findings from experiments' },
  { value: 'survey', label: 'Survey', desc: 'Review of existing literature' },
  { value: 'case_study', label: 'Case Study', desc: 'In-depth analysis of an instance' },
  { value: 'technical_report', label: 'Technical Report', desc: 'Description of technical work' },
  { value: 'position_paper', label: 'Position Paper', desc: 'Argues a viewpoint on an issue' },
]

const VENUES = [
  { value: 'arxiv', label: 'arXiv' },
  { value: 'ieee', label: 'IEEE' },
  { value: 'acm', label: 'ACM' },
  { value: 'nature', label: 'Nature' },
  { value: 'springer', label: 'Springer' },
  { value: 'custom', label: 'Custom' },
]

const WORD_PRESETS = [
  { value: 4000, label: 'Short', sub: '~4k words' },
  { value: 8000, label: 'Full', sub: '~8k words' },
  { value: 15000, label: 'Long', sub: '~15k words' },
]

const STEPS = ['Details', 'Format', 'Review']

export default function NewPaperModal({ open, onClose }) {
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [form, setForm] = useState({
    topic: '',
    niche: '',
    paper_type: '',
    venue: '',
    author_name: '',
    affiliation: '',
    word_count: 8000,
  })
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)

  const set = (k, v) => setForm(prev => ({ ...prev, [k]: v }))

  const canNext = [
    () => form.topic.trim() && form.paper_type && form.venue,
    () => form.author_name.trim(),
    () => true,
  ][step]?.() || false

  useEffect(() => {
    function handleEscape(e) {
      if (e.key === 'Escape' && open) handleClose()
    }
    window.addEventListener('keydown', handleEscape)
    return () => window.removeEventListener('keydown', handleEscape)
  }, [open])

  function handleClose() {
    setStep(0)
    setForm({
      topic: '',
      niche: '',
      paper_type: '',
      venue: '',
      author_name: '',
      affiliation: '',
      word_count: 8000,
    })
    setError(null)
    onClose()
  }

  async function handleSubmit() {
    setSubmitting(true)
    setError(null)
    try {
      const res = await api.post('/api/intake/create', {
        topic: form.topic.trim(),
        niche: form.niche.trim(),
        paper_type: form.paper_type,
        target_venue: form.venue,
        author_name: form.author_name.trim(),
        author_affiliation: form.affiliation.trim(),
        word_count_target: form.word_count,
      })
      toast.success('✓ Paper created!')
      handleClose()
      navigate(`/paper/${res.data.paper_id}/upload`)
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'Failed to create paper')
    } finally {
      setSubmitting(false)
    }
  }

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-bg/80 backdrop-blur-sm animate-fade-in"
        onClick={handleClose}
      />

      {/* Panel */}
      <div className="relative z-10 w-full max-w-[520px] bg-panel rounded-2xl border border-border shadow-2xl animate-scale-in max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-border shrink-0">
          <div>
            <h2 className="text-[15px] font-bold text-text">New Paper</h2>
            <p className="text-[11px] text-faint mt-0.5">Step {step + 1} of 3</p>
          </div>
          <button
            onClick={handleClose}
            className="p-1.5 rounded-lg hover:bg-raised text-muted hover:text-text transition-colors"
          >
            <X size={16} />
          </button>
        </div>

        {/* Step indicator */}
        <div className="flex items-center gap-0 px-6 py-4 border-b border-border shrink-0">
          {STEPS.map((label, i) => {
            const done = i < step
            const cur = i === step
            return (
              <div key={i} className="flex items-center" style={{ flex: i < STEPS.length - 1 ? '1 1 0' : 'none' }}>
                <div className="flex items-center gap-2 shrink-0">
                  <div
                    className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                      done
                        ? 'bg-emerald text-white'
                        : cur
                          ? 'bg-accent text-white'
                          : 'bg-raised text-muted border border-border'
                    }`}
                  >
                    {done ? <CheckCircle size={13} /> : i + 1}
                  </div>
                  <span className={`text-[11px] font-semibold hidden sm:block ${cur ? 'text-text' : 'text-muted'}`}>
                    {label}
                  </span>
                </div>
                {i < STEPS.length - 1 && (
                  <div className={`flex-1 h-px mx-3 ${done ? 'bg-emerald' : 'border-border'}`} />
                )}
              </div>
            )
          })}
        </div>

        {/* Step content */}
        <div className="px-6 py-6 min-h-[320px]">
          {step === 0 && (
            <div className="space-y-6 animate-slide-up">
              <div>
                <h3 className="text-lg font-bold text-text mb-1">Paper Details</h3>
                <p className="text-[13px] text-muted">Tell the AI what to write.</p>
              </div>

              <div className="space-y-1.5">
                <label className="label">Research Topic <span className="text-red normal-case tracking-normal">*</span></label>
                <input
                  className="input"
                  placeholder="e.g. Transformer architectures for time-series forecasting"
                  value={form.topic}
                  onChange={e => set('topic', e.target.value)}
                />
              </div>

              <div className="space-y-1.5">
                <label className="label">Sub-field / Domain</label>
                <input
                  className="input"
                  placeholder="e.g. Deep Learning, Biomedical NLP, Climate Modeling"
                  value={form.niche}
                  onChange={e => set('niche', e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <label className="label">Paper Type <span className="text-red normal-case tracking-normal">*</span></label>
                <div className="grid grid-cols-2 gap-2">
                  {PAPER_TYPES.map(t => (
                    <button
                      key={t.value}
                      type="button"
                      onClick={() => set('paper_type', t.value)}
                      className={`p-3.5 rounded-xl text-left border transition-all ${
                        form.paper_type === t.value
                          ? 'bg-accent/10 border-accent/40'
                          : 'bg-raised border-border hover:border-border-bright'
                      }`}
                    >
                      <p className={`text-[13px] font-semibold ${form.paper_type === t.value ? 'text-accent' : 'text-text'}`}>
                        {t.label}
                      </p>
                      <p className="text-[11px] text-muted mt-0.5 leading-snug">{t.desc}</p>
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <label className="label">Target Venue <span className="text-red normal-case tracking-normal">*</span></label>
                <div className="flex flex-wrap gap-2">
                  {VENUES.map(v => (
                    <button
                      key={v.value}
                      type="button"
                      onClick={() => set('venue', v.value)}
                      className={`px-4 py-1.5 rounded-xl text-[13px] font-semibold border transition-all ${
                        form.venue === v.value
                          ? 'bg-accent/10 border-accent/40 text-accent'
                          : 'bg-raised border-border text-muted hover:text-text hover:border-border-bright'
                      }`}
                    >
                      {v.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {step === 1 && (
            <div className="space-y-6 animate-slide-up">
              <div>
                <h3 className="text-lg font-bold text-text mb-1">Author & Format</h3>
                <p className="text-[13px] text-muted">Your name and target length.</p>
              </div>

              <div className="space-y-1.5">
                <label className="label">Author Name <span className="text-red normal-case tracking-normal">*</span></label>
                <input
                  className="input"
                  placeholder="Full name as it should appear on the paper"
                  value={form.author_name}
                  onChange={e => set('author_name', e.target.value)}
                />
              </div>

              <div className="space-y-1.5">
                <label className="label">Affiliation</label>
                <input
                  className="input"
                  placeholder="e.g. MIT, Stanford, Independent Researcher"
                  value={form.affiliation}
                  onChange={e => set('affiliation', e.target.value)}
                />
              </div>

              <div className="space-y-3">
                <label className="label">Target Length</label>
                <div className="grid grid-cols-3 gap-2">
                  {WORD_PRESETS.map(p => (
                    <button
                      key={p.value}
                      type="button"
                      onClick={() => set('word_count', p.value)}
                      className={`p-3.5 rounded-xl text-center border transition-all ${
                        form.word_count === p.value
                          ? 'bg-accent/10 border-accent/40'
                          : 'bg-raised border-border hover:border-border-bright'
                      }`}
                    >
                      <p className={`text-[13px] font-bold ${form.word_count === p.value ? 'text-accent' : 'text-text'}`}>
                        {p.label}
                      </p>
                      <p className="text-[11px] text-muted mt-0.5">{p.sub}</p>
                    </button>
                  ))}
                </div>
                <div className="space-y-2">
                  <input
                    type="range"
                    min={3000}
                    max={20000}
                    step={500}
                    value={form.word_count}
                    onChange={e => set('word_count', parseInt(e.target.value))}
                    className="w-full accent-accent"
                  />
                  <div className="flex justify-between">
                    <span className="text-[11px] text-faint">3,000</span>
                    <span className="text-[12px] font-bold text-accent">{form.word_count.toLocaleString()} words</span>
                    <span className="text-[11px] text-faint">20,000</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-5 animate-slide-up">
              <div>
                <h3 className="text-lg font-bold text-text mb-1">Review & Create</h3>
                <p className="text-[13px] text-muted">Confirm before starting.</p>
              </div>

              <div className="rounded-xl border border-border overflow-hidden">
                {[
                  ['Topic', form.topic],
                  ['Domain', form.niche || '—'],
                  ['Type', form.paper_type.replace(/_/g, ' ')],
                  ['Venue', <VenueBadge key="v" venue={form.venue} />],
                  ['Author', form.author_name],
                  ['Affiliation', form.affiliation || '—'],
                  ['Length', `${form.word_count.toLocaleString()} words`],
                ].map(([k, v]) => (
                  <div key={k} className="flex gap-4 px-4 py-3 border-b border-border last:border-0 bg-raised/50">
                    <span className="text-[12px] text-muted min-w-[100px] shrink-0">{k}</span>
                    <span className="text-[13px] font-semibold text-text capitalize">{v}</span>
                  </div>
                ))}
              </div>

              <div className="flex gap-3 p-4 rounded-xl bg-accent/8 border border-accent/20">
                <FlaskConical size={15} className="text-accent shrink-0 mt-0.5" />
                <p className="text-[12px] text-muted leading-relaxed">
                  After creation you'll upload source documents, then watch the 9-stage AI pipeline draft your paper.
                </p>
              </div>

              {error && (
                <div className="p-3.5 rounded-xl bg-red/10 border border-red/25 text-[13px] text-red-l">{error}</div>
              )}
            </div>
          )}
        </div>

        {/* Footer navigation */}
        <div className="flex items-center justify-between px-6 py-4 border-t border-border shrink-0">
          <button
            onClick={() => setStep(s => s - 1)}
            disabled={step === 0}
            className="btn btn-ghost text-[13px]"
          >
            <ChevronLeft size={14} /> Back
          </button>
          {step < 2 ? (
            <button onClick={() => setStep(s => s + 1)} disabled={!canNext} className="btn btn-primary text-[13px] px-6">
              Continue <ChevronRight size={14} />
            </button>
          ) : (
            <button onClick={handleSubmit} disabled={submitting} className="btn btn-primary text-[13px] px-6">
              {submitting ? <Spinner size={14} color="white" /> : <FlaskConical size={14} />}
              {submitting ? 'Creating…' : 'Create Paper'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
