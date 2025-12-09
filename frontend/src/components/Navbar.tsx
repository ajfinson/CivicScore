import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-brand">
        <Link to="/">CivicPulse</Link>
      </div>
      
      <div className="nav-links">
        <Link to="/submit">Submit Issue</Link>
        <Link to="/issues">View Issues</Link>
        <Link to="/dashboard">Dashboard</Link>
      </div>
    </nav>
  )
}

export default Navbar
