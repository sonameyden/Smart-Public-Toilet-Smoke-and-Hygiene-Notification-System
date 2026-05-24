import { useState, useEffect } from 'react'
import { Save } from 'lucide-react'
import Topbar from '../../../components/layout/Topbar'
import AlertThresholds from '../components/AlertThresholds'
import NotificationToggle from '../components/NotificationToggle'
import SystemSettings from '../components/SystemSettings'
import { useSettings, useUpdateSettings } from '../hooks/useSettings'
import Button from '../../../components/ui/Button'

const DEFAULTS = {
  smoke_threshold: 200,
  gas_threshold: 100,
  air_quality_threshold: 70,
  alert_notifications: true,
  auto_resolve_hours: 24,
}

export default function SettingsPage() {
  const { data, isLoading } = useSettings()
  const { mutate: save, isPending } = useUpdateSettings()

  const [local, setLocal] = useState(DEFAULTS)

  useEffect(() => {
    if (data) setLocal(data)
  }, [data])

  const settings = data ?? DEFAULTS

  return (
    <div className="flex flex-col h-full">
      <Topbar title="Settings" />

      <div className="flex-1 overflow-y-auto p-6 space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold sg-text">System Settings</h2>
            <p className="text-xs sg-muted mt-0.5">Configure system parameters and preferences</p>
          </div>
          <Button
            variant="primary"
            size="md"
            onClick={() => save(local)}
            disabled={isPending}
          >
            <Save size={14} />
            {isPending ? 'Saving…' : 'Save Changes'}
          </Button>
        </div>

        {isLoading ? (
          <p className="text-sm sg-muted">Loading…</p>
        ) : (
          <>
            <AlertThresholds settings={local} onChange={setLocal} />
            <NotificationToggle settings={local} onChange={setLocal} />
            <SystemSettings settings={local} onChange={setLocal} />
          </>
        )}
      </div>
    </div>
  )
}
