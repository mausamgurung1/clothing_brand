import React, { useState } from 'react';
import ProductList from './components/ProductList';
import ProductForm from './components/ProductForm';
import './App.css';

function App() {
  const [showForm, setShowForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);

  const handleCreate = () => {
    setEditingProduct(null);
    setShowForm(true);
  };

  const handleEdit = (product) => {
    setEditingProduct(product);
    setShowForm(true);
  };

  const handleFormSuccess = () => {
    setShowForm(false);
    setEditingProduct(null);
    window.location.reload();
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingProduct(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Clothing Store Admin</h1>
        {!showForm && (
          <button onClick={handleCreate} className="btn-create">
            + Create New Product
          </button>
        )}
      </header>

      <main className="app-main">
        {showForm ? (
          <ProductForm
            product={editingProduct}
            onSuccess={handleFormSuccess}
            onCancel={handleCancel}
          />
        ) : (
          <ProductList
            onEdit={handleEdit}
            onDelete={() => {}}
          />
        )}
      </main>
    </div>
  );
}

export default App;

