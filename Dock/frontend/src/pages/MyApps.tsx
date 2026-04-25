import { useEffect, useState } from 'react'
import { Button, Badge, Spinner, EmptyState, useToast } from '@orbit-ui/react'
import { User, ExternalLink, AlertCircle } from 'lucide-react'
import { appsApi, type App } from '../api/dock'

const STATUS_COLOR: Record<string, 'success' | 'neutral' | 'warning' | 'info'> = {
  active: 'success',
  inactive: 'neutral',
  deprecated: 'warning',
  beta: 'info',
}

function AppCard({ app, onReport }: { app: App; onReport: (name: string) => void }) {
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

      <div className="flex gap-2 mt-auto">
        <Button
          variant="primary"
          size="sm"
          iconLeft={<ExternalLink />}
          disabled
          fullWidth
        >
          Open App
        </Button>
        <Button
          variant="ghost"
          size="sm"
          iconLeft={<AlertCircle />}
          onClick={() => onReport(app.name)}
        >
          Issue
        </Button>
      </div>
    </div>
  )
}

export default function MyApps() {
  const { toast } = useToast()
  const [apps, setApps] = useState<App[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    appsApi
      .assigned()
      .then((res) => setApps(res.data))
      .catch(() => toast({ variant: 'error', title: 'Failed to load assigned apps' }))
      .finally(() => setLoading(false))
  }, [toast])

  function handleReport(appName: string) {
    toast({ variant: 'info', title: `Issue reported for ${appName}`, message: 'Our team will look into it.' })
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-xl font-bold text-content-primary">My Apps</h1>
        <p className="text-sm text-content-muted mt-0.5">Software assigned to your account</p>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      ) : apps.length === 0 ? (
        <EmptyState
          icon={<User />}
          title="No apps assigned"
          description="You don't have any software assigned yet. Browse the catalog to request access."
          size="lg"
        />
      ) : (
        <>
          <p className="text-sm text-content-muted">
            {apps.length} app{apps.length !== 1 ? 's' : ''} assigned to you
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {apps.map((app) => (
              <AppCard key={app.id} app={app} onReport={handleReport} />
            ))}
          </div>
        </>
      )}
    </div>
  )
}
