import apiClient from '../../../lib/api-client'

export async function fetchLatestSensors() {
  const { data } = await apiClient.get('/sensors/latest')
  return data
}

export async function fetchActiveAlerts() {
  const { data } = await apiClient.get('/alerts?status=active')
  return data
}

export async function fetchRecentActivity() {
  const { data } = await apiClient.get('/activity-logs?limit=10')
  return data
}
