export function cn(...classes) {
  return classes.filter(Boolean).join(' ')
}

export function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleString('en-US', {
    month: 'numeric', day: 'numeric', year: 'numeric',
    hour: 'numeric', minute: '2-digit',
  })
}

export function formatPPM(value) {
  if (value == null) return '—'
  return `${Number(value).toFixed(1)} ppm`
}

export function severityColor(severity) {
  switch (severity) {
    case 'critical': return '#EF4444'
    case 'high':     return '#EF4444'
    case 'medium':   return '#F59E0B'
    case 'low':      return '#94A3B8'
    default:         return '#94A3B8'
  }
}

export function statusColor(status) {
  return status === 'active' ? '#EF4444' : '#22C55E'
}
