import { ScrollText } from 'lucide-react'
import { EmptyState } from '@orbit-ui/react'

export default function AuditLog() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-content-primary">Audit Log</h1>
        <p className="text-sm text-content-muted mt-0.5">Secret access history</p>
      </div>

      <div className="flex items-center justify-center min-h-96">
        <EmptyState
          icon={<ScrollText size={40} />}
          title="Audit Log"
          description="Audit trail coming soon — all secret access events will be tracked here."
        />
      </div>
    </div>
  )
}
