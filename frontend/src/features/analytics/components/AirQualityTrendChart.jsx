import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const MOCK_DATA = [
  { day: 'Mon', score: 88 },
  { day: 'Tue', score: 92 },
  { day: 'Wed', score: 75 },
  { day: 'Thu', score: 85 },
  { day: 'Fri', score: 90 },
  { day: 'Sat', score: 95 },
  { day: 'Sun', score: 87 },
]

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="sg-card sg-border border rounded-lg px-3 py-2 text-xs">
      <p className="sg-muted mb-1">{label}</p>
      <p className="text-cyan-400 font-semibold">{payload[0].value}%</p>
    </div>
  )
}

export default function AirQualityTrendChart({ data = MOCK_DATA }) {
  return (
    <div className="h-48">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 4, right: 8, bottom: 0, left: -20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1E2D3D" />
          <XAxis
            dataKey="day"
            tick={{ fill: '#94A3B8', fontSize: 11 }}
            axisLine={{ stroke: '#1E2D3D' }}
            tickLine={false}
          />
          <YAxis
            domain={[60, 100]}
            tick={{ fill: '#94A3B8', fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ stroke: '#1E2D3D' }} />
          <Line
            type="monotone"
            dataKey="score"
            stroke="#06B6D4"
            strokeWidth={2}
            dot={{ fill: '#06B6D4', r: 3 }}
            activeDot={{ r: 5, fill: '#06B6D4' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
