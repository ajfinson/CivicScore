interface Issue {
  id: number
  category: string
  severity: string
  status: string
  created_at: string
  description?: string
}

interface IssueCardProps {
  issue: Issue
}

function IssueCard({ issue }: IssueCardProps) {
  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return '#dc3545'
      case 'high':
        return '#fd7e14'
      case 'medium':
        return '#ffc107'
      case 'low':
        return '#28a745'
      default:
        return '#6c757d'
    }
  }

  return (
    <div className="issue-card">
      <div className="issue-header">
        <span className="issue-id">#{issue.id}</span>
        <span 
          className="severity-badge"
          style={{ backgroundColor: getSeverityColor(issue.severity) }}
        >
          {issue.severity}
        </span>
      </div>

      <div className="issue-body">
        <div className="issue-category">{issue.category}</div>
        {issue.description && (
          <p className="issue-description">{issue.description}</p>
        )}
      </div>

      <div className="issue-footer">
        <span className="issue-status">{issue.status}</span>
        <span className="issue-date">
          {new Date(issue.created_at).toLocaleDateString()}
        </span>
      </div>
    </div>
  )
}

export default IssueCard
