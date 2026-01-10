import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import './DCATestingPage.css';

interface Case {
  id: number;
  case_id: string;
  customer_name: string;
  overdue_amount: number;
  status: string;
  priority: string;
  dca_name: string;
  dca_id: number | null;
  confirmation_received: boolean;
  created_at: string;
  assigned_at: string | null;
}

interface DCA {
  id: number;
  name: string;
  performance_score: string;
  active_cases: number;
  total_completed: number;
  total_rejected: number;
  total_delays: number;
  avg_completion_time: number;
  min_debt: number;
  max_debt: number;
}

const DCATestingPage: React.FC = () => {
  const [cases, setCases] = useState<Case[]>([]);
  const [dcas, setDCAs] = useState<DCA[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDCA, setSelectedDCA] = useState<number | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [casesResponse, dcasResponse] = await Promise.all([
        apiService.get('/api/v1/testing/cases'),
        apiService.get('/api/v1/testing/dcas')
      ]);
      setCases(casesResponse.data);
      setDCAs(dcasResponse.data);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateCaseStatus = async (caseId: number, status: string, confirmation: boolean = false) => {
    try {
      await apiService.post('/api/v1/testing/update-status', {
        case_id: caseId,
        status,
        confirmation_received: confirmation
      });
      await loadData();
      alert('Case status updated successfully!');
    } catch (error) {
      console.error('Error updating status:', error);
      alert('Failed to update status');
    }
  };

  const simulateRejection = async (caseId: number) => {
    try {
      await apiService.post(`/api/v1/testing/simulate-rejection/${caseId}`);
      await loadData();
      alert('Case rejection simulated successfully!');
    } catch (error) {
      console.error('Error simulating rejection:', error);
      alert('Failed to simulate rejection');
    }
  };

  const simulateDelay = async (caseId: number) => {
    try {
      await apiService.post(`/api/v1/testing/simulate-delay/${caseId}`);
      await loadData();
      alert('Delay recorded successfully!');
    } catch (error) {
      console.error('Error simulating delay:', error);
      alert('Failed to record delay');
    }
  };

  const resetAllData = async () => {
    if (!window.confirm('Are you sure you want to reset all dummy data? This will reload all test cases and DCAs.')) {
      return;
    }
    
    try {
      await apiService.post('/api/v1/testing/reset-data');
      await loadData();
      alert('All data has been reset successfully!');
    } catch (error) {
      console.error('Error resetting data:', error);
      alert('Failed to reset data');
    }
  };

  const filteredCases = selectedDCA 
    ? cases.filter(c => c.dca_id === selectedDCA)
    : cases.filter(c => c.dca_id !== null);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="dca-testing-page">
      <div className="header-section">
        <div>
          <h1>🧪 DCA Testing Interface</h1>
          <p className="subtitle">Simulate DCA responses and update case statuses</p>
        </div>
        <button className="btn-reset" onClick={resetAllData}>
          🔄 Reset All Data
        </button>
      </div>

      <div className="testing-container">
        {/* DCA Performance Dashboard */}
        <div className="dca-dashboard">
          <h2>DCA Performance Metrics</h2>
          <div className="dca-grid">
            {dcas.map((dca) => (
              <div 
                key={dca.id} 
                className={`dca-card ${selectedDCA === dca.id ? 'selected' : ''}`}
                onClick={() => setSelectedDCA(selectedDCA === dca.id ? null : dca.id)}
              >
                <h3>{dca.name}</h3>
                <div className="dca-stats">
                  <div className="stat">
                    <span className="stat-label">Score:</span>
                    <span className="stat-value">{dca.performance_score}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Active:</span>
                    <span className="stat-value">{dca.active_cases}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Completed:</span>
                    <span className="stat-value success">{dca.total_completed}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Rejected:</span>
                    <span className="stat-value danger">{dca.total_rejected}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Delays:</span>
                    <span className="stat-value warning">{dca.total_delays}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Avg Time:</span>
                    <span className="stat-value">{dca.avg_completion_time.toFixed(1)} days</span>
                  </div>
                  <div className="stat full-width">
                    <span className="stat-label">Debt Range:</span>
                    <span className="stat-value">${dca.min_debt.toLocaleString()} - ${dca.max_debt.toLocaleString()}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Cases Management */}
        <div className="cases-section">
          <h2>
            {selectedDCA 
              ? `Cases for ${dcas.find(d => d.id === selectedDCA)?.name}` 
              : 'All Assigned Cases'}
            {selectedDCA && (
              <button 
                className="btn-clear-filter" 
                onClick={() => setSelectedDCA(null)}
              >
                Clear Filter
              </button>
            )}
          </h2>

          {filteredCases.length === 0 ? (
            <div className="no-cases">
              <p>No cases assigned to this DCA yet.</p>
            </div>
          ) : (
            <div className="cases-table">
              <table>
                <thead>
                  <tr>
                    <th>Case ID</th>
                    <th>Customer</th>
                    <th>Amount</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>DCA</th>
                    <th>Confirmed</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredCases.map((caseItem) => (
                    <tr key={caseItem.id}>
                      <td className="case-id">{caseItem.case_id}</td>
                      <td>{caseItem.customer_name}</td>
                      <td className="amount">${caseItem.overdue_amount.toLocaleString()}</td>
                      <td>
                        <span className={`priority priority-${caseItem.priority.toLowerCase()}`}>
                          {caseItem.priority}
                        </span>
                      </td>
                      <td>
                        <span className={`status status-${caseItem.status.toLowerCase().replace(' ', '-')}`}>
                          {caseItem.status}
                        </span>
                      </td>
                      <td className="dca-name">{caseItem.dca_name}</td>
                      <td>
                        <span className={`confirm-badge ${caseItem.confirmation_received ? 'confirmed' : 'pending'}`}>
                          {caseItem.confirmation_received ? '✓ Yes' : '○ No'}
                        </span>
                      </td>
                      <td className="actions">
                        {caseItem.status === 'Open' && (
                          <button
                            className="btn btn-sm btn-primary"
                            onClick={() => updateCaseStatus(caseItem.id, 'In Progress')}
                          >
                            Start
                          </button>
                        )}
                        {caseItem.status === 'In Progress' && (
                          <>
                            <button
                              className="btn btn-sm btn-success"
                              onClick={() => updateCaseStatus(caseItem.id, 'Closed', true)}
                            >
                              Complete
                            </button>
                            <button
                              className="btn btn-sm btn-warning"
                              onClick={() => simulateDelay(caseItem.id)}
                            >
                              Delay
                            </button>
                          </>
                        )}
                        {caseItem.status !== 'Closed' && (
                          <button
                            className="btn btn-sm btn-danger"
                            onClick={() => simulateRejection(caseItem.id)}
                          >
                            Reject
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DCATestingPage;
