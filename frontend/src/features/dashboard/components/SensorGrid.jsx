import { Wind, Flame, Activity, Thermometer, Droplets } from 'lucide-react'
import SensorCard from '../../../components/SensorCard'

export default function SensorGrid({ data }) {
  const s = data ?? {}
  return (
    <div className="grid grid-cols-5 gap-3">
      <SensorCard
        icon={Flame}
        label="Smoke Level"
        value={s.smoke_ppm ?? '12'}
        unit="ppm"
        trend={s.smoke_ppm > 50 ? 'up' : 'normal'}
        color="#EF4444"
      />
      <SensorCard
        icon={Wind}
        label="Gas Level"
        value={s.gas_ppm ?? '45'}
        unit="ppm"
        trend={s.gas_ppm > 100 ? 'up' : 'down'}
        color="#F59E0B"
      />
      <SensorCard
        icon={Activity}
        label="Air Quality"
        value={s.air_quality ?? '92'}
        unit="%"
        trend={s.air_quality < 70 ? 'up' : 'normal'}
        color="#06B6D4"
      />
      <SensorCard
        icon={Thermometer}
        label="Temperature"
        value={s.temperature ?? '24'}
        unit="°C"
        trend="normal"
        color="#8B5CF6"
      />
      <SensorCard
        icon={Droplets}
        label="Humidity"
        value={s.humidity ?? '58'}
        unit="%"
        trend="normal"
        color="#3B82F6"
      />
    </div>
  )
}
