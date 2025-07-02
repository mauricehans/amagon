import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Package, Plus, Edit, Trash2, Eye } from 'lucide-react';

interface SellerProduct {
  id: string;
  name: string;
  description: string;
  price: number;
  sku: string;
  is_active: boolean;
  images?: { url: string; is_primary: boolean }[];
}

const SellerProductsPage: React.FC = () => {
  const [products, setProducts] = useState<SellerProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem('sellerToken');
        const response = await fetch('http://localhost:8005/api/sellers/products/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          setError('Failed to fetch products');
          setProducts([]);
          return;
        }
        const data = await response.json();
        setProducts(data);
      } catch (err) {
        setError('Failed to fetch products');
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, []);

  const handleDelete = async (productId: string) => {
    if (!window.confirm('Voulez-vous vraiment supprimer ce produit ?')) return;
    setDeletingId(productId);
    try {
      const token = localStorage.getItem('sellerToken');
      const response = await fetch(`http://localhost:8005/api/sellers/products/${productId}/delete/`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.ok) {
        setProducts(products => products.filter(p => p.id !== productId));
      } else {
        alert('Erreur lors de la suppression');
      }
    } catch {
      alert('Erreur lors de la suppression');
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) return <div className="min-h-screen bg-gray-50 flex items-center justify-center">Loading...</div>;
  if (error) return <div className="min-h-screen bg-gray-50 flex items-center justify-center text-red-500">{error}</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center mb-8">
          <div className="p-4 bg-blue-100 rounded-full mr-4">
            <Package className="h-8 w-8 text-blue-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-1">Mes produits</h1>
            <p className="text-gray-600">Gérez vos produits en vente sur la marketplace</p>
          </div>
          <div className="flex-1 flex justify-end">
            <Link to="/seller/products/create" className="btn btn-primary flex items-center">
              <Plus className="h-4 w-4 mr-2" /> Ajouter un produit
            </Link>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          {products.length === 0 ? (
            <div className="text-center text-gray-500 py-12">
              Aucun produit trouvé.<br />
              <Link to="/seller/products/create" className="text-amazon-orange hover:underline font-medium">
                Ajouter votre premier produit
              </Link>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead>
                  <tr>
                    <th className="text-left p-2">Image</th>
                    <th className="text-left p-2">Nom</th>
                    <th className="text-left p-2">SKU</th>
                    <th className="text-left p-2">Prix</th>
                    <th className="text-left p-2">Statut</th>
                    <th className="text-left p-2">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {products.map(product => (
                    <tr key={product.id} className="border-t hover:bg-gray-50 transition">
                      <td className="p-2">
                        <img
                          src={
                            product.images && product.images.length
                              ? product.images.find(img => img.is_primary)?.url || product.images[0].url
                              : 'https://via.placeholder.com/60x60?text=No+Image'
                          }
                          alt={product.name}
                          className="w-12 h-12 object-contain rounded"
                        />
                      </td>
                      <td className="p-2 font-medium">{product.name}</td>
                      <td className="p-2">{product.sku}</td>
                      <td className="p-2 font-semibold text-amazon-error">
                        €{Number(product.price).toFixed(2)}
                      </td>
                      <td className="p-2">
                        {product.is_active ? (
                          <span className="inline-block px-2 py-1 text-xs font-semibold bg-green-100 text-green-700 rounded">
                            Actif
                          </span>
                        ) : (
                          <span className="inline-block px-2 py-1 text-xs font-semibold bg-gray-200 text-gray-500 rounded">
                            Inactif
                          </span>
                        )}
                      </td>
                      <td className="p-2 space-x-2">
                        <Link
                          to={`/seller/products/${product.id}`}
                          className="inline-flex items-center text-amazon-teal hover:underline"
                          title="Voir"
                        >
                          <Eye className="h-4 w-4 mr-1" /> Voir
                        </Link>
                        <Link
                          to={`/seller/products/${product.id}/update`}
                          className="inline-flex items-center text-blue-600 hover:underline"
                          title="Éditer"
                        >
                          <Edit className="h-4 w-4 mr-1" /> Éditer
                        </Link>
                        <button
                          onClick={() => handleDelete(product.id)}
                          className="inline-flex items-center text-red-600 hover:underline disabled:opacity-50"
                          title="Supprimer"
                          disabled={deletingId === product.id}
                        >
                          <Trash2 className="h-4 w-4 mr-1" />
                          {deletingId === product.id ? 'Suppression...' : 'Supprimer'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
        <div className="mt-8 flex justify-end">
          <Link to="/seller/dashboard" className="btn btn-secondary">
            Retour au tableau de bord
          </Link>
        </div>
      </div>
    </div>
  );
};

export default SellerProductsPage;
