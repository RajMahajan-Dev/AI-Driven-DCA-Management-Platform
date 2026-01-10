import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      {/* Header */}
      <header className="landing-header">
        <div className="container">
          <div className="logo">
            <span className="logo-icon">📦</span>
            <span className="logo-text">FedEx DCA Management</span>
          </div>
          <nav className="nav-menu">
            <a href="#features">Features</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
          </nav>
          <div className="header-actions">
            <button onClick={() => navigate('/login')} className="btn-outline">
              Sign In
            </button>
            <button onClick={() => navigate('/login')} className="btn-primary">
              Get Started
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="container">
          <div className="hero-content">
            <div className="hero-text">
              <div className="badge">
                <span className="badge-icon">✨</span>
                <span>Use AI to manage debt collection efficiently</span>
              </div>
              <h1 className="hero-title">
                The fastest way to manage
                <br />
                <span className="gradient-text">debt collection</span>
              </h1>
              <p className="hero-description">
                Empower your debt collection agency with AI-powered case management,
                intelligent DCA assignment, and comprehensive performance analytics.
              </p>
              <div className="hero-buttons">
                <button onClick={() => navigate('/login')} className="btn-large btn-primary">
                  Start Free Trial
                </button>
                <button onClick={() => navigate('/customer-login')} className="btn-large btn-secondary">
                  Customer Portal
                </button>
              </div>
            </div>
            <div className="hero-visual">
              <div className="platform-preview">
                {/* Placeholder for platform screenshots */}
                <div className="preview-card preview-card-1">
                  <div className="card-header">
                    <div className="card-dots">
                      <span></span><span></span><span></span>
                    </div>
                    <span className="card-title">Case Dashboard</span>
                  </div>
                  <div className="card-content">
                    <div className="chart-placeholder"></div>
                  </div>
                </div>
                
                <div className="preview-card preview-card-2">
                  <div className="card-header">
                    <div className="card-dots">
                      <span></span><span></span><span></span>
                    </div>
                    <span className="card-title">Analytics</span>
                  </div>
                  <div className="card-content">
                    <div className="stats-placeholder">
                      <div className="stat-bar"></div>
                      <div className="stat-bar"></div>
                      <div className="stat-bar"></div>
                    </div>
                  </div>
                </div>
                
                <div className="preview-card preview-card-3">
                  <div className="card-header">
                    <div className="card-dots">
                      <span></span><span></span><span></span>
                    </div>
                    <span className="card-title">DCA Performance</span>
                  </div>
                  <div className="card-content">
                    <div className="performance-placeholder">
                      <div className="perf-circle"></div>
                      <div className="perf-details">
                        <div className="perf-line"></div>
                        <div className="perf-line"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section">
        <div className="container">
          <div className="section-header">
            <h2>Powerful Features for Modern Debt Collection</h2>
            <p>Everything you need to manage cases, DCAs, and recover outstanding debts efficiently</p>
          </div>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>AI-Powered Assignment</h3>
              <p>Intelligent case allocation to DCAs based on performance, capacity, and debt range</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Real-Time Analytics</h3>
              <p>Comprehensive dashboards with performance metrics, recovery rates, and SLA tracking</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Automated Workflows</h3>
              <p>Streamline case management with automated status updates and notifications</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">👥</div>
              <h3>DCA Management</h3>
              <p>Track and manage multiple debt collection agencies with performance scoring</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📄</div>
              <h3>PDF Reports</h3>
              <p>Generate comprehensive reports for individual cases or entire portfolios</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>SLA Monitoring</h3>
              <p>Never miss deadlines with automated SLA tracking and breach alerts</p>
            </div>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="stats-section">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-number">95%</div>
              <div className="stat-label">Recovery Rate</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">10K+</div>
              <div className="stat-label">Cases Managed</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">50+</div>
              <div className="stat-label">Active DCAs</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">24/7</div>
              <div className="stat-label">Support</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to transform your debt collection process?</h2>
            <p>Join hundreds of organizations already using our platform</p>
            <button onClick={() => navigate('/login')} className="btn-large btn-primary">
              Get Started Today
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <h4>Product</h4>
              <ul>
                <li><a href="#features">Features</a></li>
                <li><a href="#pricing">Pricing</a></li>
                <li><a href="#demo">Demo</a></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Company</h4>
              <ul>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
                <li><a href="#careers">Careers</a></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Legal</h4>
              <ul>
                <li><a href="#privacy">Privacy</a></li>
                <li><a href="#terms">Terms</a></li>
              </ul>
            </div>
            <div className="footer-section">
              <div className="footer-logo">
                <span className="logo-icon">📦</span>
                <span>FedEx DCA Management</span>
              </div>
              <p className="footer-tagline">
                Efficient debt collection management powered by AI
              </p>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2026 FedEx DCA Management. Created by Raj Mahajan. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
