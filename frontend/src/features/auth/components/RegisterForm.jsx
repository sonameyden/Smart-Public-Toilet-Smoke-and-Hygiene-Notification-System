import { useState } from 'react'
import { User, Mail, Lock, Eye, EyeOff, UserPlus, Shield, Wrench } from 'lucide-react'

const ROLES = [
  { id: 'viewer',      label: 'Viewer / Authority',  sub: 'Read-only monitoring access',      icon: Eye },
  { id: 'maintenance', label: 'Maintenance Staff',    sub: 'Maintenance management access',    icon: Wrench },
  { id: 'admin',       label: 'Administrator',        sub: 'Full system access',               icon: Shield },
]

export default function RegisterForm({ onSubmit, loading, error }) {
  const [form, setForm] = useState({ full_name: '', email: '', password: '', confirmPassword: '', role: 'viewer' })
  const [showPw, setShowPw] = useState(false)

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }))

  const handleSubmit = (e) => {
    e.preventDefault()
    if (form.password !== form.confirmPassword) return
    onSubmit({ full_name: form.full_name, email: form.email, password: form.password, role: form.role })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <p className="rounded-lg bg-red-500/10 border border-red-500/20 px-3 py-2 text-xs text-red-400">
          {error}
        </p>
      )}

      <div>
        <label className="block text-xs sg-muted mb-1.5">Full Name</label>
        <div className="relative">
          <User size={14} className="absolute left-3 top-1/2 -translate-y-1/2 sg-muted" />
          <input value={form.full_name} onChange={set('full_name')} placeholder="John Doe" required className="sg-input pl-9" />
        </div>
      </div>

      <div>
        <label className="block text-xs sg-muted mb-1.5">Email Address</label>
        <div className="relative">
          <Mail size={14} className="absolute left-3 top-1/2 -translate-y-1/2 sg-muted" />
          <input type="email" value={form.email} onChange={set('email')} placeholder="john@campus.edu" required className="sg-input pl-9" />
        </div>
      </div>

      <div>
        <label className="block text-xs sg-muted mb-1.5">Password</label>
        <div className="relative">
          <Lock size={14} className="absolute left-3 top-1/2 -translate-y-1/2 sg-muted" />
          <input type={showPw ? 'text' : 'password'} value={form.password} onChange={set('password')} placeholder="Minimum 6 characters" required className="sg-input pl-9 pr-9" />
          <button type="button" onClick={() => setShowPw(!showPw)} className="absolute right-3 top-1/2 -translate-y-1/2 sg-muted">
            {showPw ? <EyeOff size={14} /> : <Eye size={14} />}
          </button>
        </div>
      </div>

      <div>
        <label className="block text-xs sg-muted mb-1.5">Confirm Password</label>
        <div className="relative">
          <Lock size={14} className="absolute left-3 top-1/2 -translate-y-1/2 sg-muted" />
          <input type="password" value={form.confirmPassword} onChange={set('confirmPassword')} placeholder="Confirm your password" required className="sg-input pl-9" />
        </div>
      </div>

      <div>
        <label className="block text-xs sg-muted mb-2">Select Role</label>
        <div className="space-y-2">
          {ROLES.map(({ id, label, sub, icon: Icon }) => (
            <button
              key={id}
              type="button"
              onClick={() => setForm((f) => ({ ...f, role: id }))}
              className={`w-full flex items-center gap-3 rounded-lg px-3 py-2.5 text-left transition-all border ${
                form.role === id
                  ? 'border-cyan-500/60 bg-cyan-500/10'
                  : 'sg-border sg-card'
              }`}
            >
              <Icon size={15} className={form.role === id ? 'text-cyan-400' : 'sg-muted'} />
              <div>
                <p className={`text-sm font-medium ${form.role === id ? 'text-cyan-400' : 'sg-text'}`}>{label}</p>
                <p className="text-xs sg-muted">{sub}</p>
              </div>
            </button>
          ))}
        </div>
      </div>

      <button type="submit" disabled={loading} className="sg-btn-primary">
        <UserPlus size={15} />
        {loading ? 'Creating…' : 'Create Account'}
      </button>
    </form>
  )
}
