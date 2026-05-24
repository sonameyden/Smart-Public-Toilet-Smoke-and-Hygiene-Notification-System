import { useQuery } from '@tanstack/react-query'
import { fetchRecentActivity } from '../api/dashboard.api'

export function useRecentActivity() {
  return useQuery({
    queryKey: ['activity-logs'],
    queryFn: fetchRecentActivity,
    refetchInterval: 30000,
  })
}
