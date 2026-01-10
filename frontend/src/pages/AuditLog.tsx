import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import './AuditLog.css';

interface AuditLog {
  id: number;
  user_id: number;
  case_id: number | null;
  action_type: string;
  description: string;
  old_value: string | null;
  new_value: string | null;
  timestamp: string;
}

const AuditLog: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    try {
      const data = await apiService.getAuditLogs();
      setLogs(data);
    } catch (err) {
      console.error('Failed to load audit logs:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  const getActionClass = (actionType: string) => {
    if (actionType.includes('CREATE')) return 'action-create';
    if (actionType.includes('UPDATE')) return 'action-update';
    if (actionType.includes('DELETE')) return 'action-delete';
    if (actionType.includes('ESCALATE')) return 'action-escalate';
    return '';
  };

  return (
    <div className="audit-log-page">
      <h1>Audit Log</h1>
      <p className="subtitle">
        Complete audit trail of all system actions. Every action is logged with timestamp, user, and
        details for compliance and tracking purposes.
      </p>

      {loading ? (
        <div className="loading">Loading audit logs...</div>
      ) : (
        <div className="table-container">
          <table className="audit-table">
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Action Type</th>
                <th>Description</th>
                <th>Case ID</th>
                <th>User ID</th>
                <th>Changes</th>
              </tr>
            </thead>
            <tbody>
              {logs.length === 0 ? (
                <tr>
                  <td colSpan={6} className="no-data">
                    No audit logs found
                  </td>
                </tr>
              ) : (
                logs.map((log) => (
                  <tr key={log.id}>
                    <td className="timestamp">{formatDate(log.timestamp)}</td>
                    <td>
                      <span className={`action-badge ${getActionClass(log.action_type)}`}>
                        {log.action_type}
                      </span>
                    </td>
                    <td>{log.description}</td>
                    <td>{log.case_id ? `#${log.case_id}` : '—'}</td>
                    <td>{log.user_id}</td>
                    <td className="changes">
                      {log.old_value && log.new_value ? (
                        <div className="change-detail">
                          <span className="old-value">{log.old_value}</span>
                          <span className="arrow">→</span>
                          <span className="new-value">{log.new_value}</span>
                        </div>
                      ) : log.new_value ? (
                        <span className="new-value">{log.new_value}</span>
                      ) : (
                        '—'
                      )}
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

export default AuditLog;
