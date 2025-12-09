import { useState } from 'react'
import { civicPulseApi } from '../api/civicpulseApi'

function SubmitIssue() {
  const [formData, setFormData] = useState({
    tenant_id: 1,
    description: '',
    location: '',
  })
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    setMessage('')

    try {
      const response = await civicPulseApi.submitReport(formData)
      setMessage('Report submitted successfully!')
      setFormData({ ...formData, description: '', location: '' })
      console.log('Report submitted:', response.data)
    } catch (error) {
      setMessage('Error submitting report. Please try again.')
      console.error('Error:', error)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="page submit-issue">
      <h1>Submit an Issue Report</h1>
      <form onSubmit={handleSubmit} className="issue-form">
        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            placeholder="Describe the issue..."
            rows={6}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="location">Location (optional)</label>
          <input
            id="location"
            type="text"
            value={formData.location}
            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
            placeholder="e.g., Main St & 1st Ave"
          />
        </div>

        <button type="submit" disabled={submitting}>
          {submitting ? 'Submitting...' : 'Submit Report'}
        </button>

        {message && <div className="message">{message}</div>}
      </form>
    </div>
  )
}

export default SubmitIssue
