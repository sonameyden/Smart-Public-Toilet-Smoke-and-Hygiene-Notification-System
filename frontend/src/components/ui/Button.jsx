import { cn } from '../../lib/utils'

const variants = {
  primary:   'bg-gradient-to-r from-teal-700 to-cyan-400 text-white hover:opacity-90',
  secondary: 'sg-card sg-border border hover:border-cyan-500/50 sg-text',
  ghost:     'hover:bg-white/5 sg-muted hover:sg-text',
  danger:    'bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30',
  resolve:   'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-500/20',
}

const sizes = {
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-2.5 text-sm',
}

export default function Button({
  variant = 'secondary',
  size = 'md',
  children,
  className,
  ...props
}) {
  return (
    <button
      className={cn(
        'inline-flex items-center gap-2 rounded-lg font-medium transition-all',
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}
