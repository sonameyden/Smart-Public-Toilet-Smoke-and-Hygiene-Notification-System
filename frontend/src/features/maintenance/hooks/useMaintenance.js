import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  fetchMaintenanceLogs,
  createMaintenanceLog,
  updateMaintenanceLog,
} from '../api/maintenance.api'

export function useMaintenance() {
  return useQuery({
    queryKey: ['maintenance', 'logs'],
    queryFn: fetchMaintenanceLogs,
  })
}

export function useCreateMaintenance() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: createMaintenanceLog,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['maintenance'] }),
  })
}

export function useUpdateMaintenance() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, ...payload }) => updateMaintenanceLog(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['maintenance'] }),
  })
}
