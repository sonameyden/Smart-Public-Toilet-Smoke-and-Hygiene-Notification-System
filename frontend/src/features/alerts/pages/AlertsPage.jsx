import { useState } from 'react'
import Topbar from '../../../components/layout/Topbar'
import AlertCard from '../components/AlertCard'
import AlertFilters from '../components/AlertFilters'
import { useAlerts, useResolveAlert } from '../hooks/useAlerts'
import { useAuthStore } from '../../../store/auth-store'

// Mock data for when API isn't connected
const MOCK_ALERTS = [
  {
    id: '1', title: 'Smoke Level Elevated', severity: 'high', status: 'active',
    description: 'Smoke sensor detected elevated levels in the toilet area',
    created_at: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
  },
  {
    id: '2', title: 'Cleaning Required', severity: 'medium', status: 'active',
    description: 'Toilet hygiene score dropped below threshold',
    created_at: new Date(Date.now() - 90 * 60 * 1000).toISOString(),
  },
  {
    id: '3', title: 'System Update Available', severity: 'low', status: 'resolved',
    description: 'Firmware update available for sensor modules',
    created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
  },
]

export default function AlertsPage() {
  const [filters, setFilters] = useState({})
  const { role } = useAuthStore()
  const canResolve = ['admin', 'maintenance'].includes(role)

  const { data, isLoading } = useAlerts(filters)
  const { mutate: resolve } = useResolveAlert()

  const alerts = data ?? MOCK_ALERTS
  const activeCount   = alerts.filter((a) => a.status === 'active').length

  return (
    <div className="flex flex-col h-full">
      <Topbar title="Alerts" />

      <div className="flex-1 overflow-y-auto p-6 space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold sg-text">All Alerts</h2>
          </div>
          <span className="text-xs sg-muted">
            {activeCount} active / {alerts.length} total
          </span>
        </div>

        <AlertFilters filters={filters} onChange={setFilters} />

        <div className="space-y-3">
          {isLoading ? (
            <p className="text-sm sg-muted">Loading…</p>
          ) : alerts.length === 0 ? (
            <p className="text-sm sg-muted text-center py-10">No alerts found.</p>
          ) : (
            alerts.map((alert) => (
              <AlertCard
                key={alert.id}
                alert={alert}
                canResolve={canResolve}
                onResolve={resolve}
              />
            ))
          )}
        </div>
      </div>
    </div>
  )
}
