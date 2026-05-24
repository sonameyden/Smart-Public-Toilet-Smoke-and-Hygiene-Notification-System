import apiClient from '../../../lib/api-client'

export async function fetchAlerts({ status, type, severity } = {}) {
  const params = new URLSearchParams()
  if (status)   params.set('status', status)
  if (type)     params.set('type', type)
  if (severity) params.set('severity', severity)
  const { data } = await apiClient.get(`/alerts?${params}`)
  return data
}

export async function resolveAlert(id) {
  const { data } = await apiClient.patch(`/alerts/${id}/resolve`)
  return data
}
