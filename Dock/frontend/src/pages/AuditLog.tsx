import { useEffect, useState } from 'react'
import { Badge, Skeleton, EmptyState } from '@orbit-ui/react'
import { ScrollText } from 'lucide-react'
import { auditApi, type AuditEvent } from '../api/dock'
import { formatRelativeTime } from '../lib/utils'
import { useToast } from '@orbit-ui/react'

const ACTION_COLOR: Record<string, 'success' | 'danger' | 'info' | 'warning' | 'neutral'> = {
  create: 'success',
  created: 'success',
  update: 'info',
  updated: 'info',
  delete: 'danger',
  deleted: 'danger',
  revoke: 'danger',
  revoked: 'danger',
  approve: 'success',
  approved: 'success',
  reject: 'warning',
  rejected: 'warning',
  assign: 'info',
  assigned: 'info',
}

function actionColor(action: string): 'success' | 'danger' | 'info' | 'warning' | 'neutral' {
  const lower = action.toLowerCase()
  for (const key of Object.keys(ACTION_COLOR)) {
    if (lower.includes(key)) return ACTION_COLOR[key]!
  }
  return 'neutral'
}

export default function AuditLog() {
  const { toast } = useToast()
  const [events, setEvents] = useState<AuditEvent[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    auditApi
      .list()
      .then((res) => setEvents(res.data))
      .catch(() => toast({ variant: 'error', title: 'Failed to load audit log' }))
      .finally(() => setLoading(false))
  }, [toast])

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-xl font-bold text-content-primary">Audit Log</h1>
        <p className="text-sm text-content-muted mt-0.5">Track all system actions and changes</p>
      </div>

      {loading ? (
        <div className="space-y-2">
          {Array.from({ length: 8 }).map((_, i) => (
            <Skeleton key={i} className="h-12 w-full rounded-lg" />
          ))}
        </div>
      ) : events.length === 0 ? (
        <EmptyState
          icon={<ScrollText />}
          title="No audit events"
          description="Audit events will appear here as actions are performed in the system."
          size="lg"
        />
      ) : (
        <div className="overflow-x-auto rounded-xl border border-border-default">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-surface-muted border-b border-border-default">
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Action</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Actor</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Resource Type</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Resource ID</th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary">Time</th>
              </tr>
            </thead>
            <tbody>
              {events.map((evt) => (
                <tr key={evt.id} className="border-b border-border-subtle hover:bg-surface-muted/50 transition-colors">
                  <td className="px-4 py-3">
                    <Badge color={actionColor(evt.action)} variant="subtle" size="sm">
                      {evt.action}
                    </Badge>
                  </td>
                  <td className="px-4 py-3 text-content-muted font-mono text-xs">
                    {evt.actor_id}
                  </td>
                  <td className="px-4 py-3">
                    <Badge color="neutral" variant="outline" size="sm">
                      {evt.resource_type}
                    </Badge>
                  </td>
                  <td className="px-4 py-3 text-content-muted font-mono text-xs truncate max-w-[140px]">
                    {evt.resource_id}
                  </td>
                  <td className="px-4 py-3 text-content-muted text-xs whitespace-nowrap">
                    {formatRelativeTime(evt.created_at)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
