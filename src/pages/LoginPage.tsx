import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showReset, setShowReset] = useState(false);
  const [resetEmail, setResetEmail] = useState('');
  const [resetLoading, setResetLoading] = useState(false);
  const [resetMsg, setResetMsg] = useState<string | null>(null);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email || !password) {
      setError('Please enter both email and password');
      return;
    }
    
    try {
      setIsLoading(true);
      setError(null);
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError('Invalid email or password');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setResetLoading(true);
    setResetMsg(null);
    try {
      const response = await fetch('http://localhost:8005/api/sellers/password-reset/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: resetEmail }),
      });
      if (response.ok) {
        setResetMsg('Un email de réinitialisation a été envoyé si ce compte existe.');
      } else {
        setResetMsg("Impossible d'envoyer l'email. Vérifiez l'adresse.");
      }
    } catch {
      setResetMsg('Erreur de connexion au serveur.');
    } finally {
      setResetLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-sm mx-auto">
        <Link to="/" className="block text-center mb-6">
          <h1 className="text-3xl font-bold tracking-wide">amazon</h1>
        </Link>
        
        <div className="bg-white p-6 rounded shadow-sm border border-gray-200">
          <h1 className="text-2xl font-medium mb-4">Sign in</h1>
          
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="email" className="form-label">Email</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="form-input"
                autoComplete="email"
              />
            </div>
            
            <div className="mb-4">
              <div className="flex justify-between">
                <label htmlFor="password" className="form-label">Password</label>
              </div>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-input"
                autoComplete="current-password"
              />
            </div>
            
            <button 
              type="submit" 
              className="w-full py-2 bg-amazon-yellow hover:bg-amazon-yellow-hover rounded mb-4"
              disabled={isLoading}
            >
              {isLoading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>
          
          <div className="mt-4 text-sm">
            <p>By continuing, you agree to Amazon's <a href="#" className="text-amazon-teal hover:underline">Conditions of Use</a> and <a href="#" className="text-amazon-teal hover:underline">Privacy Notice</a>.</p>
          </div>
          
          <div className="mt-4 flex items-center">
            <input type="checkbox" id="keep-signed-in" className="mr-2" />
            <label htmlFor="keep-signed-in" className="text-sm">Keep me signed in</label>
          </div>
        </div>
        
        <div className="mt-4 text-center">
          <div className="relative py-2">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center">
              <span className="bg-gray-100 px-2 text-sm text-gray-500">New to Amazon?</span>
            </div>
          </div>
          
          <Link 
            to="/register" 
            className="block w-full py-2 bg-gray-200 hover:bg-gray-300 rounded mt-2 text-gray-800"
          >
            Create your Amazon account
          </Link>
        </div>
        
        <div className="mt-4 text-center">
          <button
            className="text-amazon-orange hover:underline text-sm"
            onClick={() => setShowReset(!showReset)}
          >
            Mot de passe oublié ?
          </button>
        </div>
        
        {showReset && (
          <div className="mt-6 bg-white rounded shadow p-6 max-w-sm mx-auto">
            <h2 className="text-lg font-bold mb-2">Réinitialiser le mot de passe</h2>
            <form onSubmit={handleResetPassword} className="space-y-4">
              <input
                type="email"
                className="form-input w-full"
                placeholder="Votre email"
                value={resetEmail}
                onChange={e => setResetEmail(e.target.value)}
                required
              />
              <button
                type="submit"
                className="btn btn-primary w-full"
                disabled={resetLoading}
              >
                {resetLoading ? 'Envoi...' : 'Envoyer le lien'}
              </button>
            </form>
            {resetMsg && <div className="mt-2 text-sm text-gray-600">{resetMsg}</div>}
          </div>
        )}
      </div>
    </div>
  );
};

export default LoginPage;