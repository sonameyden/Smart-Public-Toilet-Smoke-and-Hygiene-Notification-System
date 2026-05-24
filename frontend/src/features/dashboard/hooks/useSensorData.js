import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useEffect, useRef } from 'react'
import { fetchLatestSensors } from '../api/dashboard.api'
import { connectWS, subscribeWS } from '../../../lib/ws-client'
import { useAuthStore } from '../../../store/auth-store'

// Matches firmware READ_INTERVAL — used as the WS-coalesce window and fallback poll
const SENSOR_INTERVAL_MS = 3000

export function useSensorData() {
  const { token } = useAuthStore()
  const qc = useQueryClient()

  // Buffer incoming WS sensor updates and apply them together after a short
  // debounce window. This prevents 4 rapid partial renders per firmware cycle
  // (one broadcast per MQTT topic: smoke → gas → air_quality → env).
  const pendingRef = useRef(null)
  const timerRef   = useRef(null)

  useEffect(() => {
    if (!token) return

    connectWS(token)

    const unsub = subscribeWS((msg) => {
      if (msg.type === 'sensor_update') {
        // Merge into pending buffer
        pendingRef.current = { ...(pendingRef.current ?? {}), ...msg.data }

        // Debounce: flush the buffer 200 ms after the last incoming message
        // so all 4 topic updates are applied in one React render
        clearTimeout(timerRef.current)
        timerRef.current = setTimeout(() => {
          const snapshot = pendingRef.current
          pendingRef.current = null
          if (!snapshot) return

          qc.setQueryData(['sensors', 'latest'], (prev) => {
            // If the HTTP fetch hasn't finished yet, prev may be undefined.
            // In that case fall back to the full WS snapshot so cards still render.
            if (!prev) return snapshot
            return { ...prev, ...snapshot }
          })
        }, 200)
      }

      if (msg.type === 'new_alert') {
        qc.invalidateQueries({ queryKey: ['alerts'] })
        qc.invalidateQueries({ queryKey: ['analytics'] })
        qc.invalidateQueries({ queryKey: ['activity-logs'] })
      }

      if (msg.type === 'alert_resolved') {
        qc.invalidateQueries({ queryKey: ['alerts'] })
        qc.invalidateQueries({ queryKey: ['analytics'] })
        qc.invalidateQueries({ queryKey: ['activity-logs'] })
      }
    })

    return () => {
      unsub()
      clearTimeout(timerRef.current)
    }
  }, [token, qc])

  return useQuery({
    queryKey: ['sensors', 'latest'],
    queryFn: fetchLatestSensors,
    // Fallback poll every 3 s (= firmware read interval).
    // WebSocket updates arrive faster, but this guarantees cards refresh
    // even if the WS connection drops or is slow to establish.
    refetchInterval: SENSOR_INTERVAL_MS,
    // Keep previous data visible while a background refetch is running so
    // cards never flash blank between updates.
    placeholderData: (prev) => prev,
  })
}