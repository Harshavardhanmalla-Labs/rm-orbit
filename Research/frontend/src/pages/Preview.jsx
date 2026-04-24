import { useState, useEffect, useRef, useCallback } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  Download,
  AlertTriangle,
  CheckCircle,
  ChevronRight,
  BookOpen,
  Tag,
  Hash,
} from 'lucide-react'
import { api } from '../api/client.js'
import VenueBadge from '../components/VenueBadge.jsx'
import Spinner from '../components/Spinner.jsx'
import ErrorCard from '../components/ErrorCard.jsx'

const SECTION_ORDER = ['introduction', 'literature_review', 'methodology', 'results', 'discussion', 'conclusion']
const SECTION_LABELS = {
  introduction: 'Introduction',
  literature_review: 'Related Work',
  methodology: 'Methodology',
  results: 'Results',
  discussion: 'Discussion',
  conclusion: 'Conclusion',
}

function ProgressBar({ value }) {
  const pct = Math.max(0, Math.min(100, value || 0))
  const barColor = pct >= 80 ? 'bg-green' : pct >= 60 ? 'bg-amber' : 'bg-red'
  const textColor = pct >= 80 ? 'text-green-l' : pct >= 60 ? 'text-amber-l' : 'text-red-l'
  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 h-1.5 rounded-full overflow-hidden bg-border">
        <div className={`h-full rounded-full transition-all duration-500 ${barColor}`} style={{ width: `${pct}%` }} />
      </div>
      <span className={`text-xs font-semibold w-10 text-right ${textColor}`}>{pct}%</span>
    </div>
  )
}

function QualityBadge({ level }) {
  const configs = {
    high:   { cls: 'bg-green/10 text-green-l border-green/25', label: 'High' },
    medium: { cls: 'bg-amber/10 text-amber-l border-amber/25', label: 'Medium' },
    low:    { cls: 'bg-red/10 text-red-l border-red/25', label: 'Low' },
    pass:   { cls: 'bg-green/10 text-green-l border-green/25', label: 'Pass' },
    fail:   { cls: 'bg-red/10 text-red-l border-red/25', label: 'Fail' },
  }
  const key = (level || '').toLowerCase()
  const c = configs[key] || configs.medium
  return (
    <span className={`inline-flex items-center text-xs font-medium px-2 py-0.5 rounded-full border ${c.cls}`}>
      {c.label}
    </span>
  )
}

