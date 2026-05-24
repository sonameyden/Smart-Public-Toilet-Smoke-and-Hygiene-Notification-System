import { AlertTriangle, Activity, CheckCircle2, Zap } from 'lucide-react'

const CARDS = [
  { key: 'total',    label: 'Total Alerts',   icon: AlertTriangle, color: '#F59E0B', bg: '#F59E0B18' },
  { key: 'active',   label: 'Active Alerts',  icon: Activity,      color: '#EF4444', bg: '#EF444418' },
  { key: 'resolved', label: 'Resolved',       icon: CheckCircle2,  color: '#22C55E', bg: '#22C55E18' },
  { key: 'critical', label: 'Critical',       icon: Zap,           color: '#A855F7', bg: '#A855F718' },
]

export default function StatSummaryCards({ summary }) {
  const s = summary ?? { total: 3, active: 2, resolved: 1, critical: 0 }

  return (
    <div className="grid grid-cols-4 gap-4">
      {CARDS.map(({ key, label, icon: Icon, color, bg }) => (
        <div
          key={key}
          className="rounded-xl p-4 sg-border border"
          style={{ background: bg }}
        >
          <div className="flex items-center gap-2 mb-3">
            <Icon size={16} style={{ color }} />
          </div>
          <p className="text-2xl font-bold sg-text">{s[key] ?? 0}</p>
          <p className="text-xs sg-muted mt-1">{label}</p>
        </div>
      ))}
    </div>
  )
}
