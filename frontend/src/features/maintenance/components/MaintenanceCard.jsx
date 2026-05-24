import { Wrench, User, Calendar, CheckCircle2 } from 'lucide-react'
import Badge from '../../../components/ui/Badge'
import Button from '../../../components/ui/Button'
import { formatDate } from '../../../lib/utils'

export default function MaintenanceCard({ log, onComplete, canUpdate }) {
  const typeLabel = log.type === 'preventive' ? 'Preventive Maintenance' : 'Corrective Maintenance'
  const typeColor = log.type === 'preventive' ? '#06B6D4' : '#F59E0B'

  return (
    <div className="sg-card sg-border border rounded-xl p-5 space-y-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-semibold sg-text">{typeLabel}</p>
          <p className="text-xs sg-muted">IT Building Ground Floor Toilet</p>
        </div>
        <Badge variant={log.status}>{log.status.replace('_', ' ')}</Badge>
      </div>

      <p className="text-sm sg-muted">{log.description}</p>

      <div className="space-y-1.5">
        {log.assigned_to_name && (
          <div className="flex items-center gap-2 text-xs sg-muted">
            <User size={12} />
            <span>Assigned to: {log.assigned_to_name}</span>
          </div>
        )}
        {log.notes && (
          <div className="flex items-center gap-2 text-xs sg-muted">
            <Wrench size={12} />
            <span>{log.notes}</span>
          </div>
        )}
        <div className="flex items-center gap-2 text-xs sg-muted">
          <Calendar size={12} />
          <span>{formatDate(log.created_at)}</span>
        </div>
      </div>

      {canUpdate && log.status === 'in_progress' && (
        <div className="flex justify-end pt-1">
          <Button variant="resolve" size="sm" onClick={() => onComplete(log.id)}>
            <CheckCircle2 size={12} />
            Mark Complete
          </Button>
        </div>
      )}
    </div>
  )
}
