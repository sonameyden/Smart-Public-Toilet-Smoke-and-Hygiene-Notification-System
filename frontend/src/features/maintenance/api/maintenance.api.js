import apiClient from '../../../lib/api-client'

export async function fetchMaintenanceLogs() {
  const { data } = await apiClient.get('/maintenance/logs')
  return data
}

export async function createMaintenanceLog(payload) {
  const { data } = await apiClient.post('/maintenance/logs', payload)
  return data
}

export async function updateMaintenanceLog(id, payload) {
  const { data } = await apiClient.patch(`/maintenance/logs/${id}`, payload)
  return data
}
