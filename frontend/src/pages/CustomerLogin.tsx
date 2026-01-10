import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './CustomerLogin.css';

interface Case {
  id: number;
  case_id: string;
  customer_name: string;
  customer_email: string;
  overdue_amount: number;
  status: string;
  priority: string;
}

const CustomerLogin: React.FC = () => {
  const [email, setEmail] = useState('');
  const [cases, setCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      // Search for cases by customer email
      const response = await fetch(`http://localhost:8000/api/v1/customer/cases?email=${encodeURIComponent(email)}`);
      
      if (!response.ok) {
        throw new Error('No cases found for this email');
      }
      
      const data = await response.json();
      setCases(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load cases');
      setCases([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCaseClick = (caseId: number) => {
    // Store customer info and navigate to customer dashboard
    localStorage.setItem('customer_email', email);
    localStorage.setItem('customer_case_id', caseId.toString());
    navigate(`/customer/dashboard/${caseId}`);
  };

  return (
    <div className="customer-login-page">
      <div className="customer-login-container">
        <div className="login-header">
          <h1>Customer Portal</h1>
          <p>Enter your email to view your cases</p>
        </div>

        <form onSubmit={handleSearch} className="search-form">
          <div className="form-group">
            <label>Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your.email@example.com"
              required
            />
          </div>
          <button type="submit" className="btn-search" disabled={loading}>
            {loading ? 'Searching...' : 'Find My Cases'}
          </button>
        </form>

        {error && <div className="error-message">{error}</div>}

        {cases.length > 0 && (
          <div className="cases-list">
            <h3>Your Cases</h3>
            <p className="subtitle">Click on a case to view details and manage it</p>
            {cases.map((caseItem) => (
              <div
                key={caseItem.id}
                className="case-card"
                onClick={() => handleCaseClick(caseItem.id)}
              >
                <div className="case-header">
                  <h4>{caseItem.case_id}</h4>
                  <span className={`status-badge ${caseItem.status.toLowerCase()}`}>
                    {caseItem.status}
                  </span>
                </div>
                <div className="case-details">
                  <p><strong>Customer:</strong> {caseItem.customer_name}</p>
                  <p><strong>Amount:</strong> ${caseItem.overdue_amount.toLocaleString()}</p>
                  <p><strong>Priority:</strong> {caseItem.priority}</p>
                </div>
                <button className="btn-access">Access Dashboard →</button>
              </div>
            ))}
          </div>
        )}

        <div className="login-footer">
          <p>Admin? <a href="/login">Click here for Admin Login</a></p>
        </div>
      </div>
    </div>
  );
};

export default CustomerLogin;
