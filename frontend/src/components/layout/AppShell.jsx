import { Outlet, useLocation } from 'react-router-dom'
import { Suspense } from 'react'
import Sidebar from './Sidebar'

const PAGE_TITLES = {
  '/app/dashboard':   'Dashboard',
  '/app/alerts':      'Alerts',
  '/app/maintenance': 'Maintenance',
  '/app/analytics':   'Analytics',
  '/app/users':       'User Management',
  '/app/settings':    'Settings',
}

function PageLoader() {
  return (
    <div className="flex h-full items-center justify-center">
      <div
        className="h-8 w-8 animate-spin rounded-full border-2 border-t-transparent"
        style={{ borderColor: '#06B6D4', borderTopColor: 'transparent' }}
      />
    </div>
  )
}

export default function AppShell() {
  const { pathname } = useLocation()
  const title = PAGE_TITLES[pathname] ?? 'Dashboard'

  return (
    <div className="flex h-screen sg-bg overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <main className="flex-1 overflow-y-auto">
          <div className="h-full min-h-[calc(100vh-4rem)] overflow-hidden">
            <Suspense fallback={<PageLoader />}>
              <div key={pathname} className="h-full min-h-full page-transition">
                <Outlet />
              </div>
            </Suspense>
          </div>
        </main>
      </div>
    </div>
  )
}
