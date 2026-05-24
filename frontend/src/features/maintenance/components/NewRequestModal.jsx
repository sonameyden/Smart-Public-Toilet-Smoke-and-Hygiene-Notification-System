import { useState } from 'react'
import { X } from 'lucide-react'

export default function NewRequestModal({ onClose, onSubmit, loading }) {
  const [form, setForm] = useState({ type: 'preventive', title: '', description: '', notes: '' })
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }))

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(form)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="sg-card sg-border border rounded-2xl p-6 w-full max-w-md shadow-2xl">
        <div className="flex items-center justify-between mb-5">
          <h3 className="text-base font-semibold sg-text">New Maintenance Request</h3>
          <button onClick={onClose} className="sg-muted hover:sg-text">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs sg-muted mb-1.5">Type</label>
            <select value={form.type} onChange={set('type')} className="sg-input">
              <option value="preventive">Preventive</option>
              <option value="corrective">Corrective</option>
            </select>
          </div>

          <div>
            <label className="block text-xs sg-muted mb-1.5">Title</label>
            <input
              value={form.title}
              onChange={set('title')}
              placeholder="e.g. Monthly sensor calibration"
              required
              className="sg-input"
            />
          </div>

          <div>
            <label className="block text-xs sg-muted mb-1.5">Description</label>
            <textarea
              value={form.description}
              onChange={set('description')}
              rows={3}
              className="sg-input resize-none"
              placeholder="Describe the maintenance task…"
            />
          </div>

          <div>
            <label className="block text-xs sg-muted mb-1.5">Notes (optional)</label>
            <input value={form.notes} onChange={set('notes')} className="sg-input" />
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 rounded-lg py-2 text-sm sg-muted sg-border border hover:sg-text transition-colors"
            >
              Cancel
            </button>
            <button type="submit" disabled={loading} className="flex-1 sg-btn-primary">
              {loading ? 'Submitting…' : 'Create Request'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
