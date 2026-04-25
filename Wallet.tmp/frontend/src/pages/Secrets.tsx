import { useState, useEffect, useCallback, useRef } from 'react'
import {
  Plus,
  Eye,
  EyeOff,
  Trash2,
  Copy,
  Check,
  KeyRound,
  ShieldCheck,
  Hash,
  Lock,
} from 'lucide-react'
import {
  Button,
  Badge,
  Modal,
  Input,
  Select,
  Textarea,
  Skeleton,
  useToast,
} from '@orbit-ui/react'
import { secretsApi, type Secret } from '../api/wallet'
import { formatRelativeTime } from '../lib/utils'

// ─── Type badge config ───────────────────────────────────────────────────────

type BadgeColor = 'primary' | 'warning' | 'info' | 'success' | 'neutral'

const TYPE_BADGE: Record<string, BadgeColor> = {
  api_key: 'primary',
  password: 'warning',
  token: 'info',
  certificate: 'success',
  ssh_key: 'neutral',
  other: 'neutral',
}

const TYPE_LABELS: Record<string, string> = {
  api_key: 'API Key',
  password: 'Password',
  token: 'Token',
  certificate: 'Certificate',
  ssh_key: 'SSH Key',
  other: 'Other',
}

// ─── Stat Card ───────────────────────────────────────────────────────────────

function StatCard({
  label,
  value,
  icon: Icon,
  color,
}: {
  label: string
  value: number
  icon: React.ElementType
  color: string
}) {
  return (
    <div className="bg-surface-elevated border border-border-default rounded-xl p-4 flex items-center gap-3">
      <div className={`w-10 h-10 rounded-lg ${color} flex items-center justify-center shrink-0`}>
        <Icon size={18} className="text-white" />
      </div>
      <div>
        <p className="text-2xl font-bold text-content-primary leading-none">{value}</p>
        <p className="text-xs text-content-muted mt-0.5">{label}</p>
      </div>
    </div>
  )
}

// ─── Reveal Modal ────────────────────────────────────────────────────────────

