import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useEffect } from 'react'
import { fetchActiveAlerts } from '../api/dashboard.api'
import { subscribeWS } from '../../../lib/ws-client'

export function useActiveAlerts() {
  const qc = useQueryClient()

  useEffect(() => {
    const unsub = subscribeWS((msg) => {
      if (msg.type === 'new_alert' || msg.type === 'alert_resolved') {
        qc.invalidateQueries({ queryKey: ['alerts', 'active'] })
      }
    })
    return unsub
  }, [qc])

  return useQuery({
    queryKey: ['alerts', 'active'],
    queryFn: fetchActiveAlerts,
    refetchInterval: 10000,
  })
}
