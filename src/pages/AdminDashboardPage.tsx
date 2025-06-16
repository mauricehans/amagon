import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Shield, 
  Users, 
  Store, 
  MessageSquare, 
  TrendingUp, 
  AlertCircle,
  CheckCircle,
  Clock,
  User,
  Settings,
  LogOut,
  Search,
  Filter,
  Eye,
  UserCheck,
  MessageCircle
} from 'lucide-react';

interface DashboardData {
  stats: {
    total_tickets: number;
    open_tickets: number;
    in_progress_tickets: number;
    resolved_today: number;
    my_tickets: number;
    my_open_tickets: number;
  };
  recent_tickets: any[];
  priority_stats: any[];
  category_stats: any[];
}

const AdminDashboardPage: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('dashboard');
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('adminToken');
      if (!token) {
        navigate('/admin/login');
        return;
      }

      const response = await fetch('http://localhost:8007/api/admin/dashboard/', {
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
    localStorage.removeItem('adminToken');
    localStorage.removeItem('adminData');
    navigate('/admin/login');
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'bg-red-100 text-red-800';
      case 'in_progress': return 'bg-yellow-100 text-yellow-800';
      case 'resolved': return 'bg-green-100 text-green-800';
      case 'closed': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-red-600"></div>
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

  const adminData = JSON.parse(localStorage.getItem('adminData') || '{}');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Shield className="h-8 w-8 text-red-600 mr-3" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">Administration Amagon</h1>
                <p className="text-sm text-gray-600">Bienvenue, {adminData.username}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Link to="/" className="text-gray-600 hover:text-gray-900">
                Voir le site
              </Link>
              <button 
                onClick={handleLogout}
                className="flex items-center text-red-600 hover:text-red-800"
              >
                <LogOut className="h-4 w-4 mr-1" />
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
            <button 
              onClick={() => setActiveTab('dashboard')}
              className={`pb-2 ${activeTab === 'dashboard' ? 'text-red-600 border-b-2 border-red-600' : 'text-gray-600 hover:text-gray-900'}`}
            >
              Tableau de bord
            </button>
            <button 
              onClick={() => setActiveTab('tickets')}
              className={`pb-2 ${activeTab === 'tickets' ? 'text-red-600 border-b-2 border-red-600' : 'text-gray-600 hover:text-gray-900'}`}
            >
              Support Tickets
            </button>
            <button 
              onClick={() => setActiveTab('users')}
              className={`pb-2 ${activeTab === 'users' ? 'text-red-600 border-b-2 border-red-600' : 'text-gray-600 hover:text-gray-900'}`}
            >
              Utilisateurs
            </button>
            <button 
              onClick={() => setActiveTab('sellers')}
              className={`pb-2 ${activeTab === 'sellers' ? 'text-red-600 border-b-2 border-red-600' : 'text-gray-600 hover:text-gray-900'}`}
            >
              Vendeurs
            </button>
          </div>
        </nav>

        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && (
          <>
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-red-100 rounded-lg">
                    <MessageSquare className="h-6 w-6 text-red-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Tickets totaux</p>
                    <p className="text-2xl font-bold text-gray-900">{dashboardData?.stats.total_tickets || 0}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-yellow-100 rounded-lg">
                    <AlertCircle className="h-6 w-6 text-yellow-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Tickets ouverts</p>
                    <p className="text-2xl font-bold text-gray-900">{dashboardData?.stats.open_tickets || 0}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Clock className="h-6 w-6 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">En cours</p>
                    <p className="text-2xl font-bold text-gray-900">{dashboardData?.stats.in_progress_tickets || 0}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <CheckCircle className="h-6 w-6 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Résolus aujourd'hui</p>
                    <p className="text-2xl font-bold text-gray-900">{dashboardData?.stats.resolved_today || 0}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Mes tickets */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Mes tickets assignés</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-blue-600">{dashboardData?.stats.my_tickets || 0}</p>
                    <p className="text-sm text-gray-600">Total assignés</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-orange-600">{dashboardData?.stats.my_open_tickets || 0}</p>
                    <p className="text-sm text-gray-600">En attente</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Répartition par priorité</h3>
                <div className="space-y-2">
                  {dashboardData?.priority_stats?.map((stat) => (
                    <div key={stat.priority} className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className={`w-3 h-3 rounded-full mr-2 ${getPriorityColor(stat.priority)}`}></div>
                        <span className="text-sm capitalize">{stat.priority}</span>
                      </div>
                      <span className="text-sm font-medium">{stat.count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Tickets récents */}
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-medium text-gray-900">Tickets récents</h3>
                  <button 
                    onClick={() => setActiveTab('tickets')}
                    className="text-red-600 hover:text-red-700"
                  >
                    Voir tout
                  </button>
                </div>
              </div>
              <div className="p-6">
                {dashboardData?.recent_tickets?.length ? (
                  <div className="space-y-4">
                    {dashboardData.recent_tickets.slice(0, 5).map((ticket) => (
                      <div key={ticket.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
                        <div className="flex items-center space-x-4">
                          <div className={`w-3 h-3 rounded-full ${getPriorityColor(ticket.priority)}`}></div>
                          <div>
                            <p className="font-medium text-gray-900">#{ticket.ticket_number}</p>
                            <p className="text-sm text-gray-600">{ticket.subject}</p>
                            <p className="text-xs text-gray-500">
                              {ticket.requester_name} ({ticket.requester_type})
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(ticket.status)}`}>
                            {ticket.status}
                          </span>
                          <p className="text-xs text-gray-500 mt-1">
                            {new Date(ticket.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-8">Aucun ticket récent</p>
                )}
              </div>
            </div>
          </>
        )}

        {/* Tickets Tab */}
        {activeTab === 'tickets' && (
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900">Gestion des tickets de support</h3>
                <div className="flex items-center space-x-2">
                  <div className="relative">
                    <Search className="h-4 w-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Rechercher..."
                      className="pl-10 pr-4 py-2 border border-gray-300 rounded-md text-sm"
                    />
                  </div>
                  <button className="flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm">
                    <Filter className="h-4 w-4 mr-1" />
                    Filtrer
                  </button>
                </div>
              </div>
            </div>
            <div className="p-6">
              <p className="text-gray-500 text-center py-8">
                Interface de gestion des tickets en cours de développement...
              </p>
            </div>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Gestion des utilisateurs</h3>
            </div>
            <div className="p-6">
              <p className="text-gray-500 text-center py-8">
                Interface de gestion des utilisateurs en cours de développement...
              </p>
            </div>
          </div>
        )}

        {/* Sellers Tab */}
        {activeTab === 'sellers' && (
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Gestion des vendeurs</h3>
            </div>
            <div className="p-6">
              <p className="text-gray-500 text-center py-8">
                Interface de gestion des vendeurs en cours de développement...
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboardPage;