import React, { Suspense, lazy, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/auth-store'
import ProtectedRoute from './routes/ProtectedRoute'
import AppShell from './components/layout/AppShell'

const LoginPage    = lazy(() => import('./features/auth/pages/LoginPage'))
const RegisterPage = lazy(() => import('./features/auth/pages/RegisterPage'))
const DashboardPage = lazy(() => import('./features/dashboard/pages/DashboardPage'))
const AlertsPage    = lazy(() => import('./features/alerts/pages/AlertsPage'))
const MaintenancePage = lazy(() => import('./features/maintenance/pages/MaintenancePage'))
const AnalyticsPage   = lazy(() => import('./features/analytics/pages/AnalyticsPage'))
const UserManagementPage = lazy(() => import('./features/user-management/pages/UserManagementPage'))
const SettingsPage = lazy(() => import('./features/settings/pages/SettingsPage'))

const Loader = () => (
  <div className="flex h-screen items-center justify-center sg-bg">
    <div className="h-8 w-8 animate-spin rounded-full border-2 border-t-transparent" style={{ borderColor: '#06B6D4', borderTopColor: 'transparent' }} />
  </div>
)

export default function App() {
  const { theme } = useAuthStore()

  useEffect(() => {
    document.documentElement.className = theme === 'light' ? 'light' : ''
  }, [theme])

  return (
    <BrowserRouter>
      <Suspense fallback={<Loader />}>
        <Routes>
          <Route path="/login"    element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/app" element={<ProtectedRoute><AppShell /></ProtectedRoute>}>
            <Route index element={<Navigate to="dashboard" replace />} />
            <Route path="dashboard"  element={<DashboardPage />} />
            <Route path="alerts"     element={<AlertsPage />} />
            <Route path="maintenance" element={<MaintenancePage />} />
            <Route path="analytics"  element={<AnalyticsPage />} />
            <Route path="users"      element={<UserManagementPage />} />
            <Route path="settings"   element={<SettingsPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}
