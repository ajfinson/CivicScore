import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function TenantSelect() {
  const [selectedTenant, setSelectedTenant] = useState('')
  const navigate = useNavigate()

  const tenants = [
    { id: 1, name: 'City of Springfield', type: 'city' },
    { id: 2, name: 'Downtown Tower', type: 'building' },
    { id: 3, name: 'State University Campus', type: 'campus' },
  ]

  const handleSelect = () => {
    if (selectedTenant) {
      // Store tenant selection in localStorage
      localStorage.setItem('selectedTenant', selectedTenant)
      navigate('/dashboard')
    }
  }

  return (
    <div className="page tenant-select">
      <h1>CivicPulse Engine</h1>
      <p>Select a tenant to get started:</p>

      <div className="tenant-list">
        {tenants.map((tenant) => (
          <div
            key={tenant.id}
            className={`tenant-card ${selectedTenant === tenant.id.toString() ? 'selected' : ''}`}
            onClick={() => setSelectedTenant(tenant.id.toString())}
          >
            <h3>{tenant.name}</h3>
            <span className="tenant-type">{tenant.type}</span>
          </div>
        ))}
      </div>

      <button onClick={handleSelect} disabled={!selectedTenant}>
        Continue
      </button>
    </div>
  )
}

export default TenantSelect
