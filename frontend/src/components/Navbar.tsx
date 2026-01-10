import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

const Navbar: React.FC = () => {
  const { user, logout, isAdmin } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <span className="brand-logo">📦</span>
          <span className="brand-name">FedEx DCA Management</span>
        </div>

        <div className="navbar-links">
          <NavLink to="/dashboard" className={({ isActive }) => (isActive ? 'active' : '')}>
            Dashboard
          </NavLink>
          <NavLink to="/cases" className={({ isActive }) => (isActive ? 'active' : '')}>
            Cases
          </NavLink>
          <NavLink to="/dcas" className={({ isActive }) => (isActive ? 'active' : '')}>
            DCAs
          </NavLink>
          <NavLink to="/audit-logs" className={({ isActive }) => (isActive ? 'active' : '')}>
            Audit Log
          </NavLink>
          {isAdmin && (
            <>
              <NavLink to="/testing" className={({ isActive }) => (isActive ? 'active' : '')}>
                🧪 Testing
              </NavLink>
              <NavLink to="/settings" className={({ isActive }) => (isActive ? 'active' : '')}>
                ⚙️ Settings
              </NavLink>
            </>
          )}
        </div>

        <div className="navbar-user">
          <div className="user-info">
            <span className="user-name">{user?.full_name || user?.username}</span>
            {isAdmin && <span className="user-role">Admin</span>}
          </div>
          <button onClick={logout} className="logout-btn">
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
