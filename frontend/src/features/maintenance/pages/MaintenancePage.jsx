import { useState } from 'react'
import { Plus } from 'lucide-react'
import Topbar from '../../../components/layout/Topbar'
import MaintenanceCard from '../components/MaintenanceCard'
import NewRequestModal from '../components/NewRequestModal'
import { useMaintenance, useCreateMaintenance, useUpdateMaintenance } from '../hooks/useMaintenance'
import { useAuthStore } from '../../../store/auth-store'
import Button from '../../../components/ui/Button'

const MOCK_LOGS = [
  {
    id: '1', type: 'preventive', status: 'completed',
    description: 'Monthly sensor calibration and cleaning',
    assigned_to_name: 'John Smith',
    notes: 'All sensors calibrated successfully',
    created_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: '2', type: 'corrective', status: 'in_progress',
    description: 'Replace air quality sensor module',
    assigned_to_name: 'Mike Johnson',
    notes: 'Waiting for replacement parts',
    created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
  },
]

export default function MaintenancePage() {
  const [showModal, setShowModal] = useState(false)
  const { role } = useAuthStore()
  const canCreate = ['admin', 'maintenance'].includes(role)
  const canUpdate = ['admin', 'maintenance'].includes(role)

  const { data, isLoading } = useMaintenance()
  const { mutate: create, isPending: creating } = useCreateMaintenance()
  const { mutate: update } = useUpdateMaintenance()

  const logs = data ?? MOCK_LOGS
  const pendingCount = logs.filter((l) => l.status === 'pending' || l.status === 'in_progress').length

  const handleCreate = (payload) => {
    create(payload, { onSuccess: () => setShowModal(false) })
  }

  const handleComplete = (id) => {
    update({ id, status: 'completed' })
  }

  return (
    <div className="flex flex-col h-full">
      <Topbar title="Maintenance" />

      <div className="flex-1 overflow-y-auto p-6 space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold sg-text">Maintenance Records</h2>
            {pendingCount > 0 && (
              <p className="text-xs sg-muted mt-0.5">{pendingCount} pending task{pendingCount > 1 ? 's' : ''}</p>
            )}
          </div>
          {canCreate && (
            <Button variant="primary" size="md" onClick={() => setShowModal(true)}>
              <Plus size={14} />
              New Request
            </Button>
          )}
        </div>

        {isLoading ? (
          <p className="text-sm sg-muted">Loading…</p>
        ) : (
          <div className="grid grid-cols-2 gap-4">
            {logs.map((log) => (
              <MaintenanceCard
                key={log.id}
                log={log}
                onComplete={handleComplete}
                canUpdate={canUpdate}
              />
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <NewRequestModal
          onClose={() => setShowModal(false)}
          onSubmit={handleCreate}
          loading={creating}
        />
      )}
    </div>
  )
}
