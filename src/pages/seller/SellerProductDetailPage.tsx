import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Edit, Trash2, ArrowLeft } from 'lucide-react';

interface SellerProduct {
  id: string;
  name: string;
  description: string;
  price: number;
  sku: string;
  is_active: boolean;
  images?: { url: string; is_primary: boolean }[];
  category?: string;
}

const SellerProductDetailPage: React.FC = () => {
  const { productId } = useParams<{ productId: string }>();
  const [product, setProduct] = useState<SellerProduct | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProduct = async () => {
      setLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem('sellerToken');
        const response = await fetch(`http://localhost:8005/api/sellers/products/${productId}/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          setError('Produit introuvable');
          setProduct(null);
          return;
        }
        const data = await response.json();
        setProduct(data);
      } catch (err) {
        setError('Erreur lors du chargement du produit');
        setProduct(null);
      } finally {
        setLoading(false);
      }
    };
    if (productId) fetchProduct();
  }, [productId]);

  const handleDelete = async () => {
    if (!window.confirm('Voulez-vous vraiment supprimer ce produit ?')) return;
    try {
      const token = localStorage.getItem('sellerToken');
      const response = await fetch(`http://localhost:8005/api/sellers/products/${productId}/delete/`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.ok) {
        navigate('/seller/products');
      } else {
        setError('Erreur lors de la suppression');
      }
    } catch {
      setError('Erreur lors de la suppression');
    }
  };

  if (loading) return <div className="min-h-screen bg-gray-50 flex items-center justify-center">Chargement...</div>;
  if (error) return <div className="min-h-screen bg-gray-50 flex items-center justify-center text-red-500">{error}</div>;
  if (!product) return <div className="min-h-screen bg-gray-50 flex items-center justify-center">Aucun produit trouvé.</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow p-8">
        <div className="flex items-center mb-6">
          <button onClick={() => navigate(-1)} className="mr-4 text-gray-500 hover:text-amazon-orange">
            <ArrowLeft className="h-5 w-5" />
          </button>
          <h1 className="text-2xl font-bold text-gray-900 flex-1">{product.name}</h1>
          <Link to={`/seller/products/${product.id}/update`} className="btn btn-secondary flex items-center mr-2">
            <Edit className="h-4 w-4 mr-1" /> Modifier
          </Link>
          <button onClick={handleDelete} className="btn btn-danger flex items-center">
            <Trash2 className="h-4 w-4 mr-1" /> Supprimer
          </button>
        </div>
        <div className="flex flex-col md:flex-row gap-8">
          <div className="md:w-1/3">
            <img
              src={
                product.images && product.images.length
                  ? product.images.find(img => img.is_primary)?.url || product.images[0].url
                  : 'https://via.placeholder.com/300x300?text=No+Image'
              }
              alt={product.name}
              className="w-full h-auto object-contain rounded border"
            />
          </div>
          <div className="md:w-2/3 space-y-4">
            <div>
              <span className="font-medium text-gray-700">Description :</span>
              <div className="text-gray-900">{product.description}</div>
            </div>
            <div>
              <span className="font-medium text-gray-700">Prix :</span>
              <span className="text-amazon-error font-bold ml-2">€{Number(product.price).toFixed(2)}</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">SKU :</span> {product.sku}
            </div>
            <div>
              <span className="font-medium text-gray-700">Statut :</span>
              {product.is_active ? (
                <span className="inline-block px-2 py-1 text-xs font-semibold bg-green-100 text-green-700 rounded ml-2">
                  Actif
                </span>
              ) : (
                <span className="inline-block px-2 py-1 text-xs font-semibold bg-gray-200 text-gray-500 rounded ml-2">
                  Inactif
                </span>
              )}
            </div>
            {product.category && (
              <div>
                <span className="font-medium text-gray-700">Catégorie :</span> {product.category}
              </div>
            )}
          </div>
        </div>
        <div className="mt-8 flex justify-end">
          <Link to="/seller/products" className="btn btn-secondary">
            Retour à la liste des produits
          </Link>
        </div>
      </div>
    </div>
  );
};

export default SellerProductDetailPage;
