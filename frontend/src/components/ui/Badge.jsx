import { cn } from '../../lib/utils'

const variants = {
  high:        'bg-red-500/20 text-red-400 border border-red-500/30',
  critical:    'bg-red-500/20 text-red-400 border border-red-500/30',
  medium:      'bg-amber-500/20 text-amber-400 border border-amber-500/30',
  low:         'bg-slate-500/20 text-slate-400 border border-slate-500/30',
  active:      'bg-red-500/20 text-red-400 border border-red-500/30',
  resolved:    'bg-green-500/20 text-green-400 border border-green-500/30',
  admin:       'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30',
  maintenance: 'bg-amber-500/20 text-amber-400 border border-amber-500/30',
  viewer:      'bg-slate-500/20 text-slate-400 border border-slate-500/30',
  operational: 'bg-green-500/20 text-green-400 border border-green-500/30',
  pending:     'bg-amber-500/20 text-amber-400 border border-amber-500/30',
  in_progress: 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30',
  completed:   'bg-green-500/20 text-green-400 border border-green-500/30',
}

export default function Badge({ variant = 'low', children, className }) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-md px-2 py-0.5 text-xs font-semibold capitalize',
        variants[variant] ?? variants.low,
        className
      )}
    >
      {children}
    </span>
  )
}
