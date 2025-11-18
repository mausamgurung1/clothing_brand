/**
 * Export Data Component - Export products, categories, etc.
 * 
 * Copyright (c) 2024 Baabuu Clothing
 * Licensed under MIT License
 */

import React, { useState } from 'react';
import { productsAPI, categoriesAPI } from '../../services/api';
import './ExportData.css';

const ExportData = () => {
  const [exportType, setExportType] = useState('products');
  const [format, setFormat] = useState('json');
  const [exporting, setExporting] = useState(false);

  const handleExport = async () => {
    setExporting(true);
    try {
      let data = [];
      let filename = '';

      if (exportType === 'products') {
        const response = await productsAPI.getAll({ page_size: 10000 });
        data = response.data.results || [];
        filename = `products_export_${new Date().toISOString().split('T')[0]}`;
      } else if (exportType === 'categories') {
        const response = await categoriesAPI.getAll();
        data = response.data || [];
        filename = `categories_export_${new Date().toISOString().split('T')[0]}`;
      }

      if (format === 'json') {
        const jsonStr = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${filename}.json`;
        a.click();
        URL.revokeObjectURL(url);
      } else if (format === 'csv') {
        // Convert to CSV
        if (data.length === 0) {
          alert('No data to export');
          return;
        }

        const headers = Object.keys(data[0]);
        const csvRows = [
          headers.join(','),
          ...data.map(row =>
            headers.map(header => {
              const value = row[header];
              return typeof value === 'object' ? JSON.stringify(value) : value;
            }).join(',')
          )
        ];
        const csvStr = csvRows.join('\n');
        const blob = new Blob([csvStr], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${filename}.csv`;
        a.click();
        URL.revokeObjectURL(url);
      }

      alert('Export completed successfully!');
    } catch (error) {
      console.error('Export error:', error);
      alert('Error exporting data');
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="export-data">
      <div className="export-header">
        <h1>Export Data</h1>
        <p>Export your store data in various formats</p>
      </div>

      <div className="export-form">
        <div className="form-group">
          <label>Export Type</label>
          <select
            value={exportType}
            onChange={(e) => setExportType(e.target.value)}
            className="form-select"
          >
            <option value="products">Products</option>
            <option value="categories">Categories</option>
          </select>
        </div>

        <div className="form-group">
          <label>Export Format</label>
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value)}
            className="form-select"
          >
            <option value="json">JSON</option>
            <option value="csv">CSV</option>
          </select>
        </div>

        <button
          onClick={handleExport}
          disabled={exporting}
          className="btn-export"
        >
          {exporting ? 'Exporting...' : 'Export Data'}
        </button>
      </div>

      <div className="export-info">
        <h3>Export Information</h3>
        <ul>
          <li><strong>JSON Format:</strong> Complete data with all fields, best for backups</li>
          <li><strong>CSV Format:</strong> Spreadsheet-friendly format, best for analysis</li>
          <li>Exports include all available data for the selected type</li>
          <li>Files are downloaded automatically to your default download folder</li>
        </ul>
      </div>
    </div>
  );
};

export default ExportData;

