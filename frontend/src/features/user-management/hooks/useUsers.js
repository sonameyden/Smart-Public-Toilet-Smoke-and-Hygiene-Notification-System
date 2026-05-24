import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { fetchUsers, createUser, updateUser, deleteUser } from '../api/users.api'

export function useUsers() {
  return useQuery({ queryKey: ['users'], queryFn: fetchUsers })
}

export function useCreateUser() {
  const qc = useQueryClient()
  return useMutation({ mutationFn: createUser, onSuccess: () => qc.invalidateQueries({ queryKey: ['users'] }) })
}

export function useUpdateUser() {
  const qc = useQueryClient()
  return useMutation({ mutationFn: ({ id, ...p }) => updateUser(id, p), onSuccess: () => qc.invalidateQueries({ queryKey: ['users'] }) })
}

export function useDeleteUser() {
  const qc = useQueryClient()
  return useMutation({ mutationFn: deleteUser, onSuccess: () => qc.invalidateQueries({ queryKey: ['users'] }) })
}
