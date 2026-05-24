import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAuthStore = create(
  persist(
    (set) => ({
      user:  null,
      token: null,
      role:  null,
      theme: 'dark',

      setAuth: ({ user, token, role }) =>
        set({ user, token, role }),

      clearAuth: () =>
        set({ user: null, token: null, role: null }),

      toggleTheme: () =>
        set((s) => ({ theme: s.theme === 'dark' ? 'light' : 'dark' })),
    }),
    {
      name: 'saniguard-auth',
      partialize: (s) => ({ user: s.user, token: s.token, role: s.role, theme: s.theme }),
    }
  )
)
