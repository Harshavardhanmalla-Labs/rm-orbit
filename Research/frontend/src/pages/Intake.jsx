import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { CheckCircle, ChevronRight, ChevronLeft, FlaskConical } from 'lucide-react'
import { api } from '../api/client.js'
import Spinner from '../components/ui/Spinner.jsx'
import VenueBadge from '../components/ui/VenueBadge.jsx'

const PAPER_TYPES = [
  { value: 'original_research', label: 'Original Research', desc: 'Novel findings from experiments' },
  { value: 'survey',            label: 'Survey',             desc: 'Review of existing literature' },
  { value: 'case_study',        label: 'Case Study',         desc: 'In-depth analysis of an instance' },
  { value: 'technical_report',  label: 'Technical Report',   desc: 'Description of technical work' },
  { value: 'position_paper',    label: 'Position Paper',     desc: 'Argues a viewpoint on an issue' },
]

const VENUES = [
  { value: 'arxiv', label: 'arXiv' }, { value: 'ieee', label: 'IEEE' },
  { value: 'acm', label: 'ACM' },     { value: 'nature', label: 'Nature' },
  { value: 'springer', label: 'Springer' }, { value: 'custom', label: 'Custom' },
]

const WORD_PRESETS = [
  { value: 4000, label: 'Short', sub: '~4k words' },
  { value: 8000, label: 'Full',  sub: '~8k words' },
  { value: 15000,label: 'Long',  sub: '~15k words' },
]

const STEPS = ['Details', 'Format', 'Review']

