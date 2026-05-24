import { Download } from 'lucide-react'
import Topbar from '../../../components/layout/Topbar'
import StatSummaryCards from '../components/StatSummaryCards'
import AirQualityTrendChart from '../components/AirQualityTrendChart'
import AlertDistributionBar from '../components/AlertDistributionBar'
import WeeklyHygieneGauge from '../components/WeeklyHygieneGauge'
import { useAnalyticsSummary, useHygieneScore, useAlertDistribution } from '../hooks/useAnalytics'
import Button from '../../../components/ui/Button'

export default function AnalyticsPage() {
  const { data: summary } = useAnalyticsSummary()
  const { data: hygieneData } = useHygieneScore()
  const { data: distribution } = useAlertDistribution()

  const distributionData = distribution
    ? [
        { label: 'Smoke Alerts',   pct: distribution.smoke,       color: '#EF4444' },
        { label: 'Hygiene Alerts', pct: distribution.hygiene,     color: '#F59E0B' },
        { label: 'Maintenance',    pct: distribution.maintenance, color: '#06B6D4' },
        { label: 'System',         pct: distribution.system,      color: '#94A3B8' },
      ]
    : undefined

  return (
    <div className="flex flex-col h-full">
      <Topbar title="Analytics" />

      <div className="flex-1 overflow-y-auto p-6 space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold sg-text">Analytics Dashboard</h2>
            <p className="text-xs sg-muted mt-0.5">System performance and insights</p>
          </div>
          <Button variant="secondary" size="md">
            <Download size={14} />
            Export Report
          </Button>
        </div>

        {/* Summary stat cards */}
        <StatSummaryCards summary={summary} />

        {/* Charts row */}
        <div className="grid grid-cols-2 gap-5">
          <div className="sg-card sg-border border rounded-xl p-4">
            <h3 className="text-sm font-semibold sg-text mb-4">Air Quality Trend</h3>
            <AirQualityTrendChart />
          </div>

          <div className="sg-card sg-border border rounded-xl p-4">
            <h3 className="text-sm font-semibold sg-text mb-4">Alert Distribution</h3>
            <AlertDistributionBar />
          </div>
        </div>

        {/* Hygiene gauge */}
        <div className="sg-card sg-border border rounded-xl p-4">
          <h3 className="text-sm font-semibold sg-text mb-2">Weekly Hygiene Score</h3>
          <WeeklyHygieneGauge score={hygieneData?.score ?? 87} />
        </div>
      </div>
    </div>
  )
}
