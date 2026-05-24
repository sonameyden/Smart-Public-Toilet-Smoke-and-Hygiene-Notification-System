import apiClient from '../../../lib/api-client'

export async function fetchSettings() {
  const { data } = await apiClient.get('/settings')
  return data
}

export async function updateSettings(payload) {
  const { data } = await apiClient.patch('/settings', payload)
  return data
}