function ConfidenceReport({ report }) {
  if (!report) return null
  const regLabel = report.academic_register_pass ? 'pass' : 'fail'
  const clarityLabel = (report.contribution_clarity || 'medium').toLowerCase()
  const verPct = report.total_citations > 0
    ? Math.round((report.verified_citations / report.total_citations) * 100)
    : 0

  const warningFlags = (report.flags || []).filter(f => f.severity === 'warning')
  const infoFlags = (report.flags || []).filter(f => f.severity === 'info')

  return (
    <div className="card sticky top-20">
      <div className="px-5 py-4 border-b border-border">
        <h3 className="text-sm font-semibold text-text">Confidence Report</h3>
        <p className="text-xs mt-0.5 text-faint">AI quality assessment</p>
      </div>

      <div className="p-5 space-y-5">
        {/* Word count */}
        {report.total_word_count > 0 && (
          <div className="flex items-center justify-between">
            <span className="text-xs text-muted">Word Count</span>
            <span className="text-xs font-semibold text-text">
              {report.total_word_count.toLocaleString()}
            </span>
          </div>
        )}

        {/* Citations verified */}
        {report.total_citations > 0 && (
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-muted">Citations Verified</span>
              <span className="text-xs font-semibold text-text">
                {report.verified_citations}/{report.total_citations}
              </span>
            </div>
            <ProgressBar value={verPct} />
          </div>
        )}

        {/* Source coverage */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-muted">Source Coverage</span>
          </div>
          <ProgressBar value={report.source_coverage_pct} />
        </div>

        {/* Claim sourcing */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-muted">Claim Sourcing</span>
          </div>
          <ProgressBar value={report.claim_sourcing_pct} />
        </div>

        {/* Section completeness */}
        {report.section_completeness && (
          <div className="flex items-center justify-between">
            <span className="text-xs text-muted">Sections Complete</span>
            <span className="text-xs font-semibold text-text">{report.section_completeness}</span>
          </div>
        )}

        {/* Badges */}
        <div className="flex items-center justify-between">
          <span className="text-xs text-muted">Academic Register</span>
          <QualityBadge level={regLabel} />
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xs text-muted">Contribution Clarity</span>
          <QualityBadge level={clarityLabel} />
        </div>

        {/* Warning flags */}
        {warningFlags.length > 0 && (
          <div>
            <p className="text-xs font-medium mb-2 text-text">Warnings</p>
            <div className="space-y-2">
              {warningFlags.map((flag, i) => (
                <div key={i} className="flex items-start gap-2 p-2.5 rounded-lg border border-amber/25 bg-amber/5 text-xs">
                  <AlertTriangle size={12} className="text-amber shrink-0 mt-0.5" />
                  <span className="text-muted">{flag.message}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Info flags (collapsed) */}
        {infoFlags.length > 0 && warningFlags.length === 0 && (
          <div>
            <p className="text-xs font-medium mb-2 text-faint">Notes</p>
            <div className="space-y-1.5">
              {infoFlags.slice(0, 3).map((flag, i) => (
                <div key={i} className="flex items-start gap-2 text-xs text-faint">
                  <CheckCircle size={11} className="mt-0.5 shrink-0" />
                  <span>{flag.message}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

function SectionContent({ heading, content, sectionRef }) {
  return (
    <div ref={sectionRef} className="mb-10">
      {heading && (
        <h2 className="text-xl font-semibold mb-4 pb-3 border-b border-border text-text">
          {heading}
        </h2>
      )}
      <div className="max-w-none text-muted">
        {(content || '').split('\n\n').map((para, i) => (
          <p key={i} className="mb-4" style={{ lineHeight: 1.8 }}>
            {para}
          </p>
        ))}
      </div>
    </div>
  )
}

export default function Preview() {
  const { paperId } = useParams()
  const [paper, setPaper] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeSection, setActiveSection] = useState(0)
  const sectionRefs = useRef([])

  const loadPaper = useCallback(async function loadPaper() {
    try {
      setLoading(true)
      setError(null)
      const res = await api.get(`/api/papers/${paperId}`)
      setPaper(res.data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [paperId])

  useEffect(() => { loadPaper() }, [loadPaper])

  function scrollToSection(i) {
    setActiveSection(i)
    sectionRefs.current[i]?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="flex flex-col items-center gap-4">
          <Spinner size={32} />
          <p className="text-sm text-faint">Loading paper...</p>
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

  if (!paper) return null

  const sectionsDict = paper.sections || {}
  const abstract = sectionsDict.abstract || ''
  const keywords = sectionsDict.keywords || []
  const citations = paper.citations || []
  const confidence = paper.confidence_report || null

  // Build ordered section list for rendering
  const bodySections = SECTION_ORDER
    .filter(key => sectionsDict[key] && sectionsDict[key].trim())
    .map(key => ({ key, heading: SECTION_LABELS[key], content: sectionsDict[key] }))

  // TOC entries: 0 = title+abstract, 1..N = body sections, N+1 = references
  const tocItems = [
    { label: 'Title & Abstract', idx: 0 },
    ...bodySections.map((s, i) => ({ label: s.heading, idx: i + 1 })),
    ...(citations.length > 0 ? [{ label: 'References', idx: bodySections.length + 1 }] : []),
  ]

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left: TOC */}
        <div className="lg:col-span-2">
          <div className="card sticky top-20 p-4">
            <p className="section-title mb-3">Contents</p>
            <nav className="space-y-0.5">
              {tocItems.map((item) => (
                <button key={item.idx} type="button" onClick={() => scrollToSection(item.idx)}
                  className={`w-full text-left flex items-center gap-2 px-2 py-1.5 rounded-lg text-xs transition-colors ${
                    activeSection === item.idx
                      ? 'bg-accent/10 text-accent'
                      : 'text-faint hover:text-muted'
                  }`}>
                  <Hash size={10} className="shrink-0" />
                  <span className="truncate">{item.label}</span>
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Center: Paper content */}
        <div className="lg:col-span-7">
          <div className="card p-8">
            {/* Title block */}
            <div ref={(el) => { sectionRefs.current[0] = el }}
              className="mb-8 text-center pb-8 border-b border-border">
              <div className="flex items-center justify-center gap-3 mb-4">
                <VenueBadge venue={paper.target_venue} />
                {paper.paper_type && (
                  <span className="text-xs text-faint">
                    {paper.paper_type.replace('_', ' ')}
                  </span>
                )}
              </div>
              <h1 className="text-3xl font-bold leading-tight mb-4 text-text" style={{ lineHeight: 1.3 }}>
                {paper.title || paper.topic}
              </h1>
              {paper.author_name && (
                <p className="text-sm text-muted">
                  {paper.author_name}
                  {paper.author_affiliation && (
                    <span className="text-faint"> — {paper.author_affiliation}</span>
                  )}
                </p>
              )}
            </div>

            {/* Abstract */}
            {abstract && (
              <div className="mb-8 p-5 rounded-xl border border-accent/25 bg-accent/5">
                <p className="section-title mb-3 text-accent">
                  Abstract
                </p>
                <p className="text-sm leading-relaxed italic text-muted" style={{ lineHeight: 1.8 }}>
                  {abstract}
                </p>
              </div>
            )}

            {/* Keywords */}
            {Array.isArray(keywords) && keywords.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-8">
                {keywords.map((kw, i) => (
                  <span key={i} className="flex items-center gap-1 px-3 py-1 rounded-full text-xs bg-surface border border-border text-muted">
                    <Tag size={10} />
                    {kw}
                  </span>
                ))}
              </div>
            )}

            {/* Body sections */}
            {bodySections.map((section, i) => (
              <SectionContent
                key={section.key}
                heading={section.heading}
                content={section.content}
                sectionRef={(el) => { sectionRefs.current[i + 1] = el }}
              />
            ))}

            {/* References */}
            {citations.length > 0 && (
              <div ref={(el) => { sectionRefs.current[bodySections.length + 1] = el }}
                className="mt-10 pt-8 border-t border-border">
                <h2 className="text-xl font-semibold mb-6 flex items-center gap-2 text-text">
                  <BookOpen size={18} className="text-accent" />
                  References
                </h2>
                <ol className="space-y-3">
                  {citations.map((c, i) => (
                    <li key={i} className="flex gap-3">
                      <span className="text-xs font-semibold shrink-0 mt-0.5 w-6 text-right text-accent">
                        [{i + 1}]
                      </span>
                      <p className="text-sm text-faint" style={{ lineHeight: 1.6 }}>
                        {c.formatted_ieee || c.formatted_apa || c.title || JSON.stringify(c)}
                      </p>
                    </li>
                  ))}
                </ol>
              </div>
            )}
          </div>
        </div>

        {/* Right: Confidence report */}
        <div className="lg:col-span-3">
          <ConfidenceReport report={confidence} />
        </div>
      </div>

      {/* Bottom action bar */}
      <div className="fixed bottom-0 left-0 right-0 border-t border-border px-6 py-4 flex items-center justify-between z-40 bg-bg/95 backdrop-blur">
        <div className="flex items-center gap-4">
          {confidence?.total_word_count > 0 && (
            <span className="text-sm text-faint">
              ~{confidence.total_word_count.toLocaleString()} words
            </span>
          )}
          {citations.length > 0 && (
            <span className="text-sm text-faint">
              {citations.length} references
            </span>
          )}
        </div>
        <Link
          to={`/paper/${paperId}/export`}
          className="btn btn-primary text-sm flex items-center gap-2"
        >
          <Download size={15} />
          Export Paper
          <ChevronRight size={14} />
        </Link>
      </div>
    </div>
  )
}
