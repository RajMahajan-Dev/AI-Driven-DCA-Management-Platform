import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import DashboardCharts from '../components/DashboardCharts';
import './Dashboard.css';

interface DashboardStats {
  total_overdue_amount: number;
  total_cases: number;
  open_cases: number;
  in_progress_cases: number;
  closed_cases: number;
  sla_breach_count: number;
  at_risk_count: number;
  total_dcas: number;
  active_dcas: number;
  rejected_cases?: number;
  pending_cases?: number;
  pending_amount?: number;
  recovered_amount?: number;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await apiService.getDashboardStats();
      setStats(data);
    } catch (err: any) {
      setError('Failed to load dashboard statistics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!stats) return null;

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      <div className="stats-grid">
        <div className="stat-card highlight">
          <div className="stat-value">{formatCurrency(stats.total_overdue_amount)}</div>
          <div className="stat-label">Total Overdue Amount</div>
        </div>

        <div className="stat-card">
          <div className="stat-value">{stats.total_cases}</div>
          <div className="stat-label">Total Cases</div>
        </div>

        <div className="stat-card warning">
          <div className="stat-value">{stats.sla_breach_count}</div>
          <div className="stat-label">SLA Breaches</div>
        </div>

        <div className="stat-card alert">
          <div className="stat-value">{stats.at_risk_count}</div>
          <div className="stat-label">At Risk</div>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{stats.open_cases}</div>
          <div className="stat-label">Open Cases</div>
          <div className="stat-detail">Newly created</div>
        </div>

        <div className="stat-card">
          <div className="stat-value">{stats.in_progress_cases}</div>
          <div className="stat-label">In Progress</div>
          <div className="stat-detail">Being processed</div>
        </div>

        <div className="stat-card success">
          <div className="stat-value">{stats.closed_cases}</div>
          <div className="stat-label">Closed Cases</div>
          <div className="stat-detail">Resolved</div>
        </div>

        <div className="stat-card">
          <div className="stat-value">{stats.active_dcas}/{stats.total_dcas}</div>
          <div className="stat-label">Active DCAs</div>
          <div className="stat-detail">Collection agencies</div>
        </div>
      </div>

      {/* Analytics Charts */}
      <DashboardCharts
        caseStats={{
          pending: stats.pending_cases || (stats.open_cases + stats.in_progress_cases),
          completed: stats.closed_cases,
          rejected: stats.rejected_cases || 0,
        }}
        amountStats={{
          pendingAmount: stats.pending_amount || 0,
          recoveredAmount: stats.recovered_amount || 0,
        }}
      />

      <div className="dashboard-info">
        <div className="info-card">
          <h3>System Overview</h3>
          <p>The dashboard provides real-time insights into case management, SLA tracking, and DCA performance.</p>
          <ul>
            <li>AI-powered recovery probability scoring</li>
            <li>Automated case prioritization (P1/P2/P3)</li>
            <li>Rule-based DCA allocation</li>
            <li>Real-time SLA monitoring</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
