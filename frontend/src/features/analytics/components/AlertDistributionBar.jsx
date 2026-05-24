const MOCK = [
  { label: 'Smoke Alerts',   pct: 35, color: '#EF4444' },
  { label: 'Hygiene Alerts', pct: 28, color: '#F59E0B' },
  { label: 'Maintenance',    pct: 22, color: '#06B6D4' },
  { label: 'System',         pct: 15, color: '#94A3B8' },
]

export default function AlertDistributionBar({ data = MOCK }) {
  return (
    <div className="space-y-3">
      {data.map(({ label, pct, color }) => (
        <div key={label}>
          <div className="flex justify-between text-xs mb-1.5">
            <span className="sg-text">{label}</span>
            <span className="sg-muted font-medium">{pct}%</span>
          </div>
          <div className="h-2 rounded-full sg-border border overflow-hidden" style={{ background: '#1E2D3D' }}>
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{ width: `${pct}%`, background: color }}
            />
          </div>
        </div>
      ))}
    </div>
  )
}
