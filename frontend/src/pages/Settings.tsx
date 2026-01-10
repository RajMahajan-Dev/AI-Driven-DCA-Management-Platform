import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Settings.css';

interface SettingsData {
  // SLA Parameters
  p1_sla_days: number;
  p2_sla_days: number;
  p3_sla_days: number;
  
  // Performance Parameters
  delay_penalty_percent: number;
  breach_penalty_percent: number;
  processing_threshold_days: number;
  processing_penalty_per_day: number;
  rejection_penalty_percent: number;
  
  // Theme
  theme_primary_color: string;
  theme_secondary_color: string;
  theme_mode: string;
  
  // Time
  timezone: string;
  date_format: string;
  time_format: string;
  
  // Features
  ai_assignment_enabled: boolean;
  email_notifications_enabled: boolean;
  sms_notifications_enabled: boolean;
}

const Settings: React.FC = () => {
  const [settings, setSettings] = useState<SettingsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/v1/settings', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSettings(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching settings:', error);
      setMessage({ type: 'error', text: 'Failed to load settings' });
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!settings) return;
    
    setSaving(true);
    setMessage(null);
    
    try {
      const token = localStorage.getItem('token');
      await axios.put('http://localhost:8000/api/v1/settings', settings, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessage({ type: 'success', text: 'Settings saved successfully!' });
    } catch (error) {
      console.error('Error saving settings:', error);
      setMessage({ type: 'error', text: 'Failed to save settings' });
    } finally {
      setSaving(false);
    }
  };

  const handleReset = async () => {
    if (!window.confirm('Are you sure you want to reset all settings to defaults?')) {
      return;
    }
    
    setSaving(true);
    setMessage(null);
    
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('http://localhost:8000/api/v1/settings/reset', {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSettings(response.data.settings);
      setMessage({ type: 'success', text: 'Settings reset to defaults!' });
    } catch (error) {
      console.error('Error resetting settings:', error);
      setMessage({ type: 'error', text: 'Failed to reset settings' });
    } finally {
      setSaving(false);
    }
  };

  const updateSetting = (field: keyof SettingsData, value: any) => {
    if (settings) {
      setSettings({ ...settings, [field]: value });
    }
  };

  if (loading) {
    return <div className="settings-container"><div className="loading">Loading settings...</div></div>;
  }

  if (!settings) {
    return <div className="settings-container"><div className="error">Failed to load settings</div></div>;
  }

  return (
    <div className="settings-container">
      <div className="page-header">
        <h1>⚙️ Platform Settings</h1>
        <div className="header-actions">
          <button onClick={handleReset} className="btn-secondary" disabled={saving}>
            Reset to Defaults
          </button>
          <button onClick={handleSave} className="btn-primary" disabled={saving}>
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </div>

      {message && (
        <div className={`message message-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="settings-grid">
        {/* SLA Configuration */}
        <div className="settings-card">
          <h2>📅 SLA Configuration</h2>
          <div className="form-group">
            <label>P1 Priority SLA (days)</label>
            <input
              type="number"
              value={settings.p1_sla_days}
              onChange={(e) => updateSetting('p1_sla_days', parseInt(e.target.value))}
              min="1"
              max="30"
            />
            <small>Critical priority cases deadline</small>
          </div>
          
          <div className="form-group">
            <label>P2 Priority SLA (days)</label>
            <input
              type="number"
              value={settings.p2_sla_days}
              onChange={(e) => updateSetting('p2_sla_days', parseInt(e.target.value))}
              min="1"
              max="30"
            />
            <small>High priority cases deadline</small>
          </div>
          
          <div className="form-group">
            <label>P3 Priority SLA (days)</label>
            <input
              type="number"
              value={settings.p3_sla_days}
              onChange={(e) => updateSetting('p3_sla_days', parseInt(e.target.value))}
              min="1"
              max="30"
            />
            <small>Normal priority cases deadline</small>
          </div>
        </div>

        {/* Performance Score Parameters */}
        <div className="settings-card">
          <h2>📊 Performance Score Parameters</h2>
          <div className="form-group">
            <label>Processing Threshold (days)</label>
            <input
              type="number"
              value={settings.processing_threshold_days}
              onChange={(e) => updateSetting('processing_threshold_days', parseInt(e.target.value))}
              min="1"
              max="30"
            />
            <small>Days before penalty applies for slow processing</small>
          </div>
          
          <div className="form-group">
            <label>Processing Penalty (% per day)</label>
            <input
              type="number"
              step="0.1"
              value={settings.processing_penalty_per_day}
              onChange={(e) => updateSetting('processing_penalty_per_day', parseFloat(e.target.value))}
              min="0"
              max="10"
            />
            <small>Penalty for each day over threshold</small>
          </div>
          
          <div className="form-group">
            <label>Delay Penalty (%)</label>
            <input
              type="number"
              step="0.1"
              value={settings.delay_penalty_percent}
              onChange={(e) => updateSetting('delay_penalty_percent', parseFloat(e.target.value))}
              min="0"
              max="20"
            />
            <small>Penalty for each delay reported</small>
          </div>
          
          <div className="form-group">
            <label>Breach/At-Risk Penalty (%)</label>
            <input
              type="number"
              step="0.1"
              value={settings.breach_penalty_percent}
              onChange={(e) => updateSetting('breach_penalty_percent', parseFloat(e.target.value))}
              min="0"
              max="20"
            />
            <small>Penalty for breached or at-risk cases</small>
          </div>
          
          <div className="form-group">
            <label>Rejection Penalty (%)</label>
            <input
              type="number"
              step="0.1"
              value={settings.rejection_penalty_percent}
              onChange={(e) => updateSetting('rejection_penalty_percent', parseFloat(e.target.value))}
              min="0"
              max="20"
            />
            <small>Penalty for each case rejection</small>
          </div>
        </div>

        {/* Theme Settings */}
        <div className="settings-card">
          <h2>🎨 Theme Settings</h2>
          <div className="form-group">
            <label>Primary Color</label>
            <div className="color-input-group">
              <input
                type="color"
                value={settings.theme_primary_color}
                onChange={(e) => updateSetting('theme_primary_color', e.target.value)}
              />
              <input
                type="text"
                value={settings.theme_primary_color}
                onChange={(e) => updateSetting('theme_primary_color', e.target.value)}
                placeholder="#6366f1"
              />
            </div>
          </div>
          
          <div className="form-group">
            <label>Secondary Color</label>
            <div className="color-input-group">
              <input
                type="color"
                value={settings.theme_secondary_color}
                onChange={(e) => updateSetting('theme_secondary_color', e.target.value)}
              />
              <input
                type="text"
                value={settings.theme_secondary_color}
                onChange={(e) => updateSetting('theme_secondary_color', e.target.value)}
                placeholder="#8b5cf6"
              />
            </div>
          </div>
          
          <div className="form-group">
            <label>Theme Mode</label>
            <select
              value={settings.theme_mode}
              onChange={(e) => updateSetting('theme_mode', e.target.value)}
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </div>
        </div>

        {/* Time & Format Settings */}
        <div className="settings-card">
          <h2>🕐 Time & Format Settings</h2>
          <div className="form-group">
            <label>Timezone</label>
            <select
              value={settings.timezone}
              onChange={(e) => updateSetting('timezone', e.target.value)}
            >
              <option value="UTC">UTC</option>
              <option value="America/New_York">Eastern Time</option>
              <option value="America/Chicago">Central Time</option>
              <option value="America/Denver">Mountain Time</option>
              <option value="America/Los_Angeles">Pacific Time</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Date Format</label>
            <select
              value={settings.date_format}
              onChange={(e) => updateSetting('date_format', e.target.value)}
            >
              <option value="YYYY-MM-DD">YYYY-MM-DD</option>
              <option value="MM/DD/YYYY">MM/DD/YYYY</option>
              <option value="DD/MM/YYYY">DD/MM/YYYY</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Time Format</label>
            <select
              value={settings.time_format}
              onChange={(e) => updateSetting('time_format', e.target.value)}
            >
              <option value="24h">24-hour</option>
              <option value="12h">12-hour (AM/PM)</option>
            </select>
          </div>
        </div>

        {/* Feature Flags */}
        <div className="settings-card">
          <h2>🚀 Feature Flags</h2>
          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={settings.ai_assignment_enabled}
                onChange={(e) => updateSetting('ai_assignment_enabled', e.target.checked)}
              />
              <span>AI Auto-Assignment</span>
            </label>
            <small>Automatically assign cases to DCAs using AI</small>
          </div>
          
          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={settings.email_notifications_enabled}
                onChange={(e) => updateSetting('email_notifications_enabled', e.target.checked)}
              />
              <span>Email Notifications</span>
            </label>
            <small>Send email notifications for case updates</small>
          </div>
          
          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={settings.sms_notifications_enabled}
                onChange={(e) => updateSetting('sms_notifications_enabled', e.target.checked)}
              />
              <span>SMS Notifications</span>
            </label>
            <small>Send SMS notifications for urgent updates</small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