function RevealModal({
  secret,
  value,
  onClose,
}: {
  secret: Secret
  value: string
  onClose: () => void
}) {
  const [copied, setCopied] = useState(false)
  const [countdown, setCountdown] = useState(30)

  useEffect(() => {
    const interval = setInterval(() => {
      setCountdown((c) => {
        if (c <= 1) {
          clearInterval(interval)
          onClose()
          return 0
        }
        return c - 1
      })
    }, 1000)
    return () => clearInterval(interval)
  }, [onClose])

  const handleCopy = () => {
    navigator.clipboard.writeText(value).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  return (
    <Modal open onClose={onClose} size="md">
      <Modal.Header>
        <Modal.Title>Secret Value — {secret.name}</Modal.Title>
        <Modal.Description>
          <span className="inline-flex items-center gap-1.5">
            <Badge color={TYPE_BADGE[secret.type] ?? 'neutral'} variant="subtle" size="sm">
              {TYPE_LABELS[secret.type] ?? secret.type}
            </Badge>
          </span>
        </Modal.Description>
      </Modal.Header>
      <Modal.Body>
        <div className="space-y-3">
          <div className="relative">
            <pre className="bg-surface-muted border border-border-default rounded-lg px-4 py-3 font-mono text-sm text-content-primary overflow-x-auto whitespace-pre-wrap break-all">
              {value}
            </pre>
            <Button
              size="sm"
              variant="ghost"
              iconLeft={copied ? <Check size={14} /> : <Copy size={14} />}
              onClick={handleCopy}
              className="absolute top-2 right-2"
            >
              {copied ? 'Copied' : 'Copy'}
            </Button>
          </div>
          <div className="flex items-start gap-2 p-3 rounded-lg bg-warning-50 dark:bg-warning-950 border border-warning-200 dark:border-warning-800">
            <ShieldCheck size={15} className="text-warning-600 dark:text-warning-400 mt-0.5 shrink-0" />
            <p className="text-xs text-warning-700 dark:text-warning-300">
              This value is encrypted at rest. Close when done.
            </p>
          </div>
        </div>
      </Modal.Body>
      <Modal.Footer>
        <p className="text-xs text-content-muted mr-auto">
          Auto-closing in {countdown}s
        </p>
        <Button variant="secondary" size="sm" onClick={onClose}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  )
}

// ─── Delete Confirm Modal ────────────────────────────────────────────────────

function DeleteModal({
  secret,
  onConfirm,
  onClose,
  loading,
}: {
  secret: Secret
  onConfirm: () => void
  onClose: () => void
  loading: boolean
}) {
  return (
    <Modal open onClose={onClose} size="sm">
      <Modal.Header>
        <Modal.Title>Delete Secret</Modal.Title>
        <Modal.Description>
          This action cannot be undone.
        </Modal.Description>
      </Modal.Header>
      <Modal.Body>
        <p className="text-sm text-content-secondary">
          Are you sure you want to delete{' '}
          <span className="font-semibold text-content-primary">{secret.name}</span>?
        </p>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" size="sm" onClick={onClose} disabled={loading}>
          Cancel
        </Button>
        <Button variant="danger" size="sm" onClick={onConfirm} loading={loading}>
          Delete
        </Button>
      </Modal.Footer>
    </Modal>
  )
}

// ─── Create Modal ────────────────────────────────────────────────────────────

const SECRET_TYPES = [
  { value: 'api_key', label: 'API Key' },
  { value: 'password', label: 'Password' },
  { value: 'token', label: 'Token' },
  { value: 'certificate', label: 'Certificate' },
  { value: 'ssh_key', label: 'SSH Key' },
  { value: 'other', label: 'Other' },
]

interface CreateForm {
  name: string
  type: string
  value: string
  project: string
  tags: string
  notes: string
}

function CreateModal({
  onCreated,
  onClose,
}: {
  onCreated: (secret: Secret) => void
  onClose: () => void
}) {
  const { toast } = useToast()
  const [form, setForm] = useState<CreateForm>({
    name: '',
    type: 'api_key',
    value: '',
    project: '',
    tags: '',
    notes: '',
  })
  const [showValue, setShowValue] = useState(false)
  const [loading, setLoading] = useState(false)

  const update = (field: keyof CreateForm) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) =>
    setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.name.trim() || !form.type || !form.value.trim()) return
    setLoading(true)
    try {
      const res = await secretsApi.create({
        name: form.name.trim(),
        type: form.type,
        value: form.value,
        project: form.project.trim() || undefined,
        tags: form.tags ? form.tags.split(',').map((t) => t.trim()).filter(Boolean) : undefined,
        notes: form.notes.trim() || undefined,
      })
      toast({ variant: 'success', title: 'Secret created', message: `${res.data.name} has been saved.` })
      onCreated(res.data)
    } catch {
      toast({ variant: 'error', title: 'Failed to create secret' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Modal open onClose={onClose} size="md">
      <Modal.Header>
        <Modal.Title>New Secret</Modal.Title>
        <Modal.Description>Add a new credential to the vault</Modal.Description>
      </Modal.Header>
      <Modal.Body>
        <form id="create-secret-form" onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-sm font-medium text-content-primary">
              Name <span className="text-danger-500">*</span>
            </label>
            <Input
              placeholder="e.g. Stripe API Key"
              value={form.name}
              onChange={update('name')}
              required
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-sm font-medium text-content-primary">
              Type <span className="text-danger-500">*</span>
            </label>
            <Select value={form.type} onChange={update('type')} required>
              {SECRET_TYPES.map((t) => (
                <option key={t.value} value={t.value}>
                  {t.label}
                </option>
              ))}
            </Select>
          </div>

          <div className="space-y-1.5">
            <label className="text-sm font-medium text-content-primary">
              Value <span className="text-danger-500">*</span>
            </label>
            <div className="relative">
              <Input
                type={showValue ? 'text' : 'password'}
                placeholder="Enter secret value"
                value={form.value}
                onChange={update('value')}
                required
                className="pr-10"
              />
              <button
                type="button"
                onClick={() => setShowValue((s) => !s)}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-content-muted hover:text-content-primary"
                tabIndex={-1}
              >
                {showValue ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-sm font-medium text-content-primary">Project</label>
            <Input
              placeholder="e.g. my-project (optional)"
              value={form.project}
              onChange={update('project')}
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-sm font-medium text-content-primary">Tags</label>
            <Input
              placeholder="comma-separated, e.g. production, billing"
              value={form.tags}
              onChange={update('tags')}
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-sm font-medium text-content-primary">Notes</label>
            <Textarea
              placeholder="Optional notes about this secret"
              value={form.notes}
              onChange={update('notes')}
              rows={3}
            />
          </div>
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" size="sm" onClick={onClose} disabled={loading}>
          Cancel
        </Button>
        <Button
          type="submit"
          form="create-secret-form"
          size="sm"
          loading={loading}
          disabled={!form.name.trim() || !form.value.trim()}
        >
          Save Secret
        </Button>
      </Modal.Footer>
    </Modal>
  )
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function Secrets() {
  const { toast } = useToast()
  const [secrets, setSecrets] = useState<Secret[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [typeFilter, setTypeFilter] = useState('')

  // Modals
  const [revealData, setRevealData] = useState<{ secret: Secret; value: string } | null>(null)
  const [deleteTarget, setDeleteTarget] = useState<Secret | null>(null)
  const [deleteLoading, setDeleteLoading] = useState(false)
  const [showCreate, setShowCreate] = useState(false)
  const [revealLoading, setRevealLoading] = useState<string | null>(null)

  // Debounce search
  const searchTimeout = useRef<ReturnType<typeof setTimeout> | null>(null)
  const [debouncedSearch, setDebouncedSearch] = useState('')

  useEffect(() => {
    if (searchTimeout.current) clearTimeout(searchTimeout.current)
    searchTimeout.current = setTimeout(() => setDebouncedSearch(search), 300)
    return () => {
      if (searchTimeout.current) clearTimeout(searchTimeout.current)
    }
  }, [search])

  const fetchSecrets = useCallback(async () => {
    setLoading(true)
    try {
      const res = await secretsApi.list({
        search: debouncedSearch || undefined,
        type: typeFilter || undefined,
      })
      setSecrets(res.data)
    } catch {
      toast({ variant: 'error', title: 'Failed to load secrets' })
    } finally {
      setLoading(false)
    }
  }, [debouncedSearch, typeFilter, toast])

  useEffect(() => {
    void fetchSecrets()
  }, [fetchSecrets])

  const handleReveal = async (secret: Secret) => {
    setRevealLoading(secret.id)
    try {
      const res = await secretsApi.reveal(secret.id)
      setRevealData({ secret, value: res.data.value })
    } catch {
      toast({ variant: 'error', title: 'Failed to reveal secret' })
    } finally {
      setRevealLoading(null)
    }
  }

  const handleDelete = async () => {
    if (!deleteTarget) return
    setDeleteLoading(true)
    try {
      await secretsApi.delete(deleteTarget.id)
      setSecrets((s) => s.filter((x) => x.id !== deleteTarget.id))
      toast({ variant: 'success', title: 'Secret deleted' })
      setDeleteTarget(null)
    } catch {
      toast({ variant: 'error', title: 'Failed to delete secret' })
    } finally {
      setDeleteLoading(false)
    }
  }

  const handleCreated = (secret: Secret) => {
    setSecrets((s) => [secret, ...s])
    setShowCreate(false)
  }

  // Stats
  const total = secrets.length
  const apiKeys = secrets.filter((s) => s.type === 'api_key').length
  const tokens = secrets.filter((s) => s.type === 'token').length
  const passwords = secrets.filter((s) => s.type === 'password').length

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-content-primary">Secrets</h1>
          <p className="text-sm text-content-muted mt-0.5">Manage your encrypted credentials</p>
        </div>
        <Button iconLeft={<Plus size={16} />} onClick={() => setShowCreate(true)}>
          New Secret
        </Button>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <StatCard label="Total Secrets" value={total} icon={Lock} color="bg-primary-600" />
        <StatCard label="API Keys" value={apiKeys} icon={KeyRound} color="bg-info-500" />
        <StatCard label="Tokens" value={tokens} icon={Hash} color="bg-success-500" />
        <StatCard label="Passwords" value={passwords} icon={ShieldCheck} color="bg-warning-500" />
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="flex-1">
          <Input
            placeholder="Search secrets..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="w-full sm:w-48">
          <Select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
            <option value="">All Types</option>
            <option value="api_key">API Key</option>
            <option value="password">Password</option>
            <option value="token">Token</option>
            <option value="certificate">Certificate</option>
            <option value="ssh_key">SSH Key</option>
            <option value="other">Other</option>
          </Select>
        </div>
      </div>

      {/* Table */}
      <div className="bg-surface-elevated border border-border-default rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border-subtle bg-surface-muted/50">
                <th className="text-left px-4 py-3 font-semibold text-content-secondary text-xs uppercase tracking-wide">
                  Name
                </th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary text-xs uppercase tracking-wide">
                  Type
                </th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary text-xs uppercase tracking-wide hidden md:table-cell">
                  Project
                </th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary text-xs uppercase tracking-wide hidden lg:table-cell">
                  Tags
                </th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary text-xs uppercase tracking-wide hidden sm:table-cell">
                  Updated
                </th>
                <th className="text-right px-4 py-3 font-semibold text-content-secondary text-xs uppercase tracking-wide">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                Array.from({ length: 5 }).map((_, i) => (
                  <tr key={i} className="border-b border-border-subtle last:border-0">
                    <td className="px-4 py-3"><Skeleton className="h-4 w-36" /></td>
                    <td className="px-4 py-3"><Skeleton className="h-5 w-20" /></td>
                    <td className="px-4 py-3 hidden md:table-cell"><Skeleton className="h-4 w-24" /></td>
                    <td className="px-4 py-3 hidden lg:table-cell"><Skeleton className="h-5 w-28" /></td>
                    <td className="px-4 py-3 hidden sm:table-cell"><Skeleton className="h-4 w-20" /></td>
                    <td className="px-4 py-3"><Skeleton className="h-7 w-20 ml-auto" /></td>
                  </tr>
                ))
              ) : secrets.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-4 py-12 text-center text-content-muted text-sm">
                    No secrets found. Add your first secret to get started.
                  </td>
                </tr>
              ) : (
                secrets.map((secret) => (
                  <tr
                    key={secret.id}
                    className="border-b border-border-subtle last:border-0 hover:bg-surface-muted/40 transition-colors"
                  >
                    <td className="px-4 py-3">
                      <div>
                        <p className="font-medium text-content-primary">{secret.name}</p>
                        <p className="text-xs text-content-muted font-mono mt-0.5">{secret.masked_value}</p>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <Badge color={TYPE_BADGE[secret.type] ?? 'neutral'} variant="subtle">
                        {TYPE_LABELS[secret.type] ?? secret.type}
                      </Badge>
                    </td>
                    <td className="px-4 py-3 hidden md:table-cell">
                      <span className="text-content-secondary text-sm">
                        {secret.project ?? <span className="text-content-muted">—</span>}
                      </span>
                    </td>
                    <td className="px-4 py-3 hidden lg:table-cell">
                      <div className="flex flex-wrap gap-1">
                        {secret.tags.length === 0 ? (
                          <span className="text-content-muted text-xs">—</span>
                        ) : (
                          secret.tags.map((tag) => (
                            <Badge key={tag} color="neutral" variant="outline" size="sm">
                              {tag}
                            </Badge>
                          ))
                        )}
                      </div>
                    </td>
                    <td className="px-4 py-3 hidden sm:table-cell">
                      <span className="text-xs text-content-muted">
                        {formatRelativeTime(secret.updated_at)}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-end gap-1.5">
                        <Button
                          size="sm"
                          variant="ghost"
                          iconLeft={<Eye size={14} />}
                          onClick={() => handleReveal(secret)}
                          loading={revealLoading === secret.id}
                        >
                          Reveal
                        </Button>
                        <Button
                          size="sm"
                          variant="ghost"
                          iconLeft={<Trash2 size={14} />}
                          onClick={() => setDeleteTarget(secret)}
                          className="text-danger-600 hover:text-danger-700 hover:bg-danger-50 dark:hover:bg-danger-950"
                        >
                          Delete
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modals */}
      {revealData && (
        <RevealModal
          secret={revealData.secret}
          value={revealData.value}
          onClose={() => setRevealData(null)}
        />
      )}

      {deleteTarget && (
        <DeleteModal
          secret={deleteTarget}
          onConfirm={handleDelete}
          onClose={() => setDeleteTarget(null)}
          loading={deleteLoading}
        />
      )}

      {showCreate && (
        <CreateModal onCreated={handleCreated} onClose={() => setShowCreate(false)} />
      )}
    </div>
  )
}
