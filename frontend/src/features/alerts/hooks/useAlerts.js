import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { fetchAlerts, resolveAlert } from '../api/alerts.api'

export function useAlerts(filters = {}) {
  return useQuery({
    queryKey: ['alerts', filters],
    queryFn: () => fetchAlerts(filters),
    refetchInterval: 15000,
  })
}

export function useResolveAlert() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: resolveAlert,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['alerts'] })
      qc.invalidateQueries({ queryKey: ['analytics'] })
    },
  })
}
