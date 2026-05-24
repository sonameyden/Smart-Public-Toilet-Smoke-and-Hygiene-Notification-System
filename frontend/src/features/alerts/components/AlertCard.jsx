import { AlertTriangle, Clock, CheckCircle2 } from 'lucide-react'
import Badge from '../../../components/ui/Badge'
import Button from '../../../components/ui/Button'
import { formatDate } from '../../../lib/utils'

export default function AlertCard({ alert, onResolve, canResolve }) {
  return (
    <div className="sg-card sg-border border rounded-xl p-4 space-y-3">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 min-w-0">
          <div className="h-8 w-8 rounded-lg bg-amber-500/10 flex items-center justify-center shrink-0 mt-0.5">
            <AlertTriangle size={15} className="text-amber-400" />
          </div>
          <div className="min-w-0">
            <p className="text-sm font-semibold sg-text">{alert.title}</p>
            <p className="text-xs sg-muted">IT Building Ground Floor Toilet</p>
          </div>
        </div>
        <div className="flex items-center gap-1.5 shrink-0">
          <Badge variant={alert.severity}>{alert.severity}</Badge>
          <Badge variant={alert.status}>{alert.status}</Badge>
        </div>
      </div>

      <p className="text-xs sg-muted pl-11">{alert.description}</p>

      <div className="flex items-center justify-between pl-11">
        <div className="flex items-center gap-1.5 text-xs sg-muted">
          <Clock size={11} />
          <span>{formatDate(alert.created_at)}</span>
        </div>
        {canResolve && alert.status === 'active' && (
          <Button variant="resolve" size="sm" onClick={() => onResolve(alert.id)}>
            <CheckCircle2 size={12} />
            Resolve
          </Button>
        )}
      </div>
    </div>
  )
}
