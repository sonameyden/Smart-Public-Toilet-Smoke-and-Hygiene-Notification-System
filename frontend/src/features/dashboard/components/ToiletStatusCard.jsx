import { RefreshCw } from 'lucide-react'
import { formatDate } from '../../../lib/utils'

export default function ToiletStatusCard({ lastUpdated, status = 'operational' }) {
  const statusColor = status === 'operational' ? '#22C55E' : '#EF4444'

  return (
    <div className="rounded-xl p-5 sg-card sg-border border">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-lg font-bold sg-text">IT Building Ground Floor Toilet</h2>
          <p className="text-sm sg-muted mt-0.5">IT Building, Ground Floor</p>
          <div className="flex items-center gap-1.5 mt-3 text-xs sg-muted">
            <RefreshCw size={12} />
            <span>Last updated: {formatDate(lastUpdated)}</span>
          </div>
        </div>
        <span
          className="rounded-full px-3 py-1 text-xs font-semibold capitalize"
          style={{ background: `${statusColor}20`, color: statusColor, border: `1px solid ${statusColor}40` }}
        >
          {status}
        </span>
      </div>
    </div>
  )
}