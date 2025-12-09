import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import SubmitIssue from './pages/SubmitIssue'
import IssueList from './pages/IssueList'
import Dashboard from './pages/Dashboard'
import TenantSelect from './pages/TenantSelect'

function App() {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<TenantSelect />} />
            <Route path="/submit" element={<SubmitIssue />} />
            <Route path="/issues" element={<IssueList />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
