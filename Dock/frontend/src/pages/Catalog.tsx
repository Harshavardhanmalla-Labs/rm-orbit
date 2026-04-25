import { useEffect, useState } from 'react'
import {
  Button,
  Badge,
  Modal,
  Input,
  Select,
  Spinner,
  EmptyState,
  useToast,
} from '@orbit-ui/react'
import { Plus, LayoutGrid, Search } from 'lucide-react'
import { appsApi, requestsApi, type App } from '../api/dock'
import { formatDate } from '../lib/utils'

type AppStatus = 'active' | 'inactive' | 'deprecated' | 'beta'

const STATUS_COLOR: Record<string, 'success' | 'neutral' | 'warning' | 'info'> = {
  active: 'success',
  inactive: 'neutral',
  deprecated: 'warning',
  beta: 'info',
}

const LICENSE_TYPES = ['subscription', 'perpetual', 'open_source', 'freeware', 'trial']
const CATEGORIES = ['productivity', 'development', 'communication', 'security', 'analytics', 'design', 'other']
const STATUSES: AppStatus[] = ['active', 'inactive', 'deprecated', 'beta']

function AppCard({ app, onRequest }: { app: App; onRequest: (app: App) => void }) {
  const statusColor = STATUS_COLOR[app.status] ?? 'neutral'
  return (
    <div className="flex flex-col bg-surface-elevated border border-border-default rounded-xl p-4 gap-3 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <h3 className="font-semibold text-content-primary text-sm truncate">{app.name}</h3>
          {app.vendor && (
            <p className="text-xs text-content-muted mt-0.5 truncate">{app.vendor}</p>
          )}
        </div>
        <Badge color={statusColor} variant="subtle" size="sm">
          {app.status}
        </Badge>
      </div>

      <div className="flex flex-wrap gap-1.5">
        {app.category && (
          <Badge color="primary" variant="subtle" size="sm">
            {app.category}
          </Badge>
        )}
        {app.license_type && (
          <Badge color="neutral" variant="outline" size="sm">
            {app.license_type}
          </Badge>
        )}
        {app.version && (
          <Badge color="neutral" variant="subtle" size="sm">
            v{app.version}
          </Badge>
        )}
      </div>

      {app.description && (
        <p className="text-xs text-content-muted line-clamp-2 flex-1">{app.description}</p>
      )}

      {app.cost_per_seat != null && (
        <p className="text-xs font-semibold text-content-secondary">
          ${app.cost_per_seat.toFixed(2)} / seat
        </p>
      )}

      <Button
        variant="outline"
        size="sm"
        fullWidth
        onClick={() => onRequest(app)}
      >
        Request Access
      </Button>
    </div>
  )
}

