import { useState, useEffect } from 'react'
import { civicPulseApi } from '../api/civicpulseApi'
import IssueCard from '../components/IssueCard'
import Filters from '../components/Filters'

interface Issue {
  id: number
  category: string
  severity: string
  status: string
  created_at: string
  description?: string
}

function IssueList() {
  const [issues, setIssues] = useState<Issue[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    tenantId: 1,
    status: '',
  })

  useEffect(() => {
    loadIssues()
  }, [filters])

  const loadIssues = async () => {
    setLoading(true)
    try {
      const response = await civicPulseApi.listIssues(
        filters.tenantId,
        filters.status || undefined
      )
      setIssues(response.data.issues || [])
    } catch (error) {
      console.error('Error loading issues:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page issue-list">
      <h1>Issues</h1>
      
      <Filters filters={filters} onChange={setFilters} />

      {loading ? (
        <div>Loading issues...</div>
      ) : (
        <div className="issues-grid">
          {issues.length === 0 ? (
            <p>No issues found.</p>
          ) : (
            issues.map((issue) => <IssueCard key={issue.id} issue={issue} />)
          )}
        </div>
      )}
    </div>
  )
}

export default IssueList
