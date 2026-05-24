import { Shield, Wrench, Eye } from 'lucide-react'

const ROLES = [
  { id: 'admin',       label: 'Admin',       icon: Shield, color: '#06B6D4' },
  { id: 'maintenance', label: 'Maintenance', icon: Wrench, color: '#F59E0B' },
  { id: 'viewer',      label: 'Viewer',      icon: Eye,    color: '#94A3B8' },
]

export default function DemoLoginPanel({ onDemo, loading }) {
  return (
    <div className="space-y-3">
      <p className="text-xs text-center sg-muted">Quick Login as Demo User</p>
      <div className="grid grid-cols-3 gap-2">
        {ROLES.map(({ id, label, icon: Icon, color }) => (
          <button
            key={id}
            onClick={() => onDemo(id)}
            disabled={loading}
            className="flex flex-col items-center gap-1.5 rounded-lg py-2.5 text-xs font-medium transition-all"
            style={{
              background: `${color}18`,
              border: `1px solid ${color}40`,
              color,
            }}
          >
            <Icon size={16} />
            {label}
          </button>
        ))}
      </div>
    </div>
  )
}
