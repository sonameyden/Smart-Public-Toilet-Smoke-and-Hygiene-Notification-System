export default function AlertThresholds({ settings, onChange }) {
  const fields = [
    { key: 'smoke_threshold',       label: 'smokeThreshold',       sub: 'Maximum smoke level before triggering alert' },
    { key: 'gas_threshold',         label: 'gasThreshold',         sub: 'Maximum gas level before triggering alert' },
    { key: 'air_quality_threshold', label: 'airQualityThreshold',  sub: 'Minimum air quality score' },
  ]

  return (
    <div className="sg-card sg-border border rounded-xl p-5 space-y-1">
      <h3 className="text-sm font-semibold sg-text mb-4">Alert Settings</h3>
      {fields.map(({ key, label, sub }) => (
        <div key={key} className="flex items-center justify-between py-3 sg-border border-b last:border-0">
          <div>
            <p className="text-sm font-medium sg-text">{label}</p>
            <p className="text-xs sg-muted">{sub}</p>
          </div>
          <input
            type="number"
            value={settings?.[key] ?? ''}
            onChange={(e) => onChange({ ...settings, [key]: Number(e.target.value) })}
            className="w-20 rounded-lg px-3 py-1.5 text-sm text-center sg-input"
          />
        </div>
      ))}
    </div>
  )
}
