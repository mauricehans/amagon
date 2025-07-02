import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { User, Edit, Save, X } from 'lucide-react';

interface SellerProfile {
  id: string;
  name: string;
  email: string;
  phone?: string;
  company_name?: string;
  business_type?: string;
  address?: any;
}

const SellerProfilePage: React.FC = () => {
  const [profile, setProfile] = useState<SellerProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editMode, setEditMode] = useState(false);
  const [editForm, setEditForm] = useState<SellerProfile | null>(null);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem('sellerToken');
        const response = await fetch('http://localhost:8005/api/sellers/profile/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          setError('Failed to fetch profile');
          setProfile(null);
          return;
        }
        const data = await response.json();
        setProfile(data);
      } catch (err) {
        setError('Failed to fetch profile');
        setProfile(null);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const handleEdit = () => {
    setEditForm(profile);
    setEditMode(true);
    setSuccess(null);
    setError(null);
  };

  const handleCancel = () => {
    setEditMode(false);
    setEditForm(null);
    setSuccess(null);
    setError(null);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!editForm) return;
    const { name, value } = e.target;
    setEditForm({ ...editForm, [name]: value });
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editForm) return;
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      const token = localStorage.getItem('sellerToken');
      const response = await fetch('http://localhost:8005/api/sellers/profile/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(editForm),
      });
      if (!response.ok) {
        const data = await response.json();
        setError(data.error || 'Erreur lors de la mise à jour');
        setSaving(false);
        return;
      }
      const updated = await response.json();
      setProfile(updated);
      setEditMode(false);
      setEditForm(null);
      setSuccess('Profil mis à jour !');
    } catch {
      setError('Erreur lors de la mise à jour');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="min-h-screen bg-gray-50 flex items-center justify-center">Loading...</div>;
  if (error) return <div className="min-h-screen bg-gray-50 flex items-center justify-center text-red-500">{error}</div>;
  if (!profile) return <div className="min-h-screen bg-gray-50 flex items-center justify-center">No profile found.</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center mb-8">
          <div className="p-4 bg-amazon-orange rounded-full mr-4">
            <User className="h-8 w-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-1">Mon profil vendeur</h1>
            <p className="text-gray-600">Gérez vos informations personnelles et professionnelles</p>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Informations du compte</h2>
            {!editMode ? (
              <button onClick={handleEdit} className="flex items-center text-amazon-orange hover:underline">
                <Edit className="h-4 w-4 mr-1" /> Modifier
              </button>
            ) : (
              <div className="flex gap-2">
                <button
                  onClick={handleSave}
                  className="flex items-center text-green-600 hover:underline disabled:opacity-50"
                  disabled={saving}
                >
                  <Save className="h-4 w-4 mr-1" /> {saving ? 'Enregistrement...' : 'Enregistrer'}
                </button>
                <button
                  onClick={handleCancel}
                  className="flex items-center text-red-600 hover:underline"
                  disabled={saving}
                >
                  <X className="h-4 w-4 mr-1" /> Annuler
                </button>
              </div>
            )}
          </div>
          {success && <div className="mb-4 text-green-600 bg-green-50 border border-green-200 rounded p-2">{success}</div>}
          {editMode && editForm ? (
            <form onSubmit={handleSave} className="space-y-4">
              <div>
                <label className="font-medium text-gray-700 block mb-1">Nom :</label>
                <input
                  name="name"
                  value={editForm.name}
                  onChange={handleChange}
                  className="form-input"
                  required
                />
              </div>
              <div>
                <label className="font-medium text-gray-700 block mb-1">Email :</label>
                <input
                  name="email"
                  value={editForm.email}
                  onChange={handleChange}
                  className="form-input"
                  required
                />
              </div>
              <div>
                <label className="font-medium text-gray-700 block mb-1">Téléphone :</label>
                <input
                  name="phone"
                  value={editForm.phone || ''}
                  onChange={handleChange}
                  className="form-input"
                />
              </div>
              <div>
                <label className="font-medium text-gray-700 block mb-1">Entreprise :</label>
                <input
                  name="company_name"
                  value={editForm.company_name || ''}
                  onChange={handleChange}
                  className="form-input"
                />
              </div>
              <div>
                <label className="font-medium text-gray-700 block mb-1">Type :</label>
                <input
                  name="business_type"
                  value={editForm.business_type || ''}
                  onChange={handleChange}
                  className="form-input"
                />
              </div>
              {/* Adresse simplifiée */}
              <div>
                <label className="font-medium text-gray-700 block mb-1">Adresse :</label>
                <input
                  name="address"
                  value={typeof editForm.address === 'string' ? editForm.address : JSON.stringify(editForm.address || {})}
                  onChange={handleChange}
                  className="form-input"
                />
              </div>
              <button
                type="submit"
                className="btn btn-primary w-full"
                disabled={saving}
              >
                {saving ? 'Enregistrement...' : 'Enregistrer'}
              </button>
            </form>
          ) : (
            <div className="space-y-4">
              <div>
                <span className="font-medium text-gray-700">Nom :</span> {profile.name}
              </div>
              <div>
                <span className="font-medium text-gray-700">Email :</span> {profile.email}
              </div>
              {profile.phone && (
                <div>
                  <span className="font-medium text-gray-700">Téléphone :</span> {profile.phone}
                </div>
              )}
              {profile.company_name && (
                <div>
                  <span className="font-medium text-gray-700">Entreprise :</span> {profile.company_name}
                </div>
              )}
              {profile.business_type && (
                <div>
                  <span className="font-medium text-gray-700">Type :</span> {profile.business_type}
                </div>
              )}
              {profile.address && (
                <div>
                  <span className="font-medium text-gray-700">Adresse :</span>
                  <div className="ml-2 text-sm text-gray-700">
                    {typeof profile.address === 'object'
                      ? Object.entries(profile.address).map(([k, v]) => (
                          <div key={k}>{k}: {v}</div>
                        ))
                      : profile.address}
                  </div>
                </div>
              )}
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

export default SellerProfilePage;