export default function Intake() {
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [data, setData] = useState({
    topic: '', niche: '', paper_type: '', venue: '',
    author_name: '', affiliation: '', word_count: 8000,
  })
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)

  const set = (k, v) => setData(p => ({ ...p, [k]: v }))

  const canNext = step === 0
    ? data.topic.trim() && data.paper_type && data.venue
    : step === 1 ? data.author_name.trim() : true

  async function submit() {
    setSubmitting(true); setError(null)
    try {
      const res = await api.post('/api/intake/create', {
        topic: data.topic.trim(), niche: data.niche.trim(),
        paper_type: data.paper_type, target_venue: data.venue,
        author_name: data.author_name.trim(),
        author_affiliation: data.affiliation.trim(),
        word_count_target: data.word_count,
      })
      navigate(`/paper/${res.data.paper_id}/upload`)
    } catch (e) { setError(e?.response?.data?.detail || e.message) }
    finally { setSubmitting(false) }
  }

  return (
    <div className="max-w-[580px] mx-auto px-6 py-10">
      {/* Step indicator */}
      <div className="flex items-center gap-0 mb-8">
        {STEPS.map((label, i) => {
          const done = i < step, cur = i === step
          return (
            <div key={i} className="flex items-center" style={{ flex: i < STEPS.length - 1 ? '1 1 0' : 'none' }}>
              <div className="flex items-center gap-2 shrink-0">
                <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all
                  ${done ? 'bg-green text-white' : cur ? 'bg-accent text-white' : 'bg-raised text-muted border border-border'}`}>
                  {done ? <CheckCircle size={13} /> : i + 1}
                </div>
                <span className={`text-[12px] font-semibold hidden sm:block ${cur ? 'text-text' : 'text-muted'}`}>{label}</span>
              </div>
              {i < STEPS.length - 1 && (
                <div className={`flex-1 h-px mx-3 ${done ? 'bg-green' : 'bg-border'}`} />
              )}
            </div>
          )
        })}
      </div>

      {/* Card */}
      <div className="card p-7">
        {step === 0 && (
          <div className="space-y-6 animate-slide-up">
            <div>
              <h2 className="text-lg font-bold text-text mb-1">Paper Details</h2>
              <p className="text-[13px] text-muted">Tell the AI what to write.</p>
            </div>

            <div className="space-y-1.5">
              <label className="label">Research Topic <span className="text-red normal-case tracking-normal">*</span></label>
              <input className="input" placeholder="e.g. Transformer architectures for time-series forecasting"
                value={data.topic} onChange={e => set('topic', e.target.value)} />
            </div>

            <div className="space-y-1.5">
              <label className="label">Sub-field / Domain</label>
              <input className="input" placeholder="e.g. Deep Learning, Biomedical NLP, Climate Modeling"
                value={data.niche} onChange={e => set('niche', e.target.value)} />
            </div>

            <div className="space-y-2">
              <label className="label">Paper Type <span className="text-red normal-case tracking-normal">*</span></label>
              <div className="grid grid-cols-2 gap-2">
                {PAPER_TYPES.map(t => (
                  <button key={t.value} type="button" onClick={() => set('paper_type', t.value)}
                    className={`p-3.5 rounded-xl text-left border transition-all ${
                      data.paper_type === t.value
                        ? 'bg-accent/10 border-accent/40'
                        : 'bg-raised border-border hover:border-border-bright'
                    }`}>
                    <p className={`text-[13px] font-semibold ${data.paper_type === t.value ? 'text-accent' : 'text-text'}`}>{t.label}</p>
                    <p className="text-[11px] text-muted mt-0.5 leading-snug">{t.desc}</p>
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <label className="label">Target Venue <span className="text-red normal-case tracking-normal">*</span></label>
              <div className="flex flex-wrap gap-2">
                {VENUES.map(v => (
                  <button key={v.value} type="button" onClick={() => set('venue', v.value)}
                    className={`px-4 py-1.5 rounded-xl text-[13px] font-semibold border transition-all ${
                      data.venue === v.value
                        ? 'bg-accent/10 border-accent/40 text-accent'
                        : 'bg-raised border-border text-muted hover:text-text hover:border-border-bright'
                    }`}>
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
              <h2 className="text-lg font-bold text-text mb-1">Author & Format</h2>
              <p className="text-[13px] text-muted">Your name and target length.</p>
            </div>

            <div className="space-y-1.5">
              <label className="label">Author Name <span className="text-red normal-case tracking-normal">*</span></label>
              <input className="input" placeholder="Full name as it should appear on the paper"
                value={data.author_name} onChange={e => set('author_name', e.target.value)} />
            </div>

            <div className="space-y-1.5">
              <label className="label">Affiliation</label>
              <input className="input" placeholder="e.g. MIT, Stanford, Independent Researcher"
                value={data.affiliation} onChange={e => set('affiliation', e.target.value)} />
            </div>

            <div className="space-y-3">
              <label className="label">Target Length</label>
              <div className="grid grid-cols-3 gap-2">
                {WORD_PRESETS.map(p => (
                  <button key={p.value} type="button" onClick={() => set('word_count', p.value)}
                    className={`p-3.5 rounded-xl text-center border transition-all ${
                      data.word_count === p.value
                        ? 'bg-accent/10 border-accent/40'
                        : 'bg-raised border-border hover:border-border-bright'
                    }`}>
                    <p className={`text-[13px] font-bold ${data.word_count === p.value ? 'text-accent' : 'text-text'}`}>{p.label}</p>
                    <p className="text-[11px] text-muted mt-0.5">{p.sub}</p>
                  </button>
                ))}
              </div>
              <div className="space-y-2">
                <input type="range" min={3000} max={20000} step={500} value={data.word_count}
                  onChange={e => set('word_count', parseInt(e.target.value))}
                  className="w-full accent-accent" />
                <div className="flex justify-between">
                  <span className="text-[11px] text-faint">3,000</span>
                  <span className="text-[12px] font-bold text-accent">{data.word_count.toLocaleString()} words</span>
                  <span className="text-[11px] text-faint">20,000</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-5 animate-slide-up">
            <div>
              <h2 className="text-lg font-bold text-text mb-1">Review & Create</h2>
              <p className="text-[13px] text-muted">Confirm before starting.</p>
            </div>

            <div className="rounded-xl border border-border overflow-hidden">
              {[
                ['Topic', data.topic],
                ['Domain', data.niche || '—'],
                ['Type', data.paper_type.replace(/_/g, ' ')],
                ['Venue', <VenueBadge key="v" venue={data.venue} />],
                ['Author', data.author_name],
                ['Affiliation', data.affiliation || '—'],
                ['Length', `${data.word_count.toLocaleString()} words`],
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
          </div>
        )}

        {error && (
          <div className="mt-5 p-3.5 rounded-xl bg-red/10 border border-red/25 text-[13px] text-red-l">{error}</div>
        )}

        {/* Navigation */}
        <div className="flex items-center justify-between mt-7 pt-5 border-t border-border">
          <button className="btn btn-ghost" onClick={() => setStep(s => s - 1)} disabled={step === 0}>
            <ChevronLeft size={14} /> Back
          </button>
          {step < 2 ? (
            <button className="btn btn-primary px-6" onClick={() => setStep(s => s + 1)} disabled={!canNext}>
              Continue <ChevronRight size={14} />
            </button>
          ) : (
            <button className="btn btn-primary px-6" onClick={submit} disabled={submitting}>
              {submitting ? <Spinner size={14} color="white" /> : <FlaskConical size={14} />}
              {submitting ? 'Creating…' : 'Create Paper'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
