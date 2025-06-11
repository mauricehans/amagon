import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Store, Eye, EyeOff, Building, User } from 'lucide-react';

const SellerRegisterPage: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
    company_name: '',
    business_type: 'individual',
    address: {
      street: '',
      city: '',
      state: '',
      zip: '',
      country: 'France'
    }
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    
    if (name.startsWith('address.')) {
      const addressField = name.split('.')[1];
      setFormData(prev => ({
        ...prev,
        address: {
          ...prev.address,
          [addressField]: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!formData.name || !formData.email || !formData.password) {
      setError('Veuillez remplir tous les champs obligatoires');
      return;
    }
    
    if (formData.password !== formData.confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      return;
    }
    
    if (formData.password.length < 6) {
      setError('Le mot de passe doit contenir au moins 6 caractères');
      return;
    }
    
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await fetch('http://localhost:8005/api/sellers/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        // Stocker le token et les infos vendeur
        localStorage.setItem('sellerToken', data.token);
        localStorage.setItem('sellerData', JSON.stringify(data.seller));
        navigate('/seller/dashboard');
      } else {
        setError(data.error || 'Erreur lors de l\'inscription');
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amazon-blue-dark to-amazon-blue-light py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="mx-auto h-16 w-16 bg-amazon-orange rounded-full flex items-center justify-center">
            <Store className="h-8 w-8 text-white" />
          </div>
          <h2 className="mt-6 text-3xl font-extrabold text-white">
            Devenir Vendeur
          </h2>
          <p className="mt-2 text-sm text-gray-300">
            Créez votre compte vendeur et commencez à vendre
          </p>
        </div>

        {/* Form */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Type de compte */}
            <div>
              <label className="form-label">Type de compte</label>
              <div className="mt-2 space-y-2">
                <div className="flex items-center">
                  <input
                    id="individual"
                    name="business_type"
                    type="radio"
                    value="individual"
                    checked={formData.business_type === 'individual'}
                    onChange={handleInputChange}
                    className="h-4 w-4 text-amazon-orange focus:ring-amazon-orange border-gray-300"
                  />
                  <label htmlFor="individual" className="ml-3 flex items-center">
                    <User className="h-5 w-5 mr-2 text-gray-500" />
                    Particulier
                  </label>
                </div>
                <div className="flex items-center">
                  <input
                    id="company"
                    name="business_type"
                    type="radio"
                    value="company"
                    checked={formData.business_type === 'company'}
                    onChange={handleInputChange}
                    className="h-4 w-4 text-amazon-orange focus:ring-amazon-orange border-gray-300"
                  />
                  <label htmlFor="company" className="ml-3 flex items-center">
                    <Building className="h-5 w-5 mr-2 text-gray-500" />
                    Entreprise
                  </label>
                </div>
              </div>
            </div>

            {/* Informations personnelles */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="name" className="form-label">
                  Nom complet *
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Votre nom complet"
                  required
                />
              </div>
              
              <div>
                <label htmlFor="email" className="form-label">
                  Adresse email *
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="votre@email.com"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="phone" className="form-label">
                  Téléphone
                </label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="+33 1 23 45 67 89"
                />
              </div>
              
              {formData.business_type === 'company' && (
                <div>
                  <label htmlFor="company_name" className="form-label">
                    Nom de l'entreprise
                  </label>
                  <input
                    type="text"
                    id="company_name"
                    name="company_name"
                    value={formData.company_name}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Nom de votre entreprise"
                  />
                </div>
              )}
            </div>

            {/* Mot de passe */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="password" className="form-label">
                  Mot de passe *
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    className="form-input pr-10"
                    placeholder="Au moins 6 caractères"
                    required
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5 text-gray-400" />
                    ) : (
                      <Eye className="h-5 w-5 text-gray-400" />
                    )}
                  </button>
                </div>
              </div>
              
              <div>
                <label htmlFor="confirmPassword" className="form-label">
                  Confirmer le mot de passe *
                </label>
                <div className="relative">
                  <input
                    type={showConfirmPassword ? 'text' : 'password'}
                    id="confirmPassword"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    className="form-input pr-10"
                    placeholder="Confirmer le mot de passe"
                    required
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-5 w-5 text-gray-400" />
                    ) : (
                      <Eye className="h-5 w-5 text-gray-400" />
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Adresse */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Adresse</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="md:col-span-2">
                  <label htmlFor="address.street" className="form-label">
                    Adresse
                  </label>
                  <input
                    type="text"
                    id="address.street"
                    name="address.street"
                    value={formData.address.street}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Numéro et nom de rue"
                  />
                </div>
                
                <div>
                  <label htmlFor="address.city" className="form-label">
                    Ville
                  </label>
                  <input
                    type="text"
                    id="address.city"
                    name="address.city"
                    value={formData.address.city}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Ville"
                  />
                </div>
                
                <div>
                  <label htmlFor="address.zip" className="form-label">
                    Code postal
                  </label>
                  <input
                    type="text"
                    id="address.zip"
                    name="address.zip"
                    value={formData.address.zip}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="75000"
                  />
                </div>
              </div>
            </div>

            {/* Conditions */}
            <div className="flex items-center">
              <input
                id="terms"
                name="terms"
                type="checkbox"
                required
                className="h-4 w-4 text-amazon-orange focus:ring-amazon-orange border-gray-300 rounded"
              />
              <label htmlFor="terms" className="ml-2 block text-sm text-gray-900">
                J'accepte les{' '}
                <a href="#" className="text-amazon-orange hover:text-amazon-orange-hover">
                  conditions d'utilisation
                </a>{' '}
                et la{' '}
                <a href="#" className="text-amazon-orange hover:text-amazon-orange-hover">
                  politique de confidentialité
                </a>
              </label>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-amazon-orange hover:bg-amazon-orange-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amazon-orange disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Création du compte...' : 'Créer mon compte vendeur'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <span className="text-sm text-gray-600">
              Déjà un compte vendeur ?{' '}
              <Link to="/seller/login" className="font-medium text-amazon-orange hover:text-amazon-orange-hover">
                Se connecter
              </Link>
            </span>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8">
          <Link to="/" className="text-sm text-gray-300 hover:text-white">
            ← Retour au site principal
          </Link>
        </div>
      </div>
    </div>
  );
};

export default SellerRegisterPage;