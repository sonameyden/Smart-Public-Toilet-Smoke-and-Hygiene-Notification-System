import apiClient from '../../../lib/api-client'

export async function fetchUsers() {
  const { data } = await apiClient.get('/users')
  return data
}

export async function createUser(payload) {
  const { data } = await apiClient.post('/users', payload)
  return data
}

export async function updateUser(id, payload) {
  const { data } = await apiClient.patch(`/users/${id}`, payload)
  return data
}

export async function deleteUser(id) {
  await apiClient.delete(`/users/${id}`)
}
