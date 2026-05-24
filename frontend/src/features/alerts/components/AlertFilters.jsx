const STATUS_OPTIONS   = ['all', 'active', 'resolved']
const SEVERITY_OPTIONS = ['all', 'critical', 'high', 'medium', 'low']

function FilterPill({ label, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-1 rounded-full text-xs font-medium transition-colors capitalize ${
        active
          ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/40'
          : 'sg-border border sg-muted hover:sg-text'
      }`}
    >
      {label}
    </button>
  )
}

export default function AlertFilters({ filters, onChange }) {
  return (
    <div className="flex flex-wrap gap-4">
      <div className="flex items-center gap-2">
        <span className="text-xs sg-muted">Status:</span>
        <div className="flex gap-1">
          {STATUS_OPTIONS.map((s) => (
            <FilterPill
              key={s}
              label={s}
              active={filters.status === s || (!filters.status && s === 'all')}
              onClick={() => onChange({ ...filters, status: s === 'all' ? undefined : s })}
            />
          ))}
        </div>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-xs sg-muted">Severity:</span>
        <div className="flex gap-1">
          {SEVERITY_OPTIONS.map((s) => (
            <FilterPill
              key={s}
              label={s}
              active={filters.severity === s || (!filters.severity && s === 'all')}
              onClick={() => onChange({ ...filters, severity: s === 'all' ? undefined : s })}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
