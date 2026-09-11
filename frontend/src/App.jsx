import { BrowserRouter, NavLink, Route, Routes } from 'react-router-dom'
import Home from './pages/Home'
import MachineList from './pages/MachineList'
import MachineDetail from './pages/MachineDetail'
import Tickets from './pages/Tickets'

function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <nav className="navbar">
          <span className="brand">
            <span className="brand-title">智能设备</span>
            <span className="brand-tagline">预测性维护系统</span>
          </span>
          <div className="nav-links">
            <NavLink to="/" end className={({ isActive }) => (isActive ? 'active' : undefined)}>
              首页
            </NavLink>
            <NavLink to="/devices" className={({ isActive }) => (isActive ? 'active' : undefined)}>
              设备监控
            </NavLink>
            <NavLink to="/tickets" className={({ isActive }) => (isActive ? 'active' : undefined)}>
              维修工单
            </NavLink>
          </div>
        </nav>
        <div className="app-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/devices" element={<MachineList />} />
            <Route path="/machines/:udi" element={<MachineDetail />} />
            <Route path="/tickets" element={<Tickets />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App
