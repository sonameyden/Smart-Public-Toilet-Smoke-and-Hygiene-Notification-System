import apiClient from '../../../lib/api-client'

export async function fetchAnalyticsSummary() {
  const { data } = await apiClient.get('/analytics/summary')
  return data
}

export async function fetchAnalyticsTrends() {
  const { data } = await apiClient.get('/analytics/trends')
  return data
}

export async function fetchHygieneScore() {
  const { data } = await apiClient.get('/analytics/hygiene-score')
  return data
}

export async function fetchAlertDistribution() {
  const { data } = await apiClient.get('/analytics/distribution')
  return data
}
