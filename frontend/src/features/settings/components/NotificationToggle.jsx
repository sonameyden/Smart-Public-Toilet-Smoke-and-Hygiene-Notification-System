import Toggle from '../../../components/ui/Toggle'

export default function NotificationToggle({ settings, onChange }) {
  return (
    <div className="sg-card sg-border border rounded-xl p-5">
      <h3 className="text-sm font-semibold sg-text mb-4">Notifications</h3>
      <div className="flex items-center justify-between py-2">
        <div>
          <p className="text-sm font-medium sg-text">alertNotifications</p>
          <p className="text-xs sg-muted">Enable email notifications for alerts</p>
        </div>
        <Toggle
          checked={settings?.alert_notifications ?? true}
          onChange={(val) => onChange({ ...settings, alert_notifications: val })}
        />
      </div>
    </div>
  )
}
