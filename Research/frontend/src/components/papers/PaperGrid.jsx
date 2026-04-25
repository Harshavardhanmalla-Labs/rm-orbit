import PaperCard from './PaperCard'
import { SkeletonCard } from '../ui/Skeleton'
import EmptyState from '../ui/EmptyState'
import ErrorState from '../ui/ErrorState'
import { FlaskConical } from 'lucide-react'

const TABS = [
  { key: 'all', label: 'All', filter: () => true },
  { key: 'draft', label: 'Draft', filter: p => p.status === 'intake' },
  { key: 'running', label: 'Running', filter: p => ['processing', 'running'].includes(p.status) },
  { key: 'complete', label: 'Complete', filter: p => p.status === 'complete' },
  { key: 'failed', label: 'Failed', filter: p => p.status === 'failed' },
]

export default function PaperGrid({
  papers = [],
  loading = false,
  error = null,
  onRetry = () => {},
  onSelect = () => {},
  selectedId = null,
  activeTab = 'all',
  onTabChange = () => {},
  searchQuery = '',
  onNewPaper = () => {},
}) {
  // Filter by tab
  const tabFilter = TABS.find(t => t.key === activeTab)?.filter || TABS[0].filter
  const tabFiltered = papers.filter(tabFilter)

  // Filter by search query
  const displayedPapers = tabFiltered.filter(p => {
    const q = searchQuery.toLowerCase()
    return (
      (p.title || '').toLowerCase().includes(q) ||
      (p.topic || '').toLowerCase().includes(q) ||
      (p.niche || '').toLowerCase().includes(q)
    )
  })

  // Count per tab
  const tabCounts = TABS.map(t => ({
    ...t,
    count: papers.filter(t.filter).length,
  }))

  return (
    <div className="flex flex-col gap-4">
      {/* Tab bar */}
      <div className="flex gap-1 p-1 bg-surface rounded-xl border border-border w-fit">
        {tabCounts.map(tab => (
          <button
            key={tab.key}
            onClick={() => onTabChange(tab.key)}
            className={`px-3 py-1.5 rounded-lg text-[13px] font-medium transition-all ${
              activeTab === tab.key
                ? 'bg-raised text-text shadow-sm'
                : 'text-muted hover:text-text'
            }`}
          >
            {tab.label}
            {tab.count > 0 && <span className="ml-1.5 text-[10px] text-faint">({tab.count})</span>}
          </button>
        ))}
      </div>

      {/* Grid or states */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      ) : error ? (
        <ErrorState message={error} onRetry={onRetry} />
      ) : papers.length === 0 ? (
        <EmptyState
          icon={FlaskConical}
          title="No papers yet"
          description="Create your first paper and the AI pipeline will draft it end-to-end."
          action={
            <button onClick={onNewPaper} className="btn btn-primary px-5 py-2.5">
              + New Paper
            </button>
          }
        />
      ) : displayedPapers.length === 0 ? (
        <div className="col-span-full text-center py-16">
          <p className="text-[13px] text-muted">No papers match "{searchQuery}"</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
          {displayedPapers.map(paper => (
            <PaperCard
              key={paper.id}
              paper={paper}
              onSelect={onSelect}
              selected={selectedId === paper.id}
            />
          ))}
        </div>
      )}
    </div>
  )
}
