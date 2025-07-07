import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus } from 'lucide-react';

const initialState = {
  name: '',
  description: '',
  price: '',
  sku: '',
  category: '',
  images: [{ url: '', is_primary: true }],
};

const SellerProductCreatePage: React.FC = () => {
  const [form, setForm] = useState(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setForm(f => ({ ...f, [name]: value }));
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm(f => ({
      ...f,
      images: [{ url: e.target.value, is_primary: true }]
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const token = localStorage.getItem('sellerToken');
      const response = await fetch('http://localhost:8005/api/sellers/products/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...form,
          price: parseFloat(form.price),
          images: form.images,
          category: form.category,
        }),
      });
      if (!response.ok) {
        const data = await response.json();
        setError(data.error || 'Erreur lors de la création du produit');
        setLoading(false);
        return;
      }
      setSuccess('Produit créé avec succès !');
      setTimeout(() => navigate('/seller/products'), 1200);
    } catch (err) {
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow p-8">
        <div className="flex items-center mb-6">
          <Plus className="h-7 w-7 text-amazon-orange mr-2" />
          <h1 className="text-2xl font-bold text-gray-900">Ajouter un produit</h1>
        </div>
        {error && <div className="mb-4 text-red-600 bg-red-50 border border-red-200 rounded p-2">{error}</div>}
        {success && <div className="mb-4 text-green-600 bg-green-50 border border-green-200 rounded p-2">{success}</div>}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="form-label">Nom du produit *</label>
            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              className="form-input"
              required
            />
          </div>
          <div>
            <label className="form-label">Description *</label>
            <textarea
              name="description"
              value={form.description}
              onChange={handleChange}
              className="form-input"
              rows={3}
              required
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="form-label">Prix (€) *</label>
              <input
                name="price"
                type="number"
                min="0"
                step="0.01"
                value={form.price}
                onChange={handleChange}
                className="form-input"
                required
              />
            </div>
            <div>
              <label className="form-label">SKU *</label>
              <input
                name="sku"
                value={form.sku}
                onChange={handleChange}
                className="form-input"
                required
              />
            </div>
          </div>
          <div>
            <label className="form-label">Catégorie *</label>
            <input
              name="category"
              value={form.category}
              onChange={handleChange}
              className="form-input"
              placeholder="ID ou nom de la catégorie"
              required
            />
          </div>
          <div>
            <label className="form-label">Image principale (URL)</label>
            <input
              name="image_url"
              value={form.images[0].url}
              onChange={handleImageChange}
              className="form-input"
              placeholder="https://..."
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary w-full"
          >
            {loading ? 'Création...' : 'Créer le produit'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default SellerProductCreatePage;
