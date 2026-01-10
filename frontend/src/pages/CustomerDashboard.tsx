import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './CustomerDashboard.css';

interface CaseDetails {
  id: number;
  case_id: string;
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  customer_address: string;
  overdue_amount: number;
  status: string;
  priority: string;
  ageing_days: number;
  sla_due_date: string;
  sla_status: string;
  dca_name: string;
  notes: string;
  created_at: string;
  customer_social_media_instagram?: string;
  customer_social_media_facebook?: string;
  customer_social_media_linkedin?: string;
}

const CustomerDashboard: React.FC = () => {
  const { caseId } = useParams<{ caseId: string }>();
  const navigate = useNavigate();
  const [caseDetails, setCaseDetails] = useState<CaseDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [showPayment, setShowPayment] = useState(false);
  const [showComplaint, setShowComplaint] = useState(false);
  const [showUpdate, setShowUpdate] = useState(false);
  
  const [complaint, setComplaint] = useState('');
  const [updateInfo, setUpdateInfo] = useState('');
  const [paymentAmount, setPaymentAmount] = useState('');

  useEffect(() => {
    loadCaseDetails();
  }, [caseId]);

  const loadCaseDetails = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/customer/dashboard/${caseId}`);
      if (!response.ok) throw new Error('Failed to load case');
      const data = await response.json();
      setCaseDetails(data);
      setPaymentAmount(data.overdue_amount.toString());
    } catch (error) {
      alert('Failed to load case details');
      navigate('/customer-login');
    } finally {
      setLoading(false);
    }
  };

  const handlePayment = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/api/v1/customer/payment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          case_id: parseInt(caseId!),
          amount: parseFloat(paymentAmount)
        })
      });
      if (response.ok) {
        alert('Payment request submitted successfully!');
        setShowPayment(false);
        loadCaseDetails();
      } else {
        alert('Payment submission failed');
      }
    } catch (error) {
      alert('Error submitting payment');
    }
  };

  const handleComplaint = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/api/v1/customer/complaint`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          case_id: parseInt(caseId!),
          complaint: complaint
        })
      });
      if (response.ok) {
        alert('Complaint registered successfully. Admin will review it.');
        setShowComplaint(false);
        setComplaint('');
      } else {
        alert('Failed to register complaint');
      }
    } catch (error) {
      alert('Error registering complaint');
    }
  };

  const handleUpdateRequest = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/api/v1/customer/update-request`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          case_id: parseInt(caseId!),
          update_info: updateInfo
        })
      });
      if (response.ok) {
        alert('Update request submitted. Admin will review and approve.');
        setShowUpdate(false);
        setUpdateInfo('');
      } else {
        alert('Failed to submit update request');
      }
    } catch (error) {
      alert('Error submitting update request');
    }
  };

  if (loading) return <div className="loading-screen">Loading your case details...</div>;
  if (!caseDetails) return <div className="error-screen">Case not found</div>;

  return (
    <div className="customer-dashboard">
      <div className="dashboard-header">
        <button onClick={() => navigate('/customer-login')} className="btn-back">
          ← Back to Cases
        </button>
        <h1>Case Dashboard</h1>
      </div>

      <div className="dashboard-grid">
        <div className="case-info-card">
          <h2>Case Information</h2>
          <div className="info-grid">
            <div className="info-item">
              <span className="label">Case ID:</span>
              <span className="value">{caseDetails.case_id}</span>
            </div>
            <div className="info-item">
              <span className="label">Status:</span>
              <span className={`value status-${caseDetails.status.toLowerCase()}`}>
                {caseDetails.status}
              </span>
            </div>
            <div className="info-item">
              <span className="label">Priority:</span>
              <span className={`value priority-${caseDetails.priority.toLowerCase()}`}>
                {caseDetails.priority}
              </span>
            </div>
            <div className="info-item">
              <span className="label">Outstanding Amount:</span>
              <span className="value amount">${caseDetails.overdue_amount.toLocaleString()}</span>
            </div>
            <div className="info-item">
              <span className="label">Days Overdue:</span>
              <span className="value">{caseDetails.ageing_days} days</span>
            </div>
            <div className="info-item">
              <span className="label">Assigned DCA:</span>
              <span className="value">{caseDetails.dca_name || 'Not assigned yet'}</span>
            </div>
            <div className="info-item">
              <span className="label">SLA Status:</span>
              <span className={`value sla-${caseDetails.sla_status.toLowerCase().replace('_', '-')}`}>
                {caseDetails.sla_status.replace('_', ' ')}
              </span>
            </div>
          </div>
        </div>

        <div className="actions-card">
          <h2>Available Actions</h2>
          <div className="action-buttons">
            <button onClick={() => setShowPayment(true)} className="action-btn pay">
              💳 Pay Now
            </button>
            <button onClick={() => setShowComplaint(true)} className="action-btn complaint">
              📢 Register Complaint
            </button>
            <button onClick={() => setShowUpdate(true)} className="action-btn update">
              ✏️ Update Information
            </button>
            <button className="action-btn grievance">
              ⚖️ File Grievance
            </button>
          </div>
        </div>

        {caseDetails.notes && (
          <div className="notes-card">
            <h2>Case Notes</h2>
            <p>{caseDetails.notes}</p>
          </div>
        )}
      </div>

      {/* Payment Modal */}
      {showPayment && (
        <div className="modal-overlay" onClick={() => setShowPayment(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Payment</h3>
            <form onSubmit={handlePayment}>
              <div className="form-group">
                <label>Amount to Pay ($)</label>
                <input
                  type="number"
                  value={paymentAmount}
                  onChange={(e) => setPaymentAmount(e.target.value)}
                  min="0"
                  step="0.01"
                  required
                />
              </div>
              <div className="modal-actions">
                <button type="submit" className="btn-primary">Submit Payment</button>
                <button type="button" onClick={() => setShowPayment(false)} className="btn-secondary">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Complaint Modal */}
      {showComplaint && (
        <div className="modal-overlay" onClick={() => setShowComplaint(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Register Complaint</h3>
            <form onSubmit={handleComplaint}>
              <div className="form-group">
                <label>Complaint Details</label>
                <textarea
                  value={complaint}
                  onChange={(e) => setComplaint(e.target.value)}
                  rows={5}
                  placeholder="Describe your complaint..."
                  required
                />
              </div>
              <div className="modal-actions">
                <button type="submit" className="btn-primary">Submit Complaint</button>
                <button type="button" onClick={() => setShowComplaint(false)} className="btn-secondary">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Update Info Modal */}
      {showUpdate && (
        <div className="modal-overlay" onClick={() => setShowUpdate(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Update Information</h3>
            <p className="modal-note">Admin will review your update request before applying changes.</p>
            <form onSubmit={handleUpdateRequest}>
              <div className="form-group">
                <label>Information to Update</label>
                <textarea
                  value={updateInfo}
                  onChange={(e) => setUpdateInfo(e.target.value)}
                  rows={5}
                  placeholder="Enter updated information (phone, address, etc.)..."
                  required
                />
              </div>
              <div className="modal-actions">
                <button type="submit" className="btn-primary">Submit Request</button>
                <button type="button" onClick={() => setShowUpdate(false)} className="btn-secondary">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="dashboard-footer">
        <p>For assistance, please contact your assigned DCA or FedEx support.</p>
      </div>
    </div>
  );
};

export default CustomerDashboard;
