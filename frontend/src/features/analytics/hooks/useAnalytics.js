import { useQuery } from '@tanstack/react-query'
import {
  fetchAnalyticsSummary,
  fetchAnalyticsTrends,
  fetchHygieneScore,
  fetchAlertDistribution,
} from '../api/analytics.api'

export function useAnalyticsSummary() {
  const query = useQuery({
    queryKey: ['analytics', 'summary'],
    queryFn: fetchAnalyticsSummary,
    staleTime: 60_000,
  })

  const normalized = query.data
    ? {
        total: query.data.total_alerts,
        active: query.data.active_alerts,
        resolved: query.data.resolved_alerts,
        critical: query.data.critical_alerts,
      }
    : undefined

  return { ...query, data: normalized }
}

export function useAnalyticsTrends() {
  return useQuery({ queryKey: ['analytics', 'trends'], queryFn: fetchAnalyticsTrends, staleTime: 5 * 60_000 })
}

export function useHygieneScore() {
  return useQuery({ queryKey: ['analytics', 'hygiene-score'], queryFn: fetchHygieneScore, staleTime: 5 * 60_000 })
}

export function useAlertDistribution() {
  return useQuery({ queryKey: ['analytics', 'distribution'], queryFn: fetchAlertDistribution, staleTime: 5 * 60_000 })
}
