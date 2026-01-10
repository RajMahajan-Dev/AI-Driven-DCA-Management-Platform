import React from 'react';
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Pie, Bar, Line } from 'react-chartjs-2';
import './DashboardCharts.css';

// Register ChartJS components
ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface DashboardChartsProps {
  caseStats: {
    pending: number;
    completed: number;
    rejected: number;
  };
  amountStats: {
    pendingAmount: number;
    recoveredAmount: number;
  };
  monthlyTrends?: {
    labels: string[];
    debtData: number[];
    recoveryData: number[];
  };
}

const DashboardCharts: React.FC<DashboardChartsProps> = ({ 
  caseStats, 
  amountStats,
  monthlyTrends 
}) => {
  // Default monthly trends if not provided
  const defaultTrends = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    debtData: [120000, 150000, 180000, 210000, 190000, 220000],
    recoveryData: [80000, 100000, 130000, 160000, 150000, 180000],
  };
  
  const trends = monthlyTrends || defaultTrends;
  // Case Status Pie Chart Data
  const caseStatusData = {
    labels: ['Pending', 'Completed', 'Rejected'],
    datasets: [
      {
        label: 'Cases',
        data: [caseStats.pending, caseStats.completed, caseStats.rejected],
        backgroundColor: [
          'rgba(255, 206, 86, 0.8)', // Yellow for Pending
          'rgba(75, 192, 192, 0.8)',  // Green for Completed
          'rgba(255, 99, 132, 0.8)',  // Red for Rejected
        ],
        borderColor: [
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(255, 99, 132, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  // Amount Recovery Bar Chart Data
  const amountRecoveryData = {
    labels: ['Pending Amount', 'Recovered Amount'],
    datasets: [
      {
        label: 'Amount ($)',
        data: [amountStats.pendingAmount, amountStats.recoveredAmount],
        backgroundColor: [
          'rgba(255, 159, 64, 0.8)',  // Orange for Pending
          'rgba(54, 162, 235, 0.8)',  // Blue for Recovered
        ],
        borderColor: [
          'rgba(255, 159, 64, 1)',
          'rgba(54, 162, 235, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  // Chart Options
  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          padding: 15,
          font: {
            size: 12,
          },
        },
      },
      title: {
        display: true,
        text: 'Case Status Distribution',
        font: {
          size: 16,
          weight: 'bold' as const,
        },
        padding: {
          top: 10,
          bottom: 20,
        },
      },
    },
    animation: {
      animateRotate: true,
      animateScale: true,
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
        text: 'Pending vs Recovered Amount',
        font: {
          size: 16,
          weight: 'bold' as const,
        },
        padding: {
          top: 10,
          bottom: 20,
        },
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
              }).format(context.parsed.y);
            }
            return label;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value: any) {
            return '$' + value.toLocaleString();
          }
        }
      }
    },
    animation: {
      duration: 1000,
      easing: 'easeInOutQuart' as const,
    },
  };

  // Debt vs Recovery Line Chart Data
  const debtRecoveryLineData = {
    labels: trends.labels,
    datasets: [
      {
        label: 'Total Debt',
        data: trends.debtData,
        borderColor: 'rgba(239, 68, 68, 1)', // Red
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        fill: true,
        tension: 0.4,
        borderWidth: 3,
        pointRadius: 5,
        pointBackgroundColor: 'rgba(239, 68, 68, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointHoverRadius: 7,
      },
      {
        label: 'Recovery',
        data: trends.recoveryData,
        borderColor: 'rgba(34, 197, 94, 1)', // Green
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        fill: true,
        tension: 0.4,
        borderWidth: 3,
        pointRadius: 5,
        pointBackgroundColor: 'rgba(34, 197, 94, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointHoverRadius: 7,
      },
    ],
  };

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          padding: 15,
          font: {
            size: 13,
            weight: 'bold' as const,
          },
          usePointStyle: true,
        },
      },
      title: {
        display: true,
        text: 'Debt vs Recovery Trend',
        font: {
          size: 18,
          weight: 'bold' as const,
        },
        padding: {
          top: 10,
          bottom: 20,
        },
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
              }).format(context.parsed.y);
            }
            return label;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value: any) {
            return '$' + (value / 1000) + 'K';
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        }
      },
      x: {
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        }
      }
    },
    animation: {
      duration: 1500,
      easing: 'easeInOutCubic' as const,
      delay: (context: any) => {
        let delay = 0;
        if (context.type === 'data' && context.mode === 'default') {
          delay = context.dataIndex * 100;
        }
        return delay;
      },
    },
  };

  return (
    <div className="dashboard-charts">
      {/* Debt vs Recovery Line Chart - Full Width */}
      <div className="chart-container chart-full-width">
        <div className="chart-card">
          <Line data={debtRecoveryLineData} options={lineOptions} />
        </div>
      </div>
      
      {/* Existing Charts */}
      <div className="chart-container">
        <div className="chart-card">
          <Pie data={caseStatusData} options={pieOptions} />
        </div>
      </div>
      <div className="chart-container">
        <div className="chart-card">
          <Bar data={amountRecoveryData} options={barOptions} />
        </div>
      </div>
    </div>
  );
};

export default DashboardCharts;
