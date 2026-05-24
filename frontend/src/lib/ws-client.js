import { useAuthStore } from '../store/auth-store'

let ws = null
const listeners = new Set()
let reconnectTimer = null

export function connectWS() {
  if (ws && ws.readyState === WebSocket.OPEN) return

  const token = useAuthStore.getState().token
  const url = `${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/api/v1/ws/dashboard`

  ws = new WebSocket(url)

  // Send the JWT as the very first text message (backend requires this)
  ws.onopen = () => {
    try {
      if (token) ws.send(token)
    } catch {}
  }

  ws.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data)
      listeners.forEach((cb) => cb(data))
    } catch {}
  }

  ws.onclose = () => {
    reconnectTimer = setTimeout(connectWS, 3000)
  }

  ws.onerror = () => ws.close()
}

export function disconnectWS() {
  clearTimeout(reconnectTimer)
  ws?.close()
  ws = null
}

export function subscribeWS(callback) {
  listeners.add(callback)
  return () => listeners.delete(callback)
}
