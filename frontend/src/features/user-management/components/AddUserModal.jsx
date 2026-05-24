import { useState } from 'react'
import { X, UserPlus } from 'lucide-react'

export default function AddUserModal({ onClose, onSubmit, loading }) {
  const [form, setForm] = useState({ full_name: '', email: '', password: '', role: 'viewer' })
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }))

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(form)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="sg-card sg-border border rounded-2xl p-6 w-full max-w-md shadow-2xl">
        <div className="flex items-center justify-between mb-5">
          <h3 className="text-base font-semibold sg-text">Add New User</h3>
          <button onClick={onClose} className="sg-muted hover:sg-text">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs sg-muted mb-1.5">Full Name</label>
            <input value={form.full_name} onChange={set('full_name')} placeholder="John Doe" required className="sg-input" />
          </div>

          <div>
            <label className="block text-xs sg-muted mb-1.5">Email</label>
            <input type="email" value={form.email} onChange={set('email')} placeholder="john@campus.edu" required className="sg-input" />
          </div>

          <div>
            <label className="block text-xs sg-muted mb-1.5">Password</label>
            <input type="password" value={form.password} onChange={set('password')} placeholder="Min. 6 characters" required className="sg-input" />
          </div>

          <div>
            <label className="block text-xs sg-muted mb-1.5">Role</label>
            <select value={form.role} onChange={set('role')} className="sg-input">
              <option value="viewer">Viewer</option>
              <option value="maintenance">Maintenance</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <div className="flex gap-3 pt-2">
            <button type="button" onClick={onClose} className="flex-1 rounded-lg py-2 text-sm sg-muted sg-border border hover:sg-text transition-colors">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="flex-1 sg-btn-primary">
              <UserPlus size={14} />
              {loading ? 'Adding…' : 'Add User'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
