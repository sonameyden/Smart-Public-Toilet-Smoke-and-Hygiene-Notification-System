import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../../store/auth-store'
import { login, register, demoLogin } from '../api/auth.api'

export function useAuth() {
  const { setAuth } = useAuthStore()
  const navigate    = useNavigate()

  const handleSuccess = (data) => {
    // Support two response shapes:
    // - { access_token, role, user_id, full_name } (backend)
    // - { access_token, user: { ... } } (possible alternative)
    const userFromBody = data.user
    const user = userFromBody ?? {
      id: data.user_id ?? null,
      full_name: data.full_name ?? null,
      role: data.role ?? null,
    }

    const token = data.access_token ?? data.token ?? null
    const role = user?.role ?? data.role ?? null

    setAuth({ user, token, role })
    navigate('/app/dashboard')
  }

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: handleSuccess,
  })

  const registerMutation = useMutation({
    mutationFn: register,
    onSuccess: handleSuccess,
  })

  const demoLoginMutation = useMutation({
    mutationFn: demoLogin,
    onSuccess: handleSuccess,
  })

  return { loginMutation, registerMutation, demoLoginMutation }
}
