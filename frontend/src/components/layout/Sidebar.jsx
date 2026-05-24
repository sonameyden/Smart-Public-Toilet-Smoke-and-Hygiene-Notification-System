import { NavLink, useNavigate } from 'react-router-dom'
import {
  LayoutDashboard, Bell, Wrench, BarChart2,
  Users, Settings, Shield, LogOut,
} from 'lucide-react'
import { useAuthStore } from '../../store/auth-store'

const ALL_NAV = [
  { to: '/app/dashboard',   label: 'Dashboard',       icon: LayoutDashboard, roles: ['admin','maintenance','viewer'] },
  { to: '/app/alerts',      label: 'Alerts',           icon: Bell,            roles: ['admin','maintenance','viewer'] },
  { to: '/app/maintenance', label: 'Maintenance',      icon: Wrench,          roles: ['admin','maintenance'] },
  { to: '/app/analytics',   label: 'Analytics',        icon: BarChart2,       roles: ['admin'] },
  { to: '/app/users',       label: 'User Management',  icon: Users,           roles: ['admin'] },
  { to: '/app/settings',    label: 'Settings',         icon: Settings,        roles: ['admin'] },
]

function Avatar({ name, role }) {
  const initial = name?.[0]?.toUpperCase() ?? '?'
  return (
    <div className="flex items-center gap-2">
      <div className="h-8 w-8 rounded-full bg-cyan-500 flex items-center justify-center text-white text-sm font-bold">
        {initial}
      </div>
      <div>
        <p className="text-sm font-medium sg-text leading-none">{name}</p>
        <p className="text-xs sg-muted capitalize">{role}</p>
      </div>
    </div>
  )
}

export default function Sidebar() {
  const { user, role, clearAuth } = useAuthStore()
  const navigate = useNavigate()

  const items = ALL_NAV.filter((n) => n.roles.includes(role))

  const handleSignOut = () => {
    clearAuth()
    navigate('/login')
  }

  return (
    <aside
      className="sg-sidebar sg-border border-r flex flex-col w-56 shrink-0 h-screen sticky top-0"
    >
      {/* Brand */}
      <div className="px-4 py-5 flex items-center gap-3 sg-border border-b">
        <div className="h-8 w-8 rounded-lg bg-cyan-500 flex items-center justify-center">
          <Shield size={16} className="text-white" />
        </div>
        <div>
          <p className="text-sm font-bold sg-text leading-none">Saniguard</p>
          <p className="text-xs sg-muted">Smart Monitoring</p>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 flex flex-col gap-1 overflow-y-auto">
        {items.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors cursor-pointer ${
                isActive
                  ? 'text-cyan-400'
                  : 'sg-muted hover:sg-text'
              }`
            }
            style={({ isActive }) =>
              isActive
                ? { background: 'rgba(6,182,212,0.12)', borderLeft: '2px solid #06B6D4' }
                : {}
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* User + Sign out */}
      <div className="px-4 py-4 sg-border border-t space-y-3">
        <Avatar name={user?.full_name ?? 'Demo User'} role={role} />
        <button
          onClick={handleSignOut}
          className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm sg-muted hover:text-red-400 transition-colors"
        >
          <LogOut size={14} />
          Sign Out
        </button>
      </div>
    </aside>
  )
}
