import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Store, 
  Package, 
  ShoppingCart, 
  TrendingUp, 
  DollarSign, 
  Users, 
  Plus,
  Eye,
  Edit,
  Trash2,
  BarChart3,
  Calendar,
  Star
} from 'lucide-react';

interface DashboardData {
  stats: {
    total_products: number;
    active_products: number;
    total_orders: number;
    total_revenue: number;
  };
  recent_orders: any[];
  top_products: any[];
  monthly_sales: any[];
}

const SellerDashboardPage: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('sellerToken');
      if (!token) {
        navigate('/seller/login');
        return;
      }

      const response = await fetch('http://localhost:8005/api/sellers/dashboard/', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      } else {
        setError('Erreur lors du chargement des données');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('sellerToken');
    localStorage.removeItem('sellerData');
    navigate('/seller/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-amazon-orange"></div>
          <p className="mt-4 text-gray-600">Chargement du tableau de bord...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button 
            onClick={fetchDashboardData}
            className="btn btn-primary"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  const sellerData = JSON.parse(localStorage.getItem('sellerData') || '{}');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Store className="h-8 w-8 text-amazon-orange mr-3" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">Espace Vendeur</h1>
                <p className="text-sm text-gray-600">Bienvenue, {sellerData.name}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Link to="/" className="text-gray-600 hover:text-gray-900">
                Voir le site
              </Link>
              <button 
                onClick={handleLogout}
                className="text-red-600 hover:text-red-800"
              >
                Déconnexion
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation */}
        <nav className="mb-8">
          <div className="flex space-x-8">
            <Link to="/seller/dashboard" className="text-amazon-orange border-b-2 border-amazon-orange pb-2">
              Tableau de bord
            </Link>
            <Link to="/seller/products" className="text-gray-600 hover:text-gray-900 pb-2">
              Mes produits
            </Link>
            <Link to="/seller/orders" className="text-gray-600 hover:text-gray-900 pb-2">
              Commandes
            </Link>
            <Link to="/seller/analytics" className="text-gray-600 hover:text-gray-900 pb-2">
              Analyses
            </Link>
            <Link to="/seller/profile" className="text-gray-600 hover:text-gray-900 pb-2">
              Profil
            </Link>
          </div>
        </nav>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Package className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Produits totaux</p>
                <p className="text-2xl font-bold text-gray-900">{dashboardData?.stats.total_products || 0}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <TrendingUp className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Produits actifs</p>
                <p className="text-2xl font-bold text-gray-900">{dashboardData?.stats.active_products || 0}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <ShoppingCart className="h-6 w-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Commandes</p>
                <p className="text-2xl font-bold text-gray-900">{dashboardData?.stats.total_orders || 0}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <DollarSign className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Revenus totaux</p>
                <p className="text-2xl font-bold text-gray-900">€{dashboardData?.stats.total_revenue?.toFixed(2) || '0.00'}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Commandes récentes */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900">Commandes récentes</h3>
                <Link to="/seller/orders" className="text-amazon-orange hover:text-amazon-orange-hover">
                  Voir tout
                </Link>
              </div>
            </div>
            <div className="p-6">
              {dashboardData?.recent_orders?.length ? (
                <div className="space-y-4">
                  {dashboardData.recent_orders.map((order) => (
                    <div key={order.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                      <div>
                        <p className="font-medium text-gray-900">#{order.id.slice(0, 8)}</p>
                        <p className="text-sm text-gray-600">{order.customer_email}</p>
                        <p className="text-sm text-gray-500">{new Date(order.created_at).toLocaleDateString()}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-medium text-gray-900">€{order.total_amount}</p>
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          order.status === 'completed' ? 'bg-green-100 text-green-800' :
                          order.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-blue-100 text-blue-800'
                        }`}>
                          {order.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">Aucune commande récente</p>
              )}
            </div>
          </div>

          {/* Produits les plus vendus */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900">Produits populaires</h3>
                <Link to="/seller/products" className="text-amazon-orange hover:text-amazon-orange-hover">
                  Gérer
                </Link>
              </div>
            </div>
            <div className="p-6">
              {dashboardData?.top_products?.length ? (
                <div className="space-y-4">
                  {dashboardData.top_products.map((product) => (
                    <div key={product.id} className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center">
                        <Package className="h-6 w-6 text-gray-500" />
                      </div>
                      <div className="flex-1">
                        <p className="font-medium text-gray-900">{product.name}</p>
                        <p className="text-sm text-gray-600">€{product.price}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-900">Stock: {product.stock_quantity}</p>
                        <p className="text-xs text-gray-500">{product.category}</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <Package className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500 mb-4">Aucun produit ajouté</p>
                  <Link to="/seller/products/create" className="btn btn-primary">
                    <Plus className="h-4 w-4 mr-2" />
                    Ajouter un produit
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Graphique des ventes */}
        {dashboardData?.monthly_sales?.length ? (
          <div className="mt-8 bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Évolution des ventes</h3>
            </div>
            <div className="p-6">
              <div className="flex items-end space-x-2 h-64">
                {dashboardData.monthly_sales.map((month, index) => (
                  <div key={index} className="flex-1 flex flex-col items-center">
                    <div 
                      className="w-full bg-amazon-orange rounded-t"
                      style={{ 
                        height: `${Math.max((month.sales / Math.max(...dashboardData.monthly_sales.map(m => m.sales))) * 200, 10)}px` 
                      }}
                    ></div>
                    <p className="text-xs text-gray-600 mt-2">{month.month.slice(0, 3)}</p>
                    <p className="text-xs font-medium">€{month.sales.toFixed(0)}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : null}

        {/* Actions rapides */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link to="/seller/products/create" className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <Plus className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <h4 className="font-medium text-gray-900">Ajouter un produit</h4>
                <p className="text-sm text-gray-600">Créer un nouveau produit</p>
              </div>
            </div>
          </Link>

          <Link to="/seller/analytics" className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <BarChart3 className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <h4 className="font-medium text-gray-900">Voir les analyses</h4>
                <p className="text-sm text-gray-600">Statistiques détaillées</p>
              </div>
            </div>
          </Link>

          <Link to="/seller/profile" className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Users className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <h4 className="font-medium text-gray-900">Mon profil</h4>
                <p className="text-sm text-gray-600">Gérer mon compte</p>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default SellerDashboardPage;