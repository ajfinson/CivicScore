import { useState, useEffect } from 'react'
import { civicPulseApi } from '../api/civicpulseApi'
import Charts from '../components/Charts'

interface ScoreData {
  tenant_id: number
  scores: {
    overall?: number
    sla_compliance?: number
    resolution_time?: number
  }
}

function Dashboard() {
  const [scoreData, setScoreData] = useState<ScoreData | null>(null)
  const [leaderboard, setLeaderboard] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [tenantId] = useState(1)

  useEffect(() => {
    loadDashboardData()
  }, [tenantId])

  const loadDashboardData = async () => {
    setLoading(true)
    try {
      const [scoresRes, leaderboardRes] = await Promise.all([
        civicPulseApi.getTenantScores(tenantId),
        civicPulseApi.getLeaderboard(tenantId),
      ])
      
      setScoreData(scoresRes.data)
      setLeaderboard(leaderboardRes.data.leaderboard || [])
    } catch (error) {
      console.error('Error loading dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="page dashboard">Loading dashboard...</div>
  }

  return (
    <div className="page dashboard">
      <h1>Performance Dashboard</h1>

      <div className="score-cards">
        <div className="score-card">
          <h3>Overall Score</h3>
          <div className="score-value">
            {scoreData?.scores?.overall?.toFixed(1) || 'N/A'}
          </div>
        </div>

        <div className="score-card">
          <h3>SLA Compliance</h3>
          <div className="score-value">
            {scoreData?.scores?.sla_compliance 
              ? `${(scoreData.scores.sla_compliance * 100).toFixed(1)}%`
              : 'N/A'}
          </div>
        </div>

        <div className="score-card">
          <h3>Avg Resolution Time</h3>
          <div className="score-value">
            {scoreData?.scores?.resolution_time?.toFixed(1) || 'N/A'} hrs
          </div>
        </div>
      </div>

      <Charts data={scoreData} />

      <div className="leaderboard">
        <h2>Leaderboard</h2>
        {leaderboard.length === 0 ? (
          <p>No leaderboard data available.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Rank</th>
                <th>Name</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((entry, index) => (
                <tr key={index}>
                  <td>{index + 1}</td>
                  <td>{entry.name}</td>
                  <td>{entry.score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default Dashboard
