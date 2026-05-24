export default function SystemSettings({ settings, onChange }) {
  return (
    <div className="sg-card sg-border border rounded-xl p-5">
      <h3 className="text-sm font-semibold sg-text mb-4">System Settings</h3>
      <div className="flex items-center justify-between py-2">
        <div>
          <p className="text-sm font-medium sg-text">autoResolveTime</p>
          <p className="text-xs sg-muted">Hours before auto-resolving low priority alerts</p>
        </div>
        <input
          type="number"
          value={settings?.auto_resolve_hours ?? 24}
          onChange={(e) => onChange({ ...settings, auto_resolve_hours: Number(e.target.value) })}
          className="w-20 rounded-lg px-3 py-1.5 text-sm text-center sg-input"
        />
      </div>
    </div>
  )
}
