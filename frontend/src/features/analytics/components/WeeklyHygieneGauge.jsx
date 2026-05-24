export default function WeeklyHygieneGauge({ score = 87, max = 100 }) {
  const radius = 54
  const stroke = 8
  const circumference = 2 * Math.PI * radius
  const progress = (score / max) * circumference
  const gap = circumference - progress

  const color = score >= 80 ? '#22C55E' : score >= 60 ? '#F59E0B' : '#EF4444'

  return (
    <div className="flex flex-col items-center justify-center py-4">
      <div className="relative flex items-center justify-center" style={{ width: 140, height: 140 }}>
        <svg width="140" height="140" viewBox="0 0 140 140" className="-rotate-90">
          {/* Background track */}
          <circle
            cx="70" cy="70" r={radius}
            fill="none"
            stroke="#1E2D3D"
            strokeWidth={stroke}
          />
          {/* Progress arc */}
          <circle
            cx="70" cy="70" r={radius}
            fill="none"
            stroke={color}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={`${progress} ${gap}`}
            style={{ transition: 'stroke-dasharray 0.6s ease' }}
          />
        </svg>
        <div className="absolute flex flex-col items-center">
          <span className="text-3xl font-bold sg-text">{score}</span>
          <span className="text-xs sg-muted">out of {max}</span>
        </div>
      </div>
      <p className="text-xs sg-muted mt-2">Weekly Average Score</p>
    </div>
  )
}
