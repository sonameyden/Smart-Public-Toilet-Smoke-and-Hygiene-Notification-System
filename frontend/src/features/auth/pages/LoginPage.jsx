import { Link } from 'react-router-dom'
import { Shield, UserPlus } from 'lucide-react'
import DemoLoginPanel from '../components/DemoLoginPanel'
import LoginForm from '../components/LoginForm'
import { useAuth } from '../hooks/useAuth'

export default function LoginPage() {
  const { loginMutation, demoLoginMutation } = useAuth()

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center px-4"
      style={{ background: 'linear-gradient(135deg, #0F1923 0%, #0F2A20 100%)' }}
    >
      {/* Brand */}
      <div className="flex flex-col items-center mb-6">
        <div className="h-12 w-12 rounded-2xl bg-cyan-500 flex items-center justify-center mb-3 shadow-lg shadow-cyan-500/20">
          <Shield size={22} className="text-white" />
        </div>
        <h1 className="text-xl font-bold sg-text">Saniguard</h1>
        <p className="text-xs sg-muted">Smart Toilet Monitoring System</p>
      </div>

      {/* Card */}
      <div className="sg-card sg-border border rounded-2xl p-6 w-full max-w-sm shadow-xl">
        <h2 className="text-base font-semibold sg-text text-center mb-5">Welcome Back</h2>

        <DemoLoginPanel
          onDemo={(role) => demoLoginMutation.mutate(role)}
          loading={demoLoginMutation.isPending}
        />

        <div className="flex items-center gap-3 my-4">
          <div className="flex-1 h-px sg-border border-t" />
          <span className="text-xs sg-muted">or sign in with email</span>
          <div className="flex-1 h-px sg-border border-t" />
        </div>

        <LoginForm
          onSubmit={(vals) => loginMutation.mutate(vals)}
          loading={loginMutation.isPending}
          error={loginMutation.error?.response?.data?.detail}
        />

        <p className="text-center text-xs sg-muted mt-4">
          Don't have an account?{' '}
          <Link to="/register" className="text-cyan-400 hover:text-cyan-300 font-medium inline-flex items-center gap-1">
            <UserPlus size={12} />
            Create Account
          </Link>
        </p>
      </div>

      <p className="mt-6 text-xs sg-muted">Campus Facility Management System v1.0</p>
    </div>
  )
}
