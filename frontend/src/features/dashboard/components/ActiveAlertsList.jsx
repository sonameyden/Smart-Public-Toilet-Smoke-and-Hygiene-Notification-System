import { AlertTriangle, CheckCircle2, Clock } from 'lucide-react'
import Badge from '../../../components/ui/Badge'
import Button from '../../../components/ui/Button'
import { formatDate } from '../../../lib/utils'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import apiClient from '../../../lib/api-client'
import { useAuthStore } from '../../../store/auth-store'

function resolveAlert(id) {
  return apiClient.patch(`/alerts/${id}/resolve`).then((r) => r.data)
}

export default function ActiveAlertsList({ alerts = [], loading }) {
  const { role } = useAuthStore()
  const qc = useQueryClient()
  const canResolve = ['admin', 'maintenance'].includes(role)

  const { mutate } = useMutation({
    mutationFn: resolveAlert,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['alerts'] })
    },
  })

  if (loading) return <div className="text-xs sg-muted p-2">Loading alerts…</div>

  const recentAlerts = [...alerts]
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    .slice(0, 3)

  return (
    <div className="space-y-3">
      {recentAlerts.length === 0 && (
        <div className="flex flex-col items-center py-6 sg-muted text-sm gap-2">
          <CheckCircle2 size={24} className="text-green-400" />
          <span>No active alerts</span>
        </div>
      )}
      {recentAlerts.map((alert) => (
        <div key={alert.id} className="sg-border border rounded-xl p-4 space-y-2">
          <div className="flex items-start justify-between gap-2">
            <div className="flex items-center gap-2">
              <AlertTriangle size={15} className="text-amber-400 shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold sg-text">{alert.title}</p>
                <p className="text-xs sg-muted">IT Building Ground Floor Toilet</p>
              </div>
            </div>
            <div className="flex items-center gap-1.5 shrink-0">
              <Badge variant={alert.severity}>{alert.severity}</Badge>
              <Badge variant={alert.status}>{alert.status}</Badge>
            </div>
          </div>
          <p className="text-xs sg-muted pl-5">{alert.description}</p>
          <div className="flex items-center justify-between pl-5">
            <div className="flex items-center gap-1 text-xs sg-muted">
              <Clock size={11} />
              <span>{formatDate(alert.created_at)}</span>
            </div>
            {canResolve && alert.status === 'active' && (
              <Button variant="resolve" size="sm" onClick={() => mutate(alert.id)}>
                <CheckCircle2 size={12} />
                Resolve
              </Button>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}
