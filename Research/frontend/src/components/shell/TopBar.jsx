import { useLocation, useSearchParams, useMatch } from 'react-router-dom'
import { Plus, Search, X } from 'lucide-react'
import { useModal } from '../../context/ModalContext'

const TITLES = {
  '/papers': 'Research Papers',
  '/system': 'System Status',
}

export default function TopBar() {
  const location = useLocation()
  const [searchParams, setSearchParams] = useSearchParams()
  const isOnPapersRoute = useMatch('/papers')
  const { setNewPaperModalOpen } = useModal()

  const searchQuery = searchParams.get('q') || ''
  const title = Object.entries(TITLES).find(([path]) => location.pathname.startsWith(path))?.[1] || 'Research'

  function handleSearchChange(e) {
    const value = e.target.value
    if (value) {
      setSearchParams({ q: value })
    } else {
      setSearchParams({})
    }
  }

  function handleClearSearch() {
    setSearchParams({})
  }

  return (
    <header className="h-[52px] flex items-center px-6 gap-4 border-b border-border bg-surface shrink-0">
      <h1 className="text-[15px] font-bold text-text flex-1">{title}</h1>

      {isOnPapersRoute && (
        <div className="relative w-[220px]">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-faint" />
          <input
            type="text"
            placeholder="Search papers..."
            value={searchQuery}
            onChange={handleSearchChange}
            className="w-full pl-9 pr-9 py-2 rounded-lg bg-raised border border-border text-[13px] text-text placeholder:text-faint outline-none focus:border-accent/50 transition-colors"
          />
          {searchQuery && (
            <button
              onClick={handleClearSearch}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-faint hover:text-text transition-colors"
            >
              <X size={14} />
            </button>
          )}
        </div>
      )}

      <button
        onClick={() => setNewPaperModalOpen(true)}
        className="btn btn-primary text-[13px] px-4 py-2 flex items-center gap-1.5"
      >
        <Plus size={14} />
        New Paper
      </button>
    </header>
  )
}
