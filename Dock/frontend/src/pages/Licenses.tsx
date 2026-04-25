import { useEffect, useState } from 'react'
import {
  Button,
  Badge,
  Modal,
  Input,
  Select,
  Spinner,
  EmptyState,
  Progress,
  useToast,
} from '@orbit-ui/react'
import { Plus, FileKey } from 'lucide-react'
import { licensesApi, appsApi, type License, type App } from '../api/dock'
import { formatDate } from '../lib/utils'

function maskKey(key: string | null): string {
  if (!key) return '—'
  if (key.length <= 8) return key.slice(0, 3) + '***'
  return key.slice(0, 4) + '****' + key.slice(-4)
}

function seatVariant(pct: number): 'success' | 'warning' | 'danger' {
  if (pct >= 95) return 'danger'
  if (pct >= 80) return 'warning'
  return 'success'
}

export default function Licenses() {
  const { toast } = useToast()
  const [licenses, setLicenses] = useState<License[]>([])
  const [apps, setApps] = useState<App[]>([])
  const [loading, setLoading] = useState(true)

  const [showModal, setShowModal] = useState(false)
  const [createLoading, setCreateLoading] = useState(false)
  const [form, setForm] = useState({
    app_id: '',
    seats_total: '',
    license_key: '',
    expiry_date: '',
  })

  async function fetchData() {
    setLoading(true)
    try {
      const [licRes, appRes] = await Promise.all([licensesApi.list(), appsApi.list()])
      setLicenses(licRes.data)
      setApps(appRes.data)
    } catch {
      toast({ variant: 'error', title: 'Failed to load licenses' })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void fetchData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function handleCreate() {
    if (!form.app_id || !form.seats_total) return
    setCreateLoading(true)
    try {
      await licensesApi.create({
        app_id: form.app_id,
        seats_total: parseInt(form.seats_total),
        license_key: form.license_key || undefined,
        expiry_date: form.expiry_date || undefined,
      })
      toast({ variant: 'success', title: 'License created' })
      setShowModal(false)
      setForm({ app_id: '', seats_total: '', license_key: '', expiry_date: '' })
      void fetchData()
    } catch {
      toast({ variant: 'error', title: 'Failed to create license' })
    } finally {
      setCreateLoading(false)
    }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-content-primary">Licenses</h1>
          <p className="text-sm text-content-muted mt-0.5">Manage software license inventory and seat usage</p>
        </div>
        <Button
          variant="primary"
          size="sm"
          iconLeft={<Plus />}
          onClick={() => setShowModal(true)}
        >
          Add License
        </Button>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      ) : licenses.length === 0 ? (
        <EmptyState
          icon={<FileKey />}
          title="No licenses found"
          description="Add your first software license to start tracking seat usage."
          action={
            <Button variant="primary" size="sm" iconLeft={<Plus />} onClick={() => setShowModal(true)}>
              Add License
            </Button>
          }
        />
      ) : (
        <div className="overflow-x-auto rounded-xl border border-border-default">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-surface-muted border-b border-border-default">
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">App</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">License Key</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Seat Usage</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Expiry</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Status</th>
              </tr>
            </thead>
            <tbody>
              {licenses.map((lic) => {
                const pct = lic.seats_total > 0 ? (lic.seats_used / lic.seats_total) * 100 : 0
                const variant = seatVariant(pct)
                return (
                  <tr key={lic.id} className="border-b border-border-subtle hover:bg-surface-muted/50 transition-colors">
                    <td className="px-4 py-3 font-medium text-content-primary">
                      {lic.app_name ?? lic.app_id}
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-content-muted">
                      {maskKey(lic.license_key)}
                    </td>
                    <td className="px-4 py-3 min-w-[160px]">
                      <div className="flex items-center gap-2">
                        <Progress
                          value={lic.seats_used}
                          max={lic.seats_total}
                          variant={variant}
                          size="sm"
                          className="flex-1"
                        />
                        <span className="text-xs text-content-muted whitespace-nowrap">
                          {lic.seats_used}/{lic.seats_total}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-content-muted">
                      {formatDate(lic.expiry_date)}
                    </td>
                    <td className="px-4 py-3">
                      <Badge
                        color={lic.status === 'active' ? 'success' : 'neutral'}
                        variant="subtle"
                        size="sm"
                      >
                        {lic.status}
                      </Badge>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Create License Modal */}
      <Modal open={showModal} onClose={() => setShowModal(false)}>
        <Modal.Header>
          <Modal.Title>Add License</Modal.Title>
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
              label="Total Seats *"
              type="number"
              placeholder="e.g. 50"
              value={form.seats_total}
              onChange={(e) => setForm((f) => ({ ...f, seats_total: e.target.value }))}
              fullWidth
            />
            <Input
              label="License Key"
              placeholder="XXXX-XXXX-XXXX-XXXX"
              value={form.license_key}
              onChange={(e) => setForm((f) => ({ ...f, license_key: e.target.value }))}
              fullWidth
            />
            <Input
              label="Expiry Date"
              type="date"
              value={form.expiry_date}
              onChange={(e) => setForm((f) => ({ ...f, expiry_date: e.target.value }))}
              fullWidth
            />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Cancel
          </Button>
          <Button variant="primary" loading={createLoading} onClick={() => void handleCreate()}>
            Create License
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
