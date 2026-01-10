import axios, { AxiosInstance } from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor to handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Unauthorized - clear token and redirect to login
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async login(username: string, password: string) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await this.client.post('/api/v1/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  }

  async register(userData: any) {
    const response = await this.client.post('/api/v1/auth/register', userData);
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.client.get('/api/v1/auth/me');
    return response.data;
  }

  // Dashboard
  async getDashboardStats() {
    const response = await this.client.get('/api/v1/dashboard');
    return response.data;
  }

  // Cases
  async getCases(params?: any) {
    const response = await this.client.get('/api/v1/cases/', { params });
    return response.data;
  }

  async getCase(caseId: number) {
    const response = await this.client.get(`/api/v1/cases/${caseId}`);
    return response.data;
  }

  async createCase(caseData: any) {
    const response = await this.client.post('/api/v1/cases/', caseData);
    return response.data;
  }

  async updateCaseStatus(caseId: number, status: string, notes?: string) {
    const response = await this.client.patch(`/api/v1/cases/${caseId}/status`, {
      status,
      notes,
    });
    return response.data;
  }

  async escalateCase(caseId: number, reason: string) {
    const response = await this.client.post(`/api/v1/cases/${caseId}/escalate`, {
      reason,
    });
    return response.data;
  }

  // DCAs
  async getDCAs(activeOnly = false) {
    const response = await this.client.get('/api/v1/dcas/', {
      params: { active_only: activeOnly },
    });
    return response.data;
  }

  async getDCA(dcaId: number) {
    const response = await this.client.get(`/api/v1/dcas/${dcaId}`);
    return response.data;
  }

  async createDCA(dcaData: any) {
    const response = await this.client.post('/api/v1/dcas/', dcaData);
    return response.data;
  }

  async updateDCA(dcaId: number, dcaData: any) {
    const response = await this.client.patch(`/api/v1/dcas/${dcaId}`, dcaData);
    return response.data;
  }

  async deleteDCA(dcaId: number) {
    const response = await this.client.delete(`/api/v1/dcas/${dcaId}`);
    return response.data;
  }

  // Audit Logs
  async getAuditLogs(caseId?: number) {
    const response = await this.client.get('/api/v1/audit-logs', {
      params: caseId ? { case_id: caseId } : {},
    });
    return response.data;
  }

  // Generic methods for flexibility
  async get(url: string, config?: any) {
    return await this.client.get(url, config);
  }

  async post(url: string, data?: any, config?: any) {
    return await this.client.post(url, data, config);
  }

  async patch(url: string, data?: any, config?: any) {
    return await this.client.patch(url, data, config);
  }

  async delete(url: string, config?: any) {
    return await this.client.delete(url, config);
  }
}

export const apiService = new ApiService();
