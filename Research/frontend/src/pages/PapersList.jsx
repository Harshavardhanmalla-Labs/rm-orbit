import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { api } from '../api/client'
import { useModal } from '../context/ModalContext'
import MetricsStrip from '../components/papers/MetricsStrip'
import PaperGrid from '../components/papers/PaperGrid'
import PaperInspector from '../components/papers/PaperInspector'

export default function PapersList() {
  const { setNewPaperModalOpen } = useModal()
  const [searchParams] = useSearchParams()
  const [papers, setPapers] = useState([])
  const [brain, setBrain] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedPaper, setSelectedPaper] = useState(null)
  const [activeTab, setActiveTab] = useState('all')
  const pollInterval = 10000 // 10 seconds

  const searchQuery = searchParams.get('q') || ''

  // Fetch papers and brain on mount
  useEffect(() => {
    async function fetchData() {
      setLoading(true)
      try {
        const [papersRes, brainRes] = await Promise.all([
          api.get('/api/papers/'),
          api.get('/api/system/brain').catch(() => ({ data: null })), // brain is optional
        ])
        setPapers(papersRes.data.papers || [])
        setBrain(brainRes.data)
        setError(null)
      } catch (e) {
        setError(e.response?.data?.detail || e.message || 'Failed to load papers')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // Auto-poll papers every 10s when any are running
  useEffect(() => {
    const hasRunningPapers = papers.some(p => ['processing', 'running'].includes(p.status))

    if (!hasRunningPapers) return

    const interval = setInterval(async () => {
      try {
        const res = await api.get('/api/papers/')
        setPapers(res.data.papers || [])
      } catch (e) {
        console.error('Poll failed:', e)
      }
    }, pollInterval)

    return () => clearInterval(interval)
  }, [papers])

  // Update selected paper when papers change
  useEffect(() => {
    if (selectedPaper) {
      const updated = papers.find(p => p.id === selectedPaper.id)
      if (updated) {
        setSelectedPaper(updated)
      }
    }
  }, [papers])

  function handleRetry() {
    setLoading(true)
    setError(null)
    // Re-trigger the fetch by resetting state
    ;(async () => {
      try {
        const [papersRes, brainRes] = await Promise.all([
          api.get('/api/papers/'),
          api.get('/api/system/brain').catch(() => ({ data: null })),
        ])
        setPapers(papersRes.data.papers || [])
        setBrain(brainRes.data)
      } catch (e) {
        setError(e.response?.data?.detail || e.message || 'Failed to load papers')
      } finally {
        setLoading(false)
      }
    })()
  }

  function handleInspectorAction() {
    // Refresh papers after an action (start/cancel)
    ;(async () => {
      try {
        const res = await api.get('/api/papers/')
        setPapers(res.data.papers || [])
      } catch (e) {
        console.error('Refresh failed:', e)
      }
    })()
  }

  return (
    <div className="flex flex-1 overflow-hidden bg-canvas">
      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-y-auto">
        <div className="p-6 space-y-6">
          {/* Metrics */}
          <MetricsStrip papers={papers} brain={brain} />

          {/* Grid with filters */}
          <PaperGrid
            papers={papers}
            loading={loading}
            error={error}
            onRetry={handleRetry}
            onSelect={setSelectedPaper}
            selectedId={selectedPaper?.id}
            activeTab={activeTab}
            onTabChange={setActiveTab}
            searchQuery={searchQuery}
            onNewPaper={() => setNewPaperModalOpen(true)}
          />
        </div>
      </div>

      {/* Inspector panel */}
      {selectedPaper && (
        <PaperInspector
          paperId={selectedPaper.id}
          onClose={() => setSelectedPaper(null)}
          onAction={handleInspectorAction}
        />
      )}
    </div>
  )
}
