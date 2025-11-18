/**
 * Admin Settings Page
 * 
 * Copyright (c) 2024 Baabuu Clothing
 * Licensed under MIT License
 */

import React, { useState } from 'react';
import './Settings.css';

const Settings = () => {
  const [settings, setSettings] = useState({
    siteName: 'Baabuu Clothing',
    siteDescription: 'Premium clothing store',
    email: 'admin@baabuuclothing.com',
    phone: '+1 234 567 8900',
    address: '123 Fashion Street, Style City',
    currency: 'USD',
    taxRate: 0.08,
    shippingCost: 5.99,
    freeShippingThreshold: 50,
    enableReviews: true,
    enableNewsletter: true,
    maintenanceMode: false,
  });

  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');

    // Simulate API call
    setTimeout(() => {
      setSaving(false);
      setMessage('Settings saved successfully!');
      setTimeout(() => setMessage(''), 3000);
    }, 1000);
  };

  return (
    <div className="settings-page">
      <div className="settings-header">
        <h1>Settings</h1>
        <p>Manage your store configuration</p>
      </div>

      {message && (
        <div className={`message ${message.includes('success') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="settings-form">
        <div className="settings-section">
          <h2>General Settings</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Site Name</label>
              <input
                type="text"
                name="siteName"
                value={settings.siteName}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>Site Description</label>
              <textarea
                name="siteDescription"
                value={settings.siteDescription}
                onChange={handleChange}
                rows="3"
              />
            </div>
          </div>
        </div>

        <div className="settings-section">
          <h2>Contact Information</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={settings.email}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>Phone</label>
              <input
                type="tel"
                name="phone"
                value={settings.phone}
                onChange={handleChange}
              />
            </div>
            <div className="form-group full-width">
              <label>Address</label>
              <input
                type="text"
                name="address"
                value={settings.address}
                onChange={handleChange}
              />
            </div>
          </div>
        </div>

        <div className="settings-section">
          <h2>Store Settings</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Currency</label>
              <select
                name="currency"
                value={settings.currency}
                onChange={handleChange}
              >
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
                <option value="INR">INR (₹)</option>
              </select>
            </div>
            <div className="form-group">
              <label>Tax Rate (%)</label>
              <input
                type="number"
                name="taxRate"
                value={settings.taxRate}
                onChange={handleChange}
                step="0.01"
                min="0"
                max="1"
              />
            </div>
            <div className="form-group">
              <label>Shipping Cost ($)</label>
              <input
                type="number"
                name="shippingCost"
                value={settings.shippingCost}
                onChange={handleChange}
                step="0.01"
                min="0"
              />
            </div>
            <div className="form-group">
              <label>Free Shipping Threshold ($)</label>
              <input
                type="number"
                name="freeShippingThreshold"
                value={settings.freeShippingThreshold}
                onChange={handleChange}
                step="0.01"
                min="0"
              />
            </div>
          </div>
        </div>

        <div className="settings-section">
          <h2>Feature Toggles</h2>
          <div className="toggle-group">
            <label className="toggle-item">
              <input
                type="checkbox"
                name="enableReviews"
                checked={settings.enableReviews}
                onChange={handleChange}
              />
              <span>Enable Product Reviews</span>
            </label>
            <label className="toggle-item">
              <input
                type="checkbox"
                name="enableNewsletter"
                checked={settings.enableNewsletter}
                onChange={handleChange}
              />
              <span>Enable Newsletter Subscription</span>
            </label>
            <label className="toggle-item">
              <input
                type="checkbox"
                name="maintenanceMode"
                checked={settings.maintenanceMode}
                onChange={handleChange}
              />
              <span>Maintenance Mode</span>
            </label>
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-save" disabled={saving}>
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
          <button type="button" className="btn-reset" onClick={() => window.location.reload()}>
            Reset
          </button>
        </div>
      </form>
    </div>
  );
};

export default Settings;

