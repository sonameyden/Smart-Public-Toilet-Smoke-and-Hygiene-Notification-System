import { CheckCircle2, Wrench, LogIn, Settings } from 'lucide-react'
import { useRecentActivity } from '../hooks/useRecentActivity'

const ACTION_ICONS = {
  resolve:    { icon: CheckCircle2, color: '#22C55E' },
  maintenance:{ icon: Wrench,       color: '#F59E0B' },
  login:      { icon: LogIn,        color: '#06B6D4' },
  settings:   { icon: Settings,     color: '#8B5CF6' },
}

function formatTime(dateString) {
  const date = new Date(dateString)
  return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
}

export default function RecentActivityFeed() {
  const { data: activities, isLoading } = useRecentActivity()

  if (isLoading) {
    return <div className="text-xs sg-muted">Loading...</div>
  }

  const items = activities || []

  return (
    <div className="space-y-3">
      {items.map((item) => {
        const { icon: Icon, color } = ACTION_ICONS[item.type] ?? ACTION_ICONS.login
        return (
          <div key={item.id} className="flex items-start gap-3">
            <div
              className="h-7 w-7 rounded-lg flex items-center justify-center shrink-0 mt-0.5"
              style={{ background: `${color}18` }}
            >
              <Icon size={13} style={{ color }} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm sg-text truncate">{item.action}</p>
              <p className="text-xs sg-muted">{item.username} · {item.role}</p>
            </div>
            <span className="text-xs sg-muted shrink-0">{formatTime(item.created_at)}</span>
          </div>
        )
      })}
      {items.length === 0 && (
        <div className="text-xs sg-muted text-center py-4">No recent activity</div>
      )}
    </div>
  )
}
