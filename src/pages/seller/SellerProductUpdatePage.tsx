import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Edit } from 'lucide-react';

const SellerProductUpdatePage: React.FC = () => {
  const { productId } = useParams<{ productId: string }>();
  const [form, setForm] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProduct = async () => {
      setLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem('sellerToken');
        const response = await fetch(`http://localhost:8005/api/sellers/products/${productId}/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!response.ok) {
          setError('Produit introuvable');
          setForm(null);
          return;
        }
        const data = await response.json();
        setForm({
          name: data.name,
          description: data.description,
          price: data.price,
          sku: data.sku,
          category: data.category,
          images: data.images && data.images.length ? data.images : [{ url: '', is_primary: true }],
        });
      } catch {
        setError('Erreur lors du chargement du produit');
        setForm(null);
      } finally {
        setLoading(false);
      }
    };
    if (productId) fetchProduct();
  }, [productId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setForm((f: any) => ({ ...f, [name]: value }));
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((f: any) => ({
      ...f,
      images: [{ url: e.target.value, is_primary: true }]
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      const token = localStorage.getItem('sellerToken');
      const response = await fetch(`http://localhost:8005/api/sellers/products/${productId}/update/`, {
        method: 'PUT',
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
        setError(data.error || 'Erreur lors de la mise à jour');
        setSaving(false);
        return;
      }
      setSuccess('Produit mis à jour !');
      setTimeout(() => navigate(`/seller/products/${productId}`), 1200);
    } catch {
      setError('Erreur de connexion au serveur');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="min-h-screen bg-gray-50 flex items-center justify-center">Chargement...</div>;
  if (error) return <div className="min-h-screen bg-gray-50 flex items-center justify-center text-red-500">{error}</div>;
  if (!form) return <div className="min-h-screen bg-gray-50 flex items-center justify-center">Aucun produit trouvé.</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow p-8">
        <div className="flex items-center mb-6">
          <Edit className="h-7 w-7 text-blue-600 mr-2" />
          <h1 className="text-2xl font-bold text-gray-900">Modifier le produit</h1>
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
            disabled={saving}
            className="btn btn-primary w-full"
          >
            {saving ? 'Mise à jour...' : 'Mettre à jour'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default SellerProductUpdatePage;
