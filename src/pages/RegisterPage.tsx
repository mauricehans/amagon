import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const RegisterPage: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!name || !email || !password || !confirmPassword) {
      setError('Please fill out all fields');
      return;
    }
    
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }
    
    try {
      setIsLoading(true);
      setError(null);
      await register(email, password, name);
      navigate('/');
    } catch (err) {
      setError('An error occurred during registration');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-sm mx-auto">
        <Link to="/" className="block text-center mb-6">
          <h1 className="text-3xl font-bold tracking-wide">amazon</h1>
        </Link>
        
        <div className="bg-white p-6 rounded shadow-sm border border-gray-200">
          <h1 className="text-2xl font-medium mb-4">Create account</h1>
          
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="name" className="form-label">Your name</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="form-input"
                placeholder="First and last name"
                autoComplete="name"
              />
            </div>
            
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
              <label htmlFor="password" className="form-label">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-input"
                placeholder="At least 6 characters"
                autoComplete="new-password"
              />
              <p className="text-xs text-gray-500 mt-1">Passwords must be at least 6 characters.</p>
            </div>
            
            <div className="mb-4">
              <label htmlFor="confirmPassword" className="form-label">Re-enter password</label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="form-input"
                autoComplete="new-password"
              />
            </div>
            
            <button 
              type="submit" 
              className="w-full py-2 bg-amazon-yellow hover:bg-amazon-yellow-hover rounded mb-4"
              disabled={isLoading}
            >
              {isLoading ? 'Creating your account...' : 'Create your Amazon account'}
            </button>
          </form>
          
          <div className="mt-4 text-sm">
            <p>By creating an account, you agree to Amazon's <a href="#" className="text-amazon-teal hover:underline">Conditions of Use</a> and <a href="#" className="text-amazon-teal hover:underline">Privacy Notice</a>.</p>
          </div>
        </div>
        
        <div className="mt-4 text-center">
          <div className="text-sm">
            Already have an account? <Link to="/login" className="text-amazon-teal hover:underline">Sign in</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;