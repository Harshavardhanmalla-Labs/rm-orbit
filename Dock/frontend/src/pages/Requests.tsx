import { useEffect, useState } from 'react'
import {
  Button,
  Badge,
  Modal,
  Select,
  Spinner,
  EmptyState,
  useToast,
} from '@orbit-ui/react'
import { Plus, ClipboardList, Check, X } from 'lucide-react'
import { requestsApi, appsApi, type AccessRequest, type App } from '../api/dock'
import { formatRelativeTime } from '../lib/utils'

type Tab = 'pending' | 'all'

const STATUS_COLOR: Record<string, 'warning' | 'success' | 'danger' | 'neutral'> = {
  pending: 'warning',
  approved: 'success',
  rejected: 'danger',
  cancelled: 'neutral',
}

export default function Requests() {
  const { toast } = useToast()
  const [requests, setRequests] = useState<AccessRequest[]>([])
  const [apps, setApps] = useState<App[]>([])
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState<Tab>('pending')

  const [showModal, setShowModal] = useState(false)
  const [createLoading, setCreateLoading] = useState(false)
  const [form, setForm] = useState({ app_id: '', justification: '' })

  const [actionLoading, setActionLoading] = useState<string | null>(null)

  async function fetchData() {
    setLoading(true)
    try {
      const [reqRes, appRes] = await Promise.all([requestsApi.list(), appsApi.list()])
      setRequests(reqRes.data)
      setApps(appRes.data)
    } catch {
      toast({ variant: 'error', title: 'Failed to load requests' })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void fetchData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function handleCreate() {
    if (!form.app_id) return
    setCreateLoading(true)
    try {
      await requestsApi.create({
        app_id: form.app_id,
        justification: form.justification || undefined,
      })
      toast({ variant: 'success', title: 'Access request submitted' })
      setShowModal(false)
      setForm({ app_id: '', justification: '' })
      void fetchData()
    } catch {
      toast({ variant: 'error', title: 'Failed to submit request' })
    } finally {
      setCreateLoading(false)
    }
  }

  async function handleAction(id: string, status: 'approved' | 'rejected') {
    setActionLoading(id + status)
    try {
      await requestsApi.update(id, { status })
      toast({
        variant: status === 'approved' ? 'success' : 'warning',
        title: `Request ${status}`,
      })
      void fetchData()
    } catch {
      toast({ variant: 'error', title: 'Action failed' })
    } finally {
      setActionLoading(null)
    }
  }

  const displayed = tab === 'pending'
    ? requests.filter((r) => r.status === 'pending')
    : requests

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-content-primary">Access Requests</h1>
          <p className="text-sm text-content-muted mt-0.5">Review and manage software access requests</p>
        </div>
        <Button
          variant="primary"
          size="sm"
          iconLeft={<Plus />}
          onClick={() => setShowModal(true)}
        >
          New Request
        </Button>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 p-1 bg-surface-muted rounded-lg w-fit">
        {(['pending', 'all'] as Tab[]).map((t) => {
          const count = t === 'pending' ? requests.filter((r) => r.status === 'pending').length : requests.length
          return (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${
                tab === t
                  ? 'bg-surface-elevated text-content-primary shadow-sm'
                  : 'text-content-muted hover:text-content-primary'
              }`}
            >
              {t === 'pending' ? 'Pending' : 'All'}
              {count > 0 && (
                <span className="ml-1.5 text-xs bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300 px-1.5 py-0.5 rounded-full">
                  {count}
                </span>
              )}
            </button>
          )
        })}
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      ) : displayed.length === 0 ? (
        <EmptyState
          icon={<ClipboardList />}
          title={tab === 'pending' ? 'No pending requests' : 'No requests found'}
          description={tab === 'pending' ? 'All access requests have been reviewed.' : 'No access requests have been submitted yet.'}
        />
      ) : (
        <div className="overflow-x-auto rounded-xl border border-border-default">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-surface-muted border-b border-border-default">
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">App</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Requester</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Justification</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Status</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Requested</th>
                {tab === 'pending' && <th className="px-4 py-3" />}
              </tr>
            </thead>
            <tbody>
              {displayed.map((req) => (
                <tr key={req.id} className="border-b border-border-subtle hover:bg-surface-muted/50 transition-colors">
                  <td className="px-4 py-3 font-medium text-content-primary">
                    {req.app_name ?? req.app_id}
                  </td>
                  <td className="px-4 py-3 text-content-muted">
                    {req.requester_email ?? req.requester_id}
                  </td>
                  <td className="px-4 py-3 text-content-muted max-w-[200px]">
                    <span className="line-clamp-2 text-xs">
                      {req.justification ?? '—'}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <Badge
                      color={STATUS_COLOR[req.status] ?? 'neutral'}
                      variant="subtle"
                      size="sm"
                    >
                      {req.status}
                    </Badge>
                  </td>
                  <td className="px-4 py-3 text-content-muted text-xs">
                    {formatRelativeTime(req.requested_at)}
                  </td>
                  {tab === 'pending' && (
                    <td className="px-4 py-3">
                      {req.status === 'pending' && (
                        <div className="flex gap-1.5">
                          <Button
                            variant="success"
                            size="xs"
                            iconLeft={<Check />}
                            loading={actionLoading === req.id + 'approved'}
                            onClick={() => void handleAction(req.id, 'approved')}
                          >
                            Approve
                          </Button>
                          <Button
                            variant="danger"
                            size="xs"
                            iconLeft={<X />}
                            loading={actionLoading === req.id + 'rejected'}
                            onClick={() => void handleAction(req.id, 'rejected')}
                          >
                            Reject
                          </Button>
                        </div>
                      )}
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* New Request Modal */}
      <Modal open={showModal} onClose={() => setShowModal(false)}>
        <Modal.Header>
          <Modal.Title>New Access Request</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="space-y-4">
            <Select
              label="App *"
              value={form.app_id}
              onChange={(e) => setForm((f) => ({ ...f, app_id: e.target.value }))}
              fullWidth
              placeholder="Select an app"
            >
              {apps.map((a) => (
                <option key={a.id} value={a.id}>{a.name}</option>
              ))}
            </Select>
            <div>
              <label className="block text-sm font-medium text-content-secondary mb-1.5">
                Justification
              </label>
              <textarea
                className="w-full rounded-input border border-border-default bg-surface-base text-content-primary text-sm px-3 py-2 min-h-[100px] resize-y focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-border-focus"
                placeholder="Why do you need access to this software?"
                value={form.justification}
                onChange={(e) => setForm((f) => ({ ...f, justification: e.target.value }))}
              />
            </div>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Cancel
          </Button>
          <Button variant="primary" loading={createLoading} onClick={() => void handleCreate()}>
            Submit Request
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
