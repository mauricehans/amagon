import React, { useEffect, useState } from 'react';
import { Calendar, Eye } from 'lucide-react';
import { Link } from 'react-router-dom';

interface SellerOrder {
  id: string;
  customer_email: string;
  total_amount: number;
  status: string;
  created_at: string;
}

const SellerOrdersPage: React.FC = () => {
  const [orders, setOrders] = useState<SellerOrder[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchOrders = async () => {
      setLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem('sellerToken');
        const response = await fetch('http://localhost:8005/api/sellers/orders/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!response.ok) {
          setError('Erreur lors du chargement des commandes');
          setOrders([]);
          return;
        }
        const data = await response.json();
        setOrders(data);
      } catch {
        setError('Erreur lors du chargement des commandes');
        setOrders([]);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  if (loading) return <div className="min-h-screen bg-gray-50 flex items-center justify-center">Chargement...</div>;
  if (error) return <div className="min-h-screen bg-gray-50 flex items-center justify-center text-red-500">{error}</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center mb-8">
          <div className="p-4 bg-amazon-orange rounded-full mr-4">
            <Calendar className="h-8 w-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-1">Commandes</h1>
            <p className="text-gray-600">Suivez toutes vos commandes récentes</p>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          {orders.length === 0 ? (
            <div className="text-center text-gray-500 py-12">
              Aucune commande trouvée.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead>
                  <tr>
                    <th className="text-left p-2">N°</th>
                    <th className="text-left p-2">Client</th>
                    <th className="text-left p-2">Montant</th>
                    <th className="text-left p-2">Statut</th>
                    <th className="text-left p-2">Date</th>
                    <th className="text-left p-2">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map(order => (
                    <tr key={order.id} className="border-t hover:bg-gray-50 transition">
                      <td className="p-2 font-mono">#{order.id.slice(0, 8)}</td>
                      <td className="p-2">{order.customer_email}</td>
                      <td className="p-2 font-semibold text-amazon-error">€{Number(order.total_amount).toFixed(2)}</td>
                      <td className="p-2">
                        <span className={`inline-block px-2 py-1 text-xs font-semibold rounded ${
                          order.status === 'completed'
                            ? 'bg-green-100 text-green-700'
                            : order.status === 'pending'
                            ? 'bg-yellow-100 text-yellow-700'
                            : 'bg-gray-200 text-gray-500'
                        }`}>
                          {order.status}
                        </span>
                      </td>
                      <td className="p-2">{new Date(order.created_at).toLocaleDateString()}</td>
                      <td className="p-2">
                        <Link to={`/seller/orders/${order.id}`} className="inline-flex items-center text-amazon-teal hover:underline">
                          <Eye className="h-4 w-4 mr-1" /> Voir
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SellerOrdersPage;
