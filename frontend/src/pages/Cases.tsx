import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiService } from '../services/api';
import './Cases.css';

interface Case {
  id: number;
  case_id: string;
  customer_name: string;
  overdue_amount: number;
  ageing_days: number;
  status: string;
  priority: string;
  sla_status: string;
  sla_due_date: string;
  ai_recovery_score: number;
  dca: {
    name: string;
  } | null;
  created_at: string;
}

const Cases: React.FC = () => {
  const [cases, setCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState({ status: '', priority: '', sla_status: '' });

  useEffect(() => {
    loadCases();
  }, [filter]);

  const loadCases = async () => {
    try {
      const params: any = {};
      if (filter.status) params.status = filter.status;
      if (filter.priority) params.priority = filter.priority;
      if (filter.sla_status) params.sla_status = filter.sla_status;

      const data = await apiService.getCases(params);
      setCases(data);
    } catch (err) {
      console.error('Failed to load cases:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const getPriorityClass = (priority: string) => {
    const classes: any = {
      P1: 'priority-high',
      P2: 'priority-medium',
      P3: 'priority-low',
    };
    return classes[priority] || '';
  };

  const getSLAClass = (slaStatus: string) => {
    const classes: any = {
      'Breached': 'sla-breached',
      'At Risk': 'sla-risk',
      'On Track': 'sla-track',
    };
    return classes[slaStatus] || '';
  };

  const getStatusClass = (status: string) => {
    const classes: any = {
      'Open': 'status-open',
      'In Progress': 'status-progress',
      'Closed': 'status-closed',
    };
    return classes[status] || '';
  };

  const downloadAllCasesPDF = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/reports/all-cases/pdf', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'all_cases_report.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Error downloading PDF:', error);
      alert('Failed to download PDF report');
    }
  };

  return (
    <div className="cases-page">
      <div className="page-header">
        <h1>Case Management</h1>
        <div className="header-actions">
          <button onClick={downloadAllCasesPDF} className="btn-secondary">
            📄 Download PDF Report
          </button>
          <Link to="/cases/create" className="btn-primary">
            Create New Case
          </Link>
        </div>
      </div>

      <div className="filters">
        <select
          value={filter.status}
          onChange={(e) => setFilter({ ...filter, status: e.target.value })}
        >
          <option value="">All Statuses</option>
          <option value="Open">Open</option>
          <option value="In Progress">In Progress</option>
          <option value="Closed">Closed</option>
        </select>

        <select
          value={filter.priority}
          onChange={(e) => setFilter({ ...filter, priority: e.target.value })}
        >
          <option value="">All Priorities</option>
          <option value="P1">P1 - High</option>
          <option value="P2">P2 - Medium</option>
          <option value="P3">P3 - Low</option>
        </select>

        <select
          value={filter.sla_status}
          onChange={(e) => setFilter({ ...filter, sla_status: e.target.value })}
        >
          <option value="">All SLA Status</option>
          <option value="On Track">On Track</option>
          <option value="At Risk">At Risk</option>
          <option value="Breached">Breached</option>
        </select>
      </div>

      {loading ? (
        <div className="loading">Loading cases...</div>
      ) : (
        <div className="table-container">
          <table className="cases-table">
            <thead>
              <tr>
                <th>Case ID</th>
                <th>Customer</th>
                <th>Amount</th>
                <th>Ageing</th>
                <th>Priority</th>
                <th>Status</th>
                <th>SLA Status</th>
                <th>AI Score</th>
                <th>DCA</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {cases.length === 0 ? (
                <tr>
                  <td colSpan={10} className="no-data">
                    No cases found
                  </td>
                </tr>
              ) : (
                cases.map((caseItem) => (
                  <tr key={caseItem.id}>
                    <td>
                      <Link to={`/cases/${caseItem.id}`} className="case-link">
                        {caseItem.case_id}
                      </Link>
                    </td>
                    <td>{caseItem.customer_name}</td>
                    <td className="amount">{formatCurrency(caseItem.overdue_amount)}</td>
                    <td>{caseItem.ageing_days} days</td>
                    <td>
                      <span className={`badge ${getPriorityClass(caseItem.priority)}`}>
                        {caseItem.priority}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${getStatusClass(caseItem.status)}`}>
                        {caseItem.status}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${getSLAClass(caseItem.sla_status)}`}>
                        {caseItem.sla_status}
                      </span>
                    </td>
                    <td>
                      <span className="ai-score">
                        {(caseItem.ai_recovery_score * 100).toFixed(0)}%
                      </span>
                    </td>
                    <td>{caseItem.dca?.name || 'Unassigned'}</td>
                    <td>
                      <Link to={`/cases/${caseItem.id}`} className="btn-small">
                        View
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Cases;
