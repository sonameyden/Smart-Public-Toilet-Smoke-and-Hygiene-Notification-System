import { cn } from '../../lib/utils'

export default function Card({ children, className, ...props }) {
  return (
    <div
      className={cn(
        'sg-card sg-border border rounded-xl p-4',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}
