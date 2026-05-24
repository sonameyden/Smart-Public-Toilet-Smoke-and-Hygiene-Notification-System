import Topbar from '../../../components/layout/Topbar'
import ToiletStatusCard from '../components/ToiletStatusCard'
import SensorGrid from '../components/SensorGrid'
import ActiveAlertsList from '../components/ActiveAlertsList'
import RecentActivityFeed from '../components/RecentActivityFeed'
import { useSensorData } from '../hooks/useSensorData'
import { useActiveAlerts } from '../hooks/useActiveAlerts'

export default function DashboardPage() {
  const { data: sensors, isLoading: sensorsLoading } = useSensorData()
  const { data: alerts,  isLoading: alertsLoading  } = useActiveAlerts()

  const activeCount = Array.isArray(alerts) ? alerts.filter((a) => a.status === 'active').length : 0

  return (
    <div className="flex flex-col h-full">
      <Topbar title="Dashboard" />

      <div className="flex-1 overflow-y-auto p-6 space-y-5">
        {/* Status header card */}
        <ToiletStatusCard lastUpdated={sensors?.recorded_at} status="operational" />

        {/* 5-column sensor grid */}
        <SensorGrid data={sensors} />

        {/* Alerts + Activity split */}
        <div className="grid grid-cols-2 gap-5">
          {/* Active Alerts */}
          <div className="sg-card sg-border border rounded-xl p-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold sg-text">Active Alerts</h3>
              {activeCount > 0 && (
                <span className="rounded-full bg-red-500/20 text-red-400 border border-red-500/30 px-2 py-0.5 text-xs font-semibold">
                  {activeCount} active
                </span>
              )}
            </div>
            <ActiveAlertsList
              alerts={Array.isArray(alerts) ? alerts : []}
              loading={alertsLoading}
            />
          </div>

          {/* Recent Activity */}
          <div className="sg-card sg-border border rounded-xl p-4">
            <h3 className="text-sm font-semibold sg-text mb-4">Recent Activity</h3>
            <RecentActivityFeed />
          </div>
        </div>
      </div>
    </div>
  )
}
