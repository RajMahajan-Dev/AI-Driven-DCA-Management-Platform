import React from 'react';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="app-footer">
      <div className="footer-content">
        <p>Created by <strong>Raj Mahajan</strong></p>
        <p className="footer-subtitle">FedEx SMART Hackathon - AI-Driven DCA Management Platform</p>
      </div>
    </footer>
  );
};

export default Footer;
