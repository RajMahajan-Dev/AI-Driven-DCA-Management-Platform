import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Cases from './pages/Cases';
import CaseDetail from './pages/CaseDetail';
import CreateCase from './pages/CreateCase';
import DCAManagement from './pages/DCAManagement';
import AuditLog from './pages/AuditLog';
import DCATestingPage from './pages/DCATestingPage';
import CustomerLogin from './pages/CustomerLogin';
import CustomerDashboard from './pages/CustomerDashboard';
import Settings from './pages/Settings';
import LandingPage from './pages/LandingPage';
import './App.css';

const PrivateRoute: React.FC<{ children: React.ReactElement }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
};

const AppRoutes: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />} />
      <Route path="/customer-login" element={<CustomerLogin />} />
      <Route path="/customer/dashboard/:caseId" element={<CustomerDashboard />} />
      <Route
        path="/"
        element={
          <PrivateRoute>
            <Layout />
          </PrivateRoute>
        }
      >
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="cases" element={<Cases />} />
        <Route path="cases/create" element={<CreateCase />} />
        <Route path="cases/:id" element={<CaseDetail />} />
        <Route path="dcas" element={<DCAManagement />} />
        <Route path="audit-logs" element={<AuditLog />} />
        <Route path="testing" element={<DCATestingPage />} />
        <Route path="settings" element={<Settings />} />
      </Route>
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
