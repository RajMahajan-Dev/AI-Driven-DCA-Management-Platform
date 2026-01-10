import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar, Pie } from 'react-chartjs-2';
import './DCADetailModal.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

interface DCADetailModalProps {
  dca: any;
  onClose: () => void;
}

const DCADetailModal: React.FC<DCADetailModalProps> = ({ dca, onClose }) => {
  // Generate sample data for cases accepted over time (last 6 months)
  const casesOverTimeData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Cases Accepted',
        data: [5, 8, 12, 9, 15, 11],  // Sample data - in production, fetch from backend
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.4,
      },
    ],
  };

  // Monthly completion record
  const monthlyCompletionData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Completed Cases',
        data: [4, 7, 10, 8, 13, 9],  // Sample data
        backgroundColor: 'rgba(54, 162, 235, 0.8)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2,
      },
    ],
  };

  // Cases by amount range
  const casesByAmountData = {
    labels: ['$0-5K', '$5K-10K', '$10K-20K', '$20K+'],
    datasets: [
      {
        label: 'Cases by Amount',
        data: [15, 25, 35, 25],  // Sample percentages
        backgroundColor: [
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Cases Accepted Over Time',
        font: {
          size: 14,
          weight: 'bold' as const,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Monthly Completion Record',
        font: {
          size: 14,
          weight: 'bold' as const,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right' as const,
      },
      title: {
        display: true,
        text: 'Cases by Amount Range',
        font: {
          size: 14,
          weight: 'bold' as const,
        },
      },
    },
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content dca-detail-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{dca.name}</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          {/* DCA Information */}
          <div className="dca-info-section">
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Contact Person:</span>
                <span className="info-value">{dca.contact_person}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Email:</span>
                <span className="info-value">{dca.email}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Phone:</span>
                <span className="info-value">{dca.phone}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Capacity:</span>
                <span className="info-value">{dca.capacity} cases</span>
              </div>
              <div className="info-item">
                <span className="info-label">Debt Range:</span>
                <span className="info-value">
                  ${dca.min_debt_amount?.toLocaleString()} - ${dca.max_debt_amount?.toLocaleString()}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Performance Score:</span>
                <span className="info-value performance-score">{dca.performance_score}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Active Cases:</span>
                <span className="info-value">{dca.active_cases_count}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Total Completed:</span>
                <span className="info-value">{dca.total_cases_completed}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Avg Completion Time:</span>
                <span className="info-value">{dca.avg_completion_time_days?.toFixed(1)} days</span>
              </div>
              {dca.website_url && (
                <div className="info-item full-width">
                  <span className="info-label">Website:</span>
                  <a href={dca.website_url} target="_blank" rel="noopener noreferrer" className="info-link">
                    {dca.website_url}
                  </a>
                </div>
              )}
            </div>
          </div>

          {/* Charts Section */}
          <div className="charts-section">
            <div className="chart-row">
              <div className="chart-box">
                <Line data={casesOverTimeData} options={lineOptions} />
              </div>
              <div className="chart-box">
                <Bar data={monthlyCompletionData} options={barOptions} />
              </div>
            </div>
            <div className="chart-row single">
              <div className="chart-box">
                <Pie data={casesByAmountData} options={pieOptions} />
              </div>
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="performance-metrics">
            <h3>Performance Metrics</h3>
            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-value">{dca.total_cases_rejected || 0}</div>
                <div className="metric-label">Rejected Cases</div>
              </div>
              <div className="metric-card">
                <div className="metric-value">{dca.total_delays || 0}</div>
                <div className="metric-label">Delays Reported</div>
              </div>
              <div className="metric-card">
                <div className="metric-value">
                  {dca.total_cases_completed > 0 
                    ? ((dca.total_cases_completed / (dca.total_cases_completed + (dca.total_cases_rejected || 0))) * 100).toFixed(1)
                    : 0}%
                </div>
                <div className="metric-label">Success Rate</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DCADetailModal;
