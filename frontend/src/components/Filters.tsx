interface FiltersProps {
  filters: {
    tenantId: number
    status: string
  }
  onChange: (filters: any) => void
}

function Filters({ filters, onChange }: FiltersProps) {
  const statuses = ['', 'open', 'in-progress', 'resolved', 'closed']

  return (
    <div className="filters">
      <div className="filter-group">
        <label htmlFor="status">Status:</label>
        <select
          id="status"
          value={filters.status}
          onChange={(e) => onChange({ ...filters, status: e.target.value })}
        >
          <option value="">All</option>
          {statuses.slice(1).map((status) => (
            <option key={status} value={status}>
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label htmlFor="tenant">Tenant ID:</label>
        <input
          id="tenant"
          type="number"
          value={filters.tenantId}
          onChange={(e) => onChange({ ...filters, tenantId: parseInt(e.target.value) })}
          min="1"
        />
      </div>
    </div>
  )
}

export default Filters
