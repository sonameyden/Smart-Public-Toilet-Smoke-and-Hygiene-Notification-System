import { Link } from 'react-router-dom'
import { Shield, LogIn } from 'lucide-react'
import RegisterForm from '../components/RegisterForm'
import { useAuth } from '../hooks/useAuth'

export default function RegisterPage() {
  const { registerMutation } = useAuth()

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center px-4 py-10"
      style={{ background: 'linear-gradient(135deg, #0F1923 0%, #0F2A20 100%)' }}
    >
      <div className="flex flex-col items-center mb-6">
        <div className="h-12 w-12 rounded-2xl bg-cyan-500 flex items-center justify-center mb-3 shadow-lg shadow-cyan-500/20">
          <Shield size={22} className="text-white" />
        </div>
        <h1 className="text-xl font-bold sg-text">Saniguard</h1>
        <p className="text-xs sg-muted">Create Your Account</p>
      </div>

      <div className="sg-card sg-border border rounded-2xl p-6 w-full max-w-sm shadow-xl">
        <h2 className="text-base font-semibold sg-text text-center mb-5">Join the System</h2>

        <RegisterForm
          onSubmit={(vals) => registerMutation.mutate(vals)}
          loading={registerMutation.isPending}
          error={registerMutation.error?.response?.data?.detail}
        />

        <p className="text-center text-xs sg-muted mt-4">
          Already have an account?{' '}
          <Link to="/login" className="text-cyan-400 hover:text-cyan-300 font-medium inline-flex items-center gap-1">
            <LogIn size={12} />
            Sign In
          </Link>
        </p>
      </div>

      <p className="mt-6 text-xs sg-muted">Campus Facility Management System v1.0</p>
    </div>
  )
}
