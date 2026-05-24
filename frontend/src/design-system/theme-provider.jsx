import { createContext, useContext, useEffect } from 'react'
import { useAuthStore } from '../store/auth-store'

const ThemeContext = createContext(null)

export function ThemeProvider({ children }) {
  const { theme } = useAuthStore()

  useEffect(() => {
    document.documentElement.className = theme === 'light' ? 'light' : ''
  }, [theme])

  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => useContext(ThemeContext)
