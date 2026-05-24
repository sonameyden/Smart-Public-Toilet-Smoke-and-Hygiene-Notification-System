import apiClient from '../../../lib/api-client'

export async function login({ email, password }) {
  const { data } = await apiClient.post('/auth/login', { email, password })
  return data
}

export async function register(payload) {
  const { data } = await apiClient.post('/auth/register', payload)
  return data
}

export async function demoLogin(role) {
  const { data } = await apiClient.post('/auth/demo-login', { role })
  return data
}
