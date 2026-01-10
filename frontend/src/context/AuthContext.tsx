import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
  role: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isAdmin: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    // Check for existing session
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      
      // Verify token is still valid
      apiService.getCurrentUser().catch(() => {
        logout();
      });
    }
  }, []);

  const login = async (username: string, password: string) => {
    const response = await apiService.login(username, password);
    const { access_token } = response;

    setToken(access_token);
    localStorage.setItem('token', access_token);

    // Fetch user details
    const userDetails = await apiService.getCurrentUser();
    setUser(userDetails);
    localStorage.setItem('user', JSON.stringify(userDetails));
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const isAuthenticated = !!token && !!user;
  const isAdmin = user?.role === 'admin';

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated, isAdmin }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
