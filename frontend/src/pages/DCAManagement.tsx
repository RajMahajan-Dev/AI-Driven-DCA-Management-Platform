import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import { useAuth } from '../context/AuthContext';
import DCADetailModal from '../components/DCADetailModal';
import './DCAManagement.css';

interface DCA {
  id: number;
  name: string;
  contact_person: string;
  email: string;
  phone: string;
  performance_score: number | string;  // Can be number or "TBD"
  active_cases_count: number;
  max_capacity: number;
  is_active: boolean;
}

const DCAManagement: React.FC = () => {
  const { isAdmin } = useAuth();
  const [dcas, setDcas] = useState<DCA[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [selectedDCA, setSelectedDCA] = useState<DCA | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    contact_person: '',
    email: '',
    phone: '',
    max_capacity: '100',
    min_debt_amount: '',
    max_debt_amount: '',
    website_url: '',
  });

  useEffect(() => {
    loadDCAs();
  }, []);

  const loadDCAs = async () => {
    try {
      const data = await apiService.getDCAs();
      setDcas(data);
    } catch (err) {
      console.error('Failed to load DCAs:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiService.createDCA({
        name: formData.name,
        contact_person: formData.contact_person,
        email: formData.email,
        phone: formData.phone,
        max_capacity: parseInt(formData.max_capacity),
        min_debt_amount: parseFloat(formData.min_debt_amount) || 0,
        max_debt_amount: parseFloat(formData.max_debt_amount) || 1000000,
        website_url: formData.website_url,
        performance_score: 'TBD',
      });
      setShowCreate(false);
      setFormData({
        name: '',
        contact_person: '',
        email: '',
        phone: '',
        max_capacity: '100',
        min_debt_amount: '',
        max_debt_amount: '',
        website_url: '',
      });
      loadDCAs();
      alert('DCA created successfully');
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to create DCA');
    }
  };

  const handleToggleActive = async (dcaId: number, isActive: boolean) => {
    try {
      await apiService.updateDCA(dcaId, { is_active: !isActive });
      loadDCAs();
    } catch (err) {
      alert('Failed to update DCA status');
    }
  };

  if (loading) return <div className="loading">Loading DCAs...</div>;

  return (
    <div className="dca-management-page">
      <div className="page-header">
        <h1>DCA Management</h1>
        {isAdmin && (
          <button onClick={() => setShowCreate(!showCreate)} className="btn-primary">
            {showCreate ? 'Cancel' : 'Add New DCA'}
          </button>
        )}
      </div>

      {showCreate && isAdmin && (
        <div className="create-dca-form">
          <h2>Create New DCA</h2>
          <form onSubmit={handleCreate}>
            <div className="form-row">
              <div className="form-group">
                <label>DCA Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                  placeholder="Premium Recovery Services"
                />
              </div>
              <div className="form-group">
                <label>Contact Person</label>
                <input
                  type="text"
                  value={formData.contact_person}
                  onChange={(e) =>
                    setFormData({ ...formData, contact_person: e.target.value })
                  }
                  placeholder="John Smith"
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  placeholder="contact@dca.com"
                />
              </div>
              <div className="form-group">
                <label>Phone</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  placeholder="+1-555-0100"
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Max Capacity *</label>
                <input
                  type="number"
                  min="1"
                  value={formData.max_capacity}
                  onChange={(e) =>
                    setFormData({ ...formData, max_capacity: e.target.value })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label>Website URL</label>
                <input
                  type="url"
                  value={formData.website_url}
                  onChange={(e) =>
                    setFormData({ ...formData, website_url: e.target.value })
                  }
                  placeholder="https://dca-website.com"
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Min Debt Amount ($)</label>
                <input
                  type="number"
                  min="0"
                  step="1000"
                  value={formData.min_debt_amount}
                  onChange={(e) =>
                    setFormData({ ...formData, min_debt_amount: e.target.value })
                  }
                  placeholder="1000"
                />
              </div>
              <div className="form-group">
                <label>Max Debt Amount ($)</label>
                <input
                  type="number"
                  min="0"
                  step="1000"
                  value={formData.max_debt_amount}
                  onChange={(e) =>
                    setFormData({ ...formData, max_debt_amount: e.target.value })
                  }
                  placeholder="1000000"
                />
              </div>
            </div>
            <p className="form-note">* Performance score will be calculated automatically based on case completion stats</p>
            <button type="submit" className="btn-primary">
              Create DCA
            </button>
          </form>
        </div>
      )}

      <div className="dca-grid">
        {dcas.map((dca) => (
          <div 
            key={dca.id} 
            className={`dca-card ${!dca.is_active ? 'inactive' : ''}`}
            onClick={() => setSelectedDCA(dca)}
            style={{ cursor: 'pointer' }}
          >
            <div className="dca-header">
              <h3>{dca.name}</h3>
              {!dca.is_active && <span className="inactive-badge">Inactive</span>}
            </div>
            <div className="dca-info">
              <div className="info-row">
                <span className="label">Contact:</span>
                <span>{dca.contact_person || 'N/A'}</span>
              </div>
              <div className="info-row">
                <span className="label">Email:</span>
                <span>{dca.email || 'N/A'}</span>
              </div>
              <div className="info-row">
                <span className="label">Phone:</span>
                <span>{dca.phone || 'N/A'}</span>
              </div>
              <div className="info-row">
                <span className="label">Performance:</span>
                <span className="score">
                  {typeof dca.performance_score === 'number' 
                    ? `${dca.performance_score.toFixed(1)}%` 
                    : dca.performance_score}
                </span>
              </div>
              <div className="info-row">
                <span className="label">Capacity:</span>
                <span>
                  {dca.active_cases_count} / {dca.max_capacity}
                </span>
              </div>
            </div>
            {isAdmin && (
              <div className="dca-actions">
                <button
                  onClick={() => handleToggleActive(dca.id, dca.is_active)}
                  className={`btn-toggle ${dca.is_active ? 'active' : 'inactive'}`}
                >
                  {dca.is_active ? 'Deactivate' : 'Activate'}
                </button>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* DCA Detail Modal */}
      {selectedDCA && (
        <DCADetailModal
          dca={selectedDCA}
          onClose={() => setSelectedDCA(null)}
        />
      )}
    </div>
  );
};

export default DCAManagement;
