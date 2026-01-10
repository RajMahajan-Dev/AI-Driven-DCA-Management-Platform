import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';
import './CreateCase.css';

const CreateCase: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [dcas, setDcas] = useState<any[]>([]);
  const [assignmentMode, setAssignmentMode] = useState<'ai' | 'manual'>('ai');
  const [formData, setFormData] = useState({
    customer_name: '',
    customer_email: '',
    customer_phone: '',
    overdue_amount: '',
    ageing_days: '',
    notes: '',
    dca_id: '',
  });

  useEffect(() => {
    loadDCAs();
  }, []);

  const loadDCAs = async () => {
    try {
      const response = await apiService.get('/api/v1/dcas/');
      setDcas(response.data.filter((dca: any) => dca.is_active));
    } catch (error) {
      console.error('Error loading DCAs:', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const caseData: any = {
        customer_name: formData.customer_name,
        customer_email: formData.customer_email || undefined,
        customer_phone: formData.customer_phone || undefined,
        overdue_amount: parseFloat(formData.overdue_amount),
        ageing_days: parseInt(formData.ageing_days),
        notes: formData.notes || undefined,
      };

      // Add manual DCA selection if chosen
      if (assignmentMode === 'manual' && formData.dca_id) {
        caseData.dca_id = parseInt(formData.dca_id);
      }

      const createdCase = await apiService.createCase(caseData);
      alert(`Case ${createdCase.case_id} created successfully!`);
      navigate(`/cases/${createdCase.id}`);
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to create case');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-case-page">
      <button onClick={() => navigate('/cases')} className="btn-back">
        ← Back to Cases
      </button>

      <div className="create-case-container">
        <h1>Create New Case</h1>
        <p className="subtitle">
          The system will automatically calculate priority, SLA, AI recovery score, and assign to
          the best DCA.
        </p>

        <form onSubmit={handleSubmit} className="create-form">
          <div className="form-group">
            <label htmlFor="customer_name">Customer Name *</label>
            <input
              id="customer_name"
              name="customer_name"
              type="text"
              value={formData.customer_name}
              onChange={handleChange}
              required
              placeholder="Enter customer name"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="customer_email">Customer Email</label>
              <input
                id="customer_email"
                name="customer_email"
                type="email"
                value={formData.customer_email}
                onChange={handleChange}
                placeholder="customer@example.com"
              />
            </div>

            <div className="form-group">
              <label htmlFor="customer_phone">Customer Phone</label>
              <input
                id="customer_phone"
                name="customer_phone"
                type="tel"
                value={formData.customer_phone}
                onChange={handleChange}
                placeholder="+1-555-0100"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="overdue_amount">Overdue Amount ($) *</label>
              <input
                id="overdue_amount"
                name="overdue_amount"
                type="number"
                step="0.01"
                min="0"
                value={formData.overdue_amount}
                onChange={handleChange}
                required
                placeholder="10000.00"
              />
              <small>Amount must be greater than 0</small>
            </div>

            <div className="form-group">
              <label htmlFor="ageing_days">Ageing Days *</label>
              <input
                id="ageing_days"
                name="ageing_days"
                type="number"
                min="0"
                value={formData.ageing_days}
                onChange={handleChange}
                required
                placeholder="45"
              />
              <small>Number of days the debt is overdue</small>
            </div>
          </div>

          <div className="form-group dca-assignment-section">
            <label className="section-label">DCA Assignment Method</label>
            <div className="assignment-mode-selector">
              <label className={`mode-option ${assignmentMode === 'ai' ? 'selected' : ''}`}>
                <input
                  type="radio"
                  name="assignmentMode"
                  value="ai"
                  checked={assignmentMode === 'ai'}
                  onChange={(e) => setAssignmentMode(e.target.value as 'ai' | 'manual')}
                />
                <div className="mode-content">
                  <span className="mode-icon">🤖</span>
                  <div>
                    <strong>AI Auto-Assign</strong>
                    <small>System selects best DCA based on performance & capacity</small>
                  </div>
                </div>
              </label>

              <label className={`mode-option ${assignmentMode === 'manual' ? 'selected' : ''}`}>
                <input
                  type="radio"
                  name="assignmentMode"
                  value="manual"
                  checked={assignmentMode === 'manual'}
                  onChange={(e) => setAssignmentMode(e.target.value as 'ai' | 'manual')}
                />
                <div className="mode-content">
                  <span className="mode-icon">👤</span>
                  <div>
                    <strong>Manual Selection</strong>
                    <small>Choose DCA manually from the list</small>
                  </div>
                </div>
              </label>
            </div>

            {assignmentMode === 'manual' && (
              <div className="manual-dca-select">
                <select
                  name="dca_id"
                  value={formData.dca_id}
                  onChange={(e) => setFormData({ ...formData, dca_id: e.target.value })}
                  required={assignmentMode === 'manual'}
                >
                  <option value="">-- Select a DCA --</option>
                  {dcas.map((dca) => (
                    <option key={dca.id} value={dca.id}>
                      {dca.name} - Score: {dca.performance_score} | Capacity: {dca.active_cases_count}/{dca.max_capacity}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="notes">Notes</label>
            <textarea
              id="notes"
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              rows={4}
              placeholder="Additional notes about this case..."
            />
          </div>

          <div className="ai-info">
            <h3>🤖 AI-Powered Processing</h3>
            <ul>
              <li><strong>Priority:</strong> Automatically calculated based on amount and ageing (P1/P2/P3)</li>
              <li><strong>SLA:</strong> Due date set according to priority (P1: 3 days, P2: 7 days, P3: 14 days)</li>
              <li><strong>AI Score:</strong> Recovery probability predicted using ML model</li>
              <li><strong>DCA Allocation:</strong> Best DCA assigned based on performance and capacity</li>
            </ul>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Creating Case...' : 'Create Case'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/cases')}
              className="btn-secondary"
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateCase;