export default function Catalog() {
  const { toast } = useToast()
  const [apps, setApps] = useState<App[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')

  const [showAddModal, setShowAddModal] = useState(false)
  const [addLoading, setAddLoading] = useState(false)
  const [addForm, setAddForm] = useState({
    name: '',
    vendor: '',
    category: '',
    description: '',
    version: '',
    license_type: '',
    cost_per_seat: '',
    status: 'active' as AppStatus,
  })

  const [requestingApp, setRequestingApp] = useState<App | null>(null)
  const [requestJustification, setRequestJustification] = useState('')
  const [requestLoading, setRequestLoading] = useState(false)

  async function fetchApps() {
    setLoading(true)
    try {
      const res = await appsApi.list({
        search: search || undefined,
        status: statusFilter || undefined,
        category: categoryFilter || undefined,
      })
      setApps(res.data)
    } catch {
      toast({ variant: 'error', title: 'Failed to load apps' })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void fetchApps()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [search, statusFilter, categoryFilter])

  async function handleAddApp() {
    if (!addForm.name.trim()) return
    setAddLoading(true)
    try {
      await appsApi.create({
        name: addForm.name.trim(),
        vendor: addForm.vendor || null,
        category: addForm.category || null,
        description: addForm.description || null,
        version: addForm.version || null,
        license_type: addForm.license_type || null,
        cost_per_seat: addForm.cost_per_seat ? parseFloat(addForm.cost_per_seat) : null,
        status: addForm.status,
      })
      toast({ variant: 'success', title: 'App added to catalog' })
      setShowAddModal(false)
      setAddForm({ name: '', vendor: '', category: '', description: '', version: '', license_type: '', cost_per_seat: '', status: 'active' })
      void fetchApps()
    } catch {
      toast({ variant: 'error', title: 'Failed to add app' })
    } finally {
      setAddLoading(false)
    }
  }

  async function handleRequest() {
    if (!requestingApp) return
    setRequestLoading(true)
    try {
      await requestsApi.create({
        app_id: requestingApp.id,
        justification: requestJustification || undefined,
      })
      toast({ variant: 'success', title: 'Access request submitted', message: `Request for ${requestingApp.name} sent.` })
      setRequestingApp(null)
      setRequestJustification('')
    } catch {
      toast({ variant: 'error', title: 'Failed to submit request' })
    } finally {
      setRequestLoading(false)
    }
  }

  const totalApps = apps.length
  const activeApps = apps.filter((a) => a.status === 'active').length
  const categories = new Set(apps.map((a) => a.category).filter(Boolean)).size

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-content-primary">Software Catalog</h1>
          <p className="text-sm text-content-muted mt-0.5">Browse and request access to approved enterprise software</p>
        </div>
        <Button
          variant="primary"
          size="sm"
          iconLeft={<Plus />}
          onClick={() => setShowAddModal(true)}
        >
          Add App
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: 'Total Apps', value: totalApps },
          { label: 'Active', value: activeApps },
          { label: 'Categories', value: categories },
          { label: 'My Requests', value: '—' },
        ].map((stat) => (
          <div key={stat.label} className="bg-surface-elevated border border-border-default rounded-xl p-4">
            <p className="text-2xl font-bold text-content-primary">{stat.value}</p>
            <p className="text-xs text-content-muted mt-1">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <Input
          placeholder="Search apps..."
          prefix={<Search className="size-4 text-content-muted" />}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-56"
        />
        <Select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="w-36"
        >
          <option value="">All statuses</option>
          {STATUSES.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </Select>
        <Select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="w-40"
        >
          <option value="">All categories</option>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </Select>
      </div>

      {/* App Grid */}
      {loading ? (
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      ) : apps.length === 0 ? (
        <EmptyState
          icon={<LayoutGrid />}
          title="No apps found"
          description="Try adjusting your search or filters."
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {apps.map((app) => (
            <AppCard key={app.id} app={app} onRequest={setRequestingApp} />
          ))}
        </div>
      )}

      {/* Add App Modal */}
      <Modal open={showAddModal} onClose={() => setShowAddModal(false)} size="lg">
        <Modal.Header>
          <Modal.Title>Add App to Catalog</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="space-y-4">
            <Input
              label="App Name *"
              placeholder="e.g. Slack"
              value={addForm.name}
              onChange={(e) => setAddForm((f) => ({ ...f, name: e.target.value }))}
              fullWidth
            />
            <div className="grid grid-cols-2 gap-3">
              <Input
                label="Vendor"
                placeholder="e.g. Salesforce"
                value={addForm.vendor}
                onChange={(e) => setAddForm((f) => ({ ...f, vendor: e.target.value }))}
                fullWidth
              />
              <Input
                label="Version"
                placeholder="e.g. 1.0.0"
                value={addForm.version}
                onChange={(e) => setAddForm((f) => ({ ...f, version: e.target.value }))}
                fullWidth
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <Select
                label="Category"
                value={addForm.category}
                onChange={(e) => setAddForm((f) => ({ ...f, category: e.target.value }))}
                fullWidth
              >
                <option value="">Select category</option>
                {CATEGORIES.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </Select>
              <Select
                label="Status"
                value={addForm.status}
                onChange={(e) => setAddForm((f) => ({ ...f, status: e.target.value as AppStatus }))}
                fullWidth
              >
                {STATUSES.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </Select>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <Select
                label="License Type"
                value={addForm.license_type}
                onChange={(e) => setAddForm((f) => ({ ...f, license_type: e.target.value }))}
                fullWidth
              >
                <option value="">Select type</option>
                {LICENSE_TYPES.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </Select>
              <Input
                label="Cost per Seat ($)"
                type="number"
                placeholder="0.00"
                value={addForm.cost_per_seat}
                onChange={(e) => setAddForm((f) => ({ ...f, cost_per_seat: e.target.value }))}
                fullWidth
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-content-secondary mb-1.5">
                Description
              </label>
              <textarea
                className="w-full rounded-input border border-border-default bg-surface-base text-content-primary text-sm px-3 py-2 min-h-[80px] resize-y focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-border-focus"
                placeholder="Brief description of the app..."
                value={addForm.description}
                onChange={(e) => setAddForm((f) => ({ ...f, description: e.target.value }))}
              />
            </div>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowAddModal(false)}>
            Cancel
          </Button>
          <Button variant="primary" loading={addLoading} onClick={() => void handleAddApp()}>
            Add App
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Request Access Modal */}
      <Modal open={!!requestingApp} onClose={() => setRequestingApp(null)}>
        <Modal.Header>
          <Modal.Title>Request Access</Modal.Title>
          {requestingApp && (
            <p className="text-sm text-content-muted mt-1">
              Requesting access to <strong>{requestingApp.name}</strong>
            </p>
          )}
        </Modal.Header>
        <Modal.Body>
          <div>
            <label className="block text-sm font-medium text-content-secondary mb-1.5">
              Justification (optional)
            </label>
            <textarea
              className="w-full rounded-input border border-border-default bg-surface-base text-content-primary text-sm px-3 py-2 min-h-[100px] resize-y focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-border-focus"
              placeholder="Why do you need access to this app?"
              value={requestJustification}
              onChange={(e) => setRequestJustification(e.target.value)}
            />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setRequestingApp(null)}>
            Cancel
          </Button>
          <Button variant="primary" loading={requestLoading} onClick={() => void handleRequest()}>
            Submit Request
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}

// Needed for formatDate usage in stat cards (future use)
void formatDate
