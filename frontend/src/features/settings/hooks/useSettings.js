import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { fetchSettings, updateSettings } from '../api/settings.api'

export function useSettings() {
  return useQuery({ queryKey: ['settings'], queryFn: fetchSettings })
}

export function useUpdateSettings() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: updateSettings,
    onSuccess: (data) => {
      qc.setQueryData(['settings'], data)
    },
  })
}
