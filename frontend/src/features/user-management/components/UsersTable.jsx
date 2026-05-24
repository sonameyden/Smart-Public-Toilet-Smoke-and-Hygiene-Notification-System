import { Pencil, Trash2 } from 'lucide-react'
import Badge from '../../../components/ui/Badge'
import { formatDate } from '../../../lib/utils'

export default function UsersTable({ users = [], onEdit, onDelete }) {
  return (
    <div className="sg-card sg-border border rounded-xl overflow-hidden">
      <table className="w-full text-sm">
        <thead>
          <tr className="sg-border border-b">
            <th className="text-left px-4 py-3 text-xs font-medium sg-muted">User</th>
            <th className="text-left px-4 py-3 text-xs font-medium sg-muted">Role</th>
            <th className="text-left px-4 py-3 text-xs font-medium sg-muted">Status</th>
            <th className="text-left px-4 py-3 text-xs font-medium sg-muted">Last Login</th>
            <th className="text-left px-4 py-3 text-xs font-medium sg-muted">Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => {
            const initial = user.full_name?.[0]?.toUpperCase() ?? '?'
            return (
              <tr key={user.id} className="sg-border border-b last:border-0 hover:bg-white/5 transition-colors">
                <td className="px-4 py-3">
                  <div className="flex items-center gap-3">
                    <div className="h-8 w-8 rounded-full bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400 text-xs font-bold">
                      {initial}
                    </div>
                    <div>
                      <p className="font-medium sg-text">{user.full_name}</p>
                      <p className="text-xs sg-muted">{user.email}</p>
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3">
                  <Badge variant={user.role}>{user.role}</Badge>
                </td>
                <td className="px-4 py-3">
                  <Badge variant={user.is_active ? 'operational' : 'resolved'}>
                    {user.is_active ? 'Operational' : 'Inactive'}
                  </Badge>
                </td>
                <td className="px-4 py-3 text-xs sg-muted">
                  {user.last_login ? formatDate(user.last_login) : 'Never'}
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => onEdit?.(user)}
                      className="h-7 w-7 rounded-lg flex items-center justify-center sg-muted hover:text-cyan-400 hover:bg-cyan-500/10 transition-colors"
                    >
                      <Pencil size={13} />
                    </button>
                    <button
                      onClick={() => onDelete?.(user.id)}
                      className="h-7 w-7 rounded-lg flex items-center justify-center sg-muted hover:text-red-400 hover:bg-red-500/10 transition-colors"
                    >
                      <Trash2 size={13} />
                    </button>
                  </div>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
