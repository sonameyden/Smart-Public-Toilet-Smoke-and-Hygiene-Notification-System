import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

const trendIcon = {
  up:     <TrendingUp   size={12} className="text-red-400" />,
  down:   <TrendingDown size={12} className="text-green-400" />,
  normal: <Minus        size={12} className="text-green-400" />,
}

const trendLabel = {
  up:     '↑ elevated',
  down:   '↓ normal',
  normal: '→ normal',
}

export default function SensorCard({ icon: Icon, label, value, unit, trend = 'normal', color = '#06B6D4' }) {
  return (
    <div className="sg-card sg-border border rounded-xl p-4 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div
          className="flex h-8 w-8 items-center justify-center rounded-lg"
          style={{ backgroundColor: `${color}20` }}
        >
          <Icon size={16} style={{ color }} />
        </div>
        <div className="flex items-center gap-1 text-xs sg-muted">
          {trendIcon[trend]}
          <span>{trendLabel[trend]}</span>
        </div>
      </div>
      <div>
        <p className="text-xs sg-muted mb-1">{label}</p>
        <div className="flex items-baseline gap-1">
          <span className="text-2xl font-bold sg-text">{value}</span>
          <span className="text-sm sg-muted">{unit}</span>
        </div>
      </div>
    </div>
  )
}
