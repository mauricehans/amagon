import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, ShoppingCart, User, Menu, X, MapPin, Store, MessageCircle } from 'lucide-react';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import SupportModal from '../support/SupportModal';

const Header: React.FC = () => {
  const { itemCount } = useCart();
  const { user, isAuthenticated, logout } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSupportModalOpen, setIsSupportModalOpen] = useState(false);
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const openSupportModal = () => {
    setIsSupportModalOpen(true);
  };

  return (
    <>
      <header className="bg-amazon-blue-dark text-white">
        <div className="container-custom mx-auto">
          {/* Top header */}
          <div className="flex items-center justify-between py-2">
            {/* Logo */}
            <div className="flex items-center">
              <Link to="/" className="mr-4">
                <h1 className="text-2xl font-bold tracking-wide">amagon</h1>
              </Link>

              {/* Location */}
              <div className="hidden md:flex items-center text-sm">
                <MapPin size={18} className="mr-1" />
                <div>
                  <div className="text-gray-300 text-xs">Deliver to</div>
                  <div className="font-bold">France</div>
                </div>
              </div>
            </div>

            {/* Search bar */}
            <form onSubmit={handleSearch} className="flex-grow max-w-3xl mx-4 hidden md:flex">
              <div className="relative w-full">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search products..."
                  className="w-full py-2 px-4 text-black rounded-l-md focus:outline-none"
                />
                <button 
                  type="submit" 
                  className="absolute right-0 top-0 h-full bg-amazon-yellow hover:bg-amazon-yellow-hover px-4 rounded-r-md"
                >
                  <Search size={20} className="text-black" />
                </button>
              </div>
            </form>

            {/* Right navigation */}
            <div className="flex items-center space-x-4">
              {/* Support button */}
              <button 
                onClick={openSupportModal}
                className="hidden md:flex items-center text-sm hover:text-amazon-yellow"
              >
                <MessageCircle size={18} className="mr-1" />
                <div>
                  <div className="text-gray-300 text-xs">Besoin d'aide ?</div>
                  <div className="font-bold">Support</div>
                </div>
              </button>

              {/* Seller link */}
              <Link to="/seller/login" className="hidden md:flex items-center text-sm hover:text-amazon-yellow">
                <Store size={18} className="mr-1" />
                <div>
                  <div className="text-gray-300 text-xs">Sell on</div>
                  <div className="font-bold">Amagon</div>
                </div>
              </Link>

              {/* Account */}
              <div className="hidden md:block">
                {isAuthenticated ? (
                  <div className="group relative">
                    <Link to="/account" className="text-sm">
                      <div className="text-gray-300 text-xs">Hello, {user?.name}</div>
                      <div className="font-bold">Account & Lists</div>
                    </Link>
                    <div className="absolute z-10 hidden bg-white text-black rounded-md shadow-lg py-2 w-48 group-hover:block right-0 mt-1">
                      <Link to="/account" className="block px-4 py-2 hover:bg-gray-100">Your Account</Link>
                      <Link to="/orders" className="block px-4 py-2 hover:bg-gray-100">Your Orders</Link>
                      <button onClick={openSupportModal} className="w-full text-left px-4 py-2 hover:bg-gray-100">Support</button>
                      <button onClick={logout} className="w-full text-left px-4 py-2 hover:bg-gray-100 text-amazon-blue">Sign Out</button>
                    </div>
                  </div>
                ) : (
                  <Link to="/login" className="text-sm">
                    <div className="text-gray-300 text-xs">Hello, sign in</div>
                    <div className="font-bold">Account & Lists</div>
                  </Link>
                )}
              </div>

              {/* Orders */}
              <Link to="/orders" className="hidden md:block text-sm">
                <div className="text-gray-300 text-xs">Returns</div>
                <div className="font-bold">& Orders</div>
              </Link>

              {/* Cart */}
              <Link to="/cart" className="flex items-center">
                <div className="relative">
                  <ShoppingCart size={24} />
                  <span className="absolute -top-2 -right-2 bg-amazon-orange text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                    {itemCount}
                  </span>
                </div>
                <span className="ml-1 font-bold hidden md:inline">Cart</span>
              </Link>

              {/* Mobile menu button */}
              <button 
                className="md:hidden"
                onClick={toggleMenu}
              >
                {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
              </button>
            </div>
          </div>

          {/* Bottom header - categories (desktop) */}
          <div className="hidden md:flex items-center bg-amazon-blue py-1 text-sm">
            <Link to="/all-products" className="flex items-center mr-3 hover:text-amazon-yellow">
              <Menu size={18} className="mr-1" />
              All
            </Link>
            <nav className="flex space-x-4">
              <Link to="/category/electronics" className="hover:text-amazon-yellow">Electronics</Link>
              <Link to="/category/books" className="hover:text-amazon-yellow">Books</Link>
              <Link to="/category/home-kitchen" className="hover:text-amazon-yellow">Home & Kitchen</Link>
              <Link to="/category/fashion" className="hover:text-amazon-yellow">Fashion</Link>
              <Link to="/category/toys-games" className="hover:text-amazon-yellow">Toys & Games</Link>
              <Link to="/deals" className="font-bold text-amazon-yellow hover:underline">Today's Deals</Link>
              <Link to="/seller/login" className="font-bold text-amazon-orange hover:underline">Sell on Amagon</Link>
              <button onClick={openSupportModal} className="font-bold text-green-400 hover:underline">Support</button>
            </nav>
          </div>

          {/* Mobile search - shown on small screens */}
          <div className="md:hidden py-2">
            <form onSubmit={handleSearch} className="flex w-full">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search products..."
                className="w-full py-2 px-3 text-black rounded-l-md focus:outline-none text-sm"
              />
              <button 
                type="submit" 
                className="bg-amazon-yellow hover:bg-amazon-yellow-hover px-3 rounded-r-md"
              >
                <Search size={18} className="text-black" />
              </button>
            </form>
          </div>
        </div>

        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden fixed inset-0 z-50 bg-black bg-opacity-50">
            <div className="h-full w-4/5 max-w-xs bg-white text-black overflow-y-auto">
              <div className="bg-amazon-blue-dark text-white p-4 flex items-center">
                {isAuthenticated ? (
                  <div className="flex items-center">
                    <User size={24} className="mr-2" />
                    <div>
                      <div className="font-bold">Hello, {user?.name}</div>
                    </div>
                  </div>
                ) : (
                  <Link to="/login" className="flex items-center" onClick={() => setIsMenuOpen(false)}>
                    <User size={24} className="mr-2" />
                    <div className="font-bold">Sign In</div>
                  </Link>
                )}
                <button onClick={toggleMenu} className="ml-auto">
                  <X size={24} />
                </button>
              </div>
              
              <div className="p-4">
                <h2 className="text-lg font-bold border-b pb-2 mb-3">Shop By Department</h2>
                <nav className="space-y-3">
                  <Link to="/category/electronics" className="block" onClick={() => setIsMenuOpen(false)}>Electronics</Link>
                  <Link to="/category/books" className="block" onClick={() => setIsMenuOpen(false)}>Books</Link>
                  <Link to="/category/home" className="block" onClick={() => setIsMenuOpen(false)}>Home & Kitchen</Link>
                  <Link to="/category/fashion" className="block" onClick={() => setIsMenuOpen(false)}>Fashion</Link>
                  <Link to="/category/toys" className="block" onClick={() => setIsMenuOpen(false)}>Toys & Games</Link>
                  <Link to="/deals" className="block font-bold text-amazon-orange" onClick={() => setIsMenuOpen(false)}>Today's Deals</Link>
                </nav>
                
                <h2 className="text-lg font-bold border-b pb-2 mb-3 mt-6">Sell</h2>
                <nav className="space-y-3">
                  <Link to="/seller/login" className="block text-amazon-orange font-medium" onClick={() => setIsMenuOpen(false)}>Seller Login</Link>
                  <Link to="/seller/register" className="block" onClick={() => setIsMenuOpen(false)}>Become a Seller</Link>
                </nav>
                
                <h2 className="text-lg font-bold border-b pb-2 mb-3 mt-6">Help & Support</h2>
                <nav className="space-y-3">
                  <button 
                    onClick={() => {
                      setIsMenuOpen(false);
                      openSupportModal();
                    }} 
                    className="block text-green-600 font-medium"
                  >
                    Contact Support
                  </button>
                </nav>
                
                <h2 className="text-lg font-bold border-b pb-2 mb-3 mt-6">Your Account</h2>
                <nav className="space-y-3">
                  <Link to="/account" className="block" onClick={() => setIsMenuOpen(false)}>Your Account</Link>
                  <Link to="/orders" className="block" onClick={() => setIsMenuOpen(false)}>Your Orders</Link>
                  {isAuthenticated && (
                    <button 
                      onClick={() => {
                        logout();
                        setIsMenuOpen(false);
                      }} 
                      className="block text-amazon-blue"
                    >
                      Sign Out
                    </button>
                  )}
                </nav>
              </div>
            </div>
          </div>
        )}
      </header>

      {/* Support Modal */}
      <SupportModal 
        isOpen={isSupportModalOpen}
        onClose={() => setIsSupportModalOpen(false)}
        userType="user"
      />
    </>
  );
};

export default Header;