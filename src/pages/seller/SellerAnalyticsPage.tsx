import React, { useEffect, useState } from 'react';
import { BarChart3, PieChart } from 'lucide-react';

interface CategoryStat {
  category: string;
  count: number;
  total_sales: number;
}

interface AnalyticsData {
  sales_by_period: {
    today: number;
    week: number;
    month: number;
  };
  category_stats: CategoryStat[];
}

const SellerAnalyticsPage: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      setLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem('sellerToken');
        const response = await fetch('http://localhost:8005/api/sellers/analytics/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!response.ok) {
          setError('Erreur lors du chargement des statistiques');
          setData(null);
          return;
        }
        const json = await response.json();
        setData(json);
      } catch {
        setError('Erreur lors du chargement des statistiques');
        setData(null);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) return <div className="min-h-screen bg-gray-50 flex items-center justify-center">Chargement...</div>;
  if (error) return <div className="min-h-screen bg-gray-50 flex items-center justify-center text-red-500">{error}</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center mb-8">
          <div className="p-4 bg-blue-100 rounded-full mr-4">
            <BarChart3 className="h-8 w-8 text-blue-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-1">Statistiques & Analyses</h1>
            <p className="text-gray-600">Suivez vos ventes et la performance de vos produits</p>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-sm text-gray-500 mb-2">Ventes aujourd'hui</div>
            <div className="text-2xl font-bold text-amazon-orange">€{Number(data?.sales_by_period.today || 0).toFixed(2)}</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-sm text-gray-500 mb-2">Ventes cette semaine</div>
            <div className="text-2xl font-bold text-green-600">€{Number(data?.sales_by_period.week || 0).toFixed(2)}</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-sm text-gray-500 mb-2">Ventes ce mois</div>
            <div className="text-2xl font-bold text-blue-600">€{Number(data?.sales_by_period.month || 0).toFixed(2)}</div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center mb-4">
            <PieChart className="h-5 w-5 text-amazon-orange mr-2" />
            <h2 className="text-lg font-semibold text-gray-900">Produits par catégorie</h2>
          </div>
          {data?.category_stats?.length ? (
            <table className="min-w-full text-sm">
              <thead>
                <tr>
                  <th className="text-left p-2">Catégorie</th>
                  <th className="text-left p-2">Nb produits</th>
                  <th className="text-left p-2">Ventes totales (€)</th>
                </tr>
              </thead>
              <tbody>
                {data.category_stats.map((cat, idx) => (
                  <tr key={idx} className="border-t">
                    <td className="p-2">{cat.category}</td>
                    <td className="p-2">{cat.count}</td>
                    <td className="p-2">{Number(cat.total_sales || 0).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="text-gray-500 text-center py-8">Aucune donnée de catégorie</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SellerAnalyticsPage;
