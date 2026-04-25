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
import { Plus, UserCheck } from 'lucide-react'
import { assignmentsApi, appsApi, type Assignment, type App } from '../api/dock'
import { formatDate, formatRelativeTime } from '../lib/utils'

export default function Assignments() {
  const { toast } = useToast()
  const [assignments, setAssignments] = useState<Assignment[]>([])
  const [apps, setApps] = useState<App[]>([])
  const [loading, setLoading] = useState(true)

  const [showModal, setShowModal] = useState(false)
  const [createLoading, setCreateLoading] = useState(false)
  const [form, setForm] = useState({ app_id: '', user_id: '', expires_at: '' })

  const [revokeTarget, setRevokeTarget] = useState<Assignment | null>(null)
  const [revokeLoading, setRevokeLoading] = useState(false)

  async function fetchData() {
    setLoading(true)
    try {
      const [asRes, appRes] = await Promise.all([assignmentsApi.list(), appsApi.list()])
      setAssignments(asRes.data)
      setApps(appRes.data)
    } catch {
      toast({ variant: 'error', title: 'Failed to load assignments' })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void fetchData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function handleCreate() {
    if (!form.app_id || !form.user_id.trim()) return
    setCreateLoading(true)
    try {
      await assignmentsApi.create({
        app_id: form.app_id,
        user_id: form.user_id.trim(),
        expires_at: form.expires_at || undefined,
      })
      toast({ variant: 'success', title: 'App assigned successfully' })
      setShowModal(false)
      setForm({ app_id: '', user_id: '', expires_at: '' })
      void fetchData()
    } catch {
      toast({ variant: 'error', title: 'Failed to create assignment' })
    } finally {
      setCreateLoading(false)
    }
  }

  async function handleRevoke() {
    if (!revokeTarget) return
    setRevokeLoading(true)
    try {
      await assignmentsApi.update(revokeTarget.id, { status: 'revoked' })
      toast({ variant: 'success', title: 'Assignment revoked' })
      setRevokeTarget(null)
      void fetchData()
    } catch {
      toast({ variant: 'error', title: 'Failed to revoke assignment' })
    } finally {
      setRevokeLoading(false)
    }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-content-primary">Assignments</h1>
          <p className="text-sm text-content-muted mt-0.5">Manage user software assignments</p>
        </div>
        <Button
          variant="primary"
          size="sm"
          iconLeft={<Plus />}
          onClick={() => setShowModal(true)}
        >
          Assign App
        </Button>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      ) : assignments.length === 0 ? (
        <EmptyState
          icon={<UserCheck />}
          title="No assignments"
          description="No software has been assigned to users yet."
          action={
            <Button variant="primary" size="sm" iconLeft={<Plus />} onClick={() => setShowModal(true)}>
              Assign App
            </Button>
          }
        />
      ) : (
        <div className="overflow-x-auto rounded-xl border border-border-default">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-surface-muted border-b border-border-default">
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">App</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">User</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Status</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Assigned</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Expires</th>
                <th className="px-4 py-3" />
              </tr>
            </thead>
            <tbody>
              {assignments.map((asgn) => (
                <tr key={asgn.id} className="border-b border-border-subtle hover:bg-surface-muted/50 transition-colors">
                  <td className="px-4 py-3 font-medium text-content-primary">
                    {asgn.app_name ?? asgn.app_id}
                  </td>
                  <td className="px-4 py-3 text-content-muted">
                    {asgn.user_email ?? asgn.user_id}
                  </td>
                  <td className="px-4 py-3">
                    <Badge
                      color={
                        asgn.status === 'active' ? 'success' :
                        asgn.status === 'revoked' ? 'danger' : 'neutral'
                      }
                      variant="subtle"
                      size="sm"
                    >
                      {asgn.status}
                    </Badge>
                  </td>
                  <td className="px-4 py-3 text-content-muted text-xs">
                    {formatRelativeTime(asgn.assigned_at)}
                  </td>
                  <td className="px-4 py-3 text-content-muted text-xs">
                    {formatDate(asgn.expires_at)}
                  </td>
                  <td className="px-4 py-3">
                    {asgn.status === 'active' && (
                      <Button
                        variant="danger"
                        size="xs"
                        onClick={() => setRevokeTarget(asgn)}
                      >
                        Revoke
                      </Button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Assign App Modal */}
      <Modal open={showModal} onClose={() => setShowModal(false)}>
        <Modal.Header>
          <Modal.Title>Assign App to User</Modal.Title>
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
            <Input
              label="User ID *"
              placeholder="e.g. user-123"
              value={form.user_id}
              onChange={(e) => setForm((f) => ({ ...f, user_id: e.target.value }))}
              fullWidth
            />
            <Input
              label="Expires At"
              type="date"
              value={form.expires_at}
              onChange={(e) => setForm((f) => ({ ...f, expires_at: e.target.value }))}
              fullWidth
            />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Cancel
          </Button>
          <Button variant="primary" loading={createLoading} onClick={() => void handleCreate()}>
            Assign
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Revoke Confirm Modal */}
      <Modal open={!!revokeTarget} onClose={() => setRevokeTarget(null)} size="sm">
        <Modal.Header>
          <Modal.Title>Revoke Assignment</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p className="text-sm text-content-secondary">
            Are you sure you want to revoke access to{' '}
            <strong>{revokeTarget?.app_name ?? revokeTarget?.app_id}</strong> for user{' '}
            <strong>{revokeTarget?.user_email ?? revokeTarget?.user_id}</strong>?
          </p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setRevokeTarget(null)}>
            Cancel
          </Button>
          <Button variant="danger" loading={revokeLoading} onClick={() => void handleRevoke()}>
            Revoke
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
