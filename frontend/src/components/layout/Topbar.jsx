import { useNavigate } from 'react-router-dom'
import { Sun, Moon, Bell } from 'lucide-react'
import { useAuthStore } from '../../store/auth-store'

export default function Topbar({ title, subtitle }) {
  const navigate = useNavigate()
  const { theme, toggleTheme, user } = useAuthStore()
  const initial = user?.full_name?.[0]?.toUpperCase() ?? '?'

  return (
    <div className="sg-sidebar sg-border border-b px-6 py-4 flex items-center justify-between">
      <div>
        <h1 className="text-base font-semibold sg-text">{title}</h1>
        <p className="text-xs sg-muted">{subtitle ?? 'IT Building Ground Floor Toilet'}</p>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={toggleTheme}
          className="h-8 w-8 rounded-lg flex items-center justify-center sg-border border hover:border-cyan-500/40 sg-muted hover:text-cyan-400 transition-colors"
          title="Toggle theme"
          type="button"
        >
          {theme === 'dark' ? <Sun size={15} /> : <Moon size={15} />}
        </button>

        <div className="relative">
          <button
            type="button"
            onClick={() => navigate('/app/alerts')}
            className="h-8 w-8 rounded-lg flex items-center justify-center sg-border border hover:border-cyan-500/40 sg-muted hover:text-cyan-400 transition-colors"
            title="Go to alerts"
          >
            <Bell size={15} />
          </button>
          <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-red-500 flex items-center justify-center text-white text-[10px] font-bold">
            2
          </span>
        </div>

        <div className="h-8 w-8 rounded-full bg-cyan-500 flex items-center justify-center text-white text-sm font-bold">
          {initial}
        </div>
      </div>
    </div>
  )
}
