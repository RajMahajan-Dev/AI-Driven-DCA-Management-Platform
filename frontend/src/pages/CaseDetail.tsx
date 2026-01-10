import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';
import './CaseDetail.css';

interface CaseDetail {
  id: number;
  case_id: string;
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  overdue_amount: number;
  ageing_days: number;
  status: string;
  priority: string;
  sla_status: string;
  sla_due_date: string;
  ai_recovery_score: number;
  dca: { id: number; name: string } | null;
  allocation_reason: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

const CaseDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [caseData, setCaseData] = useState<CaseDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [escalateReason, setEscalateReason] = useState('');
  const [showEscalate, setShowEscalate] = useState(false);

  useEffect(() => {
    if (id) {
      loadCase();
    }
  }, [id]);

  const loadCase = async () => {
    try {
      const data = await apiService.getCase(Number(id));
      setCaseData(data);
    } catch (err) {
      console.error('Failed to load case:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (newStatus: string) => {
    if (!caseData) return;
    setUpdating(true);
    try {
      await apiService.updateCaseStatus(caseData.id, newStatus);
      await loadCase();
      alert('Status updated successfully');
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to update status');
    } finally {
      setUpdating(false);
    }
  };

  const handleEscalate = async () => {
    if (!caseData || !escalateReason.trim()) return;
    setUpdating(true);
    try {
      await apiService.escalateCase(caseData.id, escalateReason);
      setEscalateReason('');
      setShowEscalate(false);
      alert('Case escalated successfully');
      await loadCase();
    } catch (err: any) {
      alert('Failed to escalate case');
    } finally {
      setUpdating(false);
    }
  };

  const downloadCasePDF = async () => {
    if (!caseData) return;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/reports/case/${caseData.id}/pdf`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) throw new Error('Failed to download PDF');
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `case_${caseData.case_id}_report.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Failed to download PDF:', err);
      alert('Failed to download PDF report');
    }
  };

  if (loading) return <div className="loading">Loading case details...</div>;
  if (!caseData) return <div className="error">Case not found</div>;

  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);

  const formatDate = (dateString: string) =>
    new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });

  return (
    <div className="case-detail-page">
      <button onClick={() => navigate('/cases')} className="btn-back">
        ← Back to Cases
      </button>

      <div className="case-header">
        <div>
          <h1>{caseData.case_id}</h1>
          <p className="customer-name">{caseData.customer_name}</p>
        </div>
        <div className="case-actions-header">
          <button onClick={downloadCasePDF} className="btn-download-pdf">
            📄 Download PDF
          </button>
          <div className="case-badges">
            <span className={`badge priority-${caseData.priority.toLowerCase()}`}>
              {caseData.priority}
            </span>
            <span className={`badge status-${caseData.status.toLowerCase().replace(' ', '-')}`}>
              {caseData.status}
            </span>
            <span className={`badge sla-${caseData.sla_status.toLowerCase().replace(' ', '-')}`}>
              {caseData.sla_status}
            </span>
          </div>
        </div>
      </div>

      <div className="case-content">
        <div className="case-section">
          <h2>Case Information</h2>
          <div className="info-grid">
            <div className="info-item">
              <label>Overdue Amount</label>
              <div className="value highlight">{formatCurrency(caseData.overdue_amount)}</div>
            </div>
            <div className="info-item">
              <label>Ageing Days</label>
              <div className="value">{caseData.ageing_days} days</div>
            </div>
            <div className="info-item">
              <label>AI Recovery Score</label>
              <div className="value ai-score">
                {(caseData.ai_recovery_score * 100).toFixed(1)}%
              </div>
            </div>
            <div className="info-item">
              <label>SLA Due Date</label>
              <div className="value">{formatDate(caseData.sla_due_date)}</div>
            </div>
          </div>
        </div>

        <div className="case-section">
          <h2>Customer Details</h2>
          <div className="info-grid">
            <div className="info-item">
              <label>Email</label>
              <div className="value">{caseData.customer_email || 'N/A'}</div>
            </div>
            <div className="info-item">
              <label>Phone</label>
              <div className="value">{caseData.customer_phone || 'N/A'}</div>
            </div>
          </div>
        </div>

        <div className="case-section">
          <h2>DCA Assignment</h2>
          <div className="info-grid">
            <div className="info-item">
              <label>Assigned DCA</label>
              <div className="value">{caseData.dca?.name || 'Unassigned'}</div>
            </div>
            <div className="info-item">
              <label>Allocation Reason</label>
              <div className="value small">{caseData.allocation_reason || 'N/A'}</div>
            </div>
          </div>
        </div>

        {caseData.notes && (
          <div className="case-section">
            <h2>Notes</h2>
            <div className="notes">{caseData.notes}</div>
          </div>
        )}

        <div className="case-section">
          <h2>Actions</h2>
          <div className="action-buttons">
            {caseData.status === 'Open' && (
              <button
                onClick={() => handleStatusChange('In Progress')}
                className="btn-action"
                disabled={updating}
              >
                Move to In Progress
              </button>
            )}
            {caseData.status === 'In Progress' && (
              <button
                onClick={() => handleStatusChange('Closed')}
                className="btn-action success"
                disabled={updating}
              >
                Close Case
              </button>
            )}
            {caseData.status !== 'Closed' && (
              <button
                onClick={() => setShowEscalate(!showEscalate)}
                className="btn-action warning"
                disabled={updating}
              >
                Escalate Case
              </button>
            )}
          </div>

          {showEscalate && (
            <div className="escalate-form">
              <textarea
                value={escalateReason}
                onChange={(e) => setEscalateReason(e.target.value)}
                placeholder="Enter escalation reason..."
                rows={4}
              />
              <div className="escalate-actions">
                <button onClick={handleEscalate} className="btn-primary" disabled={updating}>
                  Submit Escalation
                </button>
                <button onClick={() => setShowEscalate(false)} className="btn-secondary">
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="case-meta">
          <small>Created: {formatDate(caseData.created_at)}</small>
          {caseData.updated_at && <small>Updated: {formatDate(caseData.updated_at)}</small>}
        </div>
      </div>
    </div>
  );
};

export default CaseDetail;
