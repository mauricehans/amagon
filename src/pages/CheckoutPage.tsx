import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { Check, ChevronDown, ChevronUp, CreditCard, Gift, Lock } from 'lucide-react';

const CheckoutPage: React.FC = () => {
  const { items, total, itemCount } = useCart();
  const { user, isAuthenticated } = useAuth();
  
  const [expandedSection, setExpandedSection] = useState<string>('shipping');
  const [shippingAddress, setShippingAddress] = useState({
    name: user?.name || '',
    street: '',
    city: '',
    state: '',
    zip: '',
    country: 'France'
  });

  const toggleSection = (section: string) => {
    setExpandedSection(section);
  };

  if (items.length === 0) {
    return (
      <div className="container-custom py-8 text-center">
        <h1 className="text-2xl font-medium mb-6">Your cart is empty</h1>
        <p className="mb-6">You have no items in your cart to checkout.</p>
        <Link to="/cart" className="btn btn-primary">
          Return to Cart
        </Link>
      </div>
    );
  }

  return (
    <div className="bg-gray-100 min-h-screen">
      <div className="container-custom py-8">
        <h1 className="text-2xl font-medium mb-6">Checkout</h1>
        
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Main checkout form */}
          <div className="lg:w-3/4">
            {/* Shipping address section */}
            <div className="bg-white p-6 rounded shadow-sm mb-4">
              <button 
                className="w-full flex justify-between items-center"
                onClick={() => toggleSection('shipping')}
              >
                <div className="flex items-center">
                  <div className="rounded-full bg-amazon-yellow w-6 h-6 flex items-center justify-center text-xs font-bold mr-2">
                    1
                  </div>
                  <h2 className="font-bold text-lg">Shipping address</h2>
                </div>
                {expandedSection === 'shipping' ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
              </button>
              
              {expandedSection === 'shipping' && (
                <div className="mt-4">
                  <form>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="md:col-span-2">
                        <label htmlFor="name" className="form-label">Full name</label>
                        <input 
                          type="text"
                          id="name"
                          value={shippingAddress.name}
                          onChange={(e) => setShippingAddress({...shippingAddress, name: e.target.value})}
                          className="form-input"
                        />
                      </div>
                      
                      <div className="md:col-span-2">
                        <label htmlFor="street" className="form-label">Street address</label>
                        <input 
                          type="text"
                          id="street"
                          value={shippingAddress.street}
                          onChange={(e) => setShippingAddress({...shippingAddress, street: e.target.value})}
                          className="form-input"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="city" className="form-label">City</label>
                        <input 
                          type="text"
                          id="city"
                          value={shippingAddress.city}
                          onChange={(e) => setShippingAddress({...shippingAddress, city: e.target.value})}
                          className="form-input"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="state" className="form-label">State/Province</label>
                        <input 
                          type="text"
                          id="state"
                          value={shippingAddress.state}
                          onChange={(e) => setShippingAddress({...shippingAddress, state: e.target.value})}
                          className="form-input"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="zip" className="form-label">ZIP/Postal code</label>
                        <input 
                          type="text"
                          id="zip"
                          value={shippingAddress.zip}
                          onChange={(e) => setShippingAddress({...shippingAddress, zip: e.target.value})}
                          className="form-input"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="country" className="form-label">Country</label>
                        <select 
                          id="country"
                          value={shippingAddress.country}
                          onChange={(e) => setShippingAddress({...shippingAddress, country: e.target.value})}
                          className="form-input"
                        >
                          <option value="France">France</option>
                          <option value="Germany">Germany</option>
                          <option value="United Kingdom">United Kingdom</option>
                          <option value="Italy">Italy</option>
                          <option value="Spain">Spain</option>
                        </select>
                      </div>
                    </div>
                    
                    <div className="mt-4 flex justify-end">
                      <button 
                        type="button" 
                        className="btn btn-primary"
                        onClick={() => toggleSection('payment')}
                      >
                        Continue to payment
                      </button>
                    </div>
                  </form>
                </div>
              )}
            </div>
            
            {/* Payment method section */}
            <div className="bg-white p-6 rounded shadow-sm mb-4">
              <button 
                className="w-full flex justify-between items-center"
                onClick={() => toggleSection('payment')}
              >
                <div className="flex items-center">
                  <div className="rounded-full bg-amazon-yellow w-6 h-6 flex items-center justify-center text-xs font-bold mr-2">
                    2
                  </div>
                  <h2 className="font-bold text-lg">Payment method</h2>
                </div>
                {expandedSection === 'payment' ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
              </button>
              
              {expandedSection === 'payment' && (
                <div className="mt-4">
                  <div className="border border-gray-200 rounded p-4 mb-4">
                    <div className="flex items-center mb-4">
                      <input 
                        type="radio" 
                        id="credit-card"
                        name="payment-method"
                        className="mr-2"
                        defaultChecked
                      />
                      <label htmlFor="credit-card" className="flex items-center">
                        <CreditCard size={20} className="mr-2" />
                        Credit or debit card
                      </label>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="md:col-span-2">
                        <label className="form-label">Card number</label>
                        <input 
                          type="text"
                          placeholder="1234 5678 9012 3456"
                          className="form-input"
                        />
                      </div>
                      
                      <div>
                        <label className="form-label">Expiration date</label>
                        <div className="grid grid-cols-2 gap-2">
                          <select className="form-input">
                            {Array.from({ length: 12 }, (_, i) => i + 1).map(month => (
                              <option key={month} value={month}>{month.toString().padStart(2, '0')}</option>
                            ))}
                          </select>
                          <select className="form-input">
                            {Array.from({ length: 10 }, (_, i) => new Date().getFullYear() + i).map(year => (
                              <option key={year} value={year}>{year}</option>
                            ))}
                          </select>
                        </div>
                      </div>
                      
                      <div>
                        <label className="form-label">Security code (CVV)</label>
                        <input 
                          type="text"
                          placeholder="123"
                          className="form-input"
                        />
                      </div>
                      
                      <div className="md:col-span-2">
                        <label className="form-label">Name on card</label>
                        <input 
                          type="text"
                          className="form-input"
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center text-sm mb-4">
                    <Lock size={16} className="mr-2 text-gray-500" />
                    <span>Your payment information is secure and encrypted</span>
                  </div>
                  
                  <div className="flex justify-end">
                    <button 
                      type="button" 
                      className="btn btn-primary"
                      onClick={() => toggleSection('review')}
                    >
                      Continue to review
                    </button>
                  </div>
                </div>
              )}
            </div>
            
            {/* Review section */}
            <div className="bg-white p-6 rounded shadow-sm mb-4">
              <button 
                className="w-full flex justify-between items-center"
                onClick={() => toggleSection('review')}
              >
                <div className="flex items-center">
                  <div className="rounded-full bg-amazon-yellow w-6 h-6 flex items-center justify-center text-xs font-bold mr-2">
                    3
                  </div>
                  <h2 className="font-bold text-lg">Review items and shipping</h2>
                </div>
                {expandedSection === 'review' ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
              </button>
              
              {expandedSection === 'review' && (
                <div className="mt-4">
                  <div className="border-b border-gray-200 pb-4 mb-4">
                    <h3 className="font-bold mb-3">Shipping address</h3>
                    {shippingAddress.name && (
                      <div className="text-sm">
                        <p>{shippingAddress.name}</p>
                        <p>{shippingAddress.street}</p>
                        <p>{shippingAddress.city}, {shippingAddress.state} {shippingAddress.zip}</p>
                        <p>{shippingAddress.country}</p>
                      </div>
                    )}
                  </div>
                  
                  <div className="border-b border-gray-200 pb-4 mb-4">
                    <h3 className="font-bold mb-3">Items ({itemCount})</h3>
                    
                    <div className="space-y-4">
                      {items.map((item) => (
                        <div key={item.id} className="flex">
                          <div className="w-16 h-16 flex-shrink-0">
                            <img 
                              src={item.image} 
                              alt={item.title} 
                              className="w-full h-full object-contain"
                            />
                          </div>
                          
                          <div className="ml-4">
                            <div className="font-medium">{item.title}</div>
                            <div className="text-amazon-error font-bold">${item.price.toFixed(2)}</div>
                            <div className="text-sm">Quantity: {item.quantity}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="flex items-center mb-4">
                    <Gift size={20} className="mr-2" />
                    <div>
                      <div className="font-medium">Gift options</div>
                      <a href="#" className="text-amazon-teal hover:underline text-sm">Add a gift message or gift receipt</a>
                    </div>
                  </div>
                  
                  <div className="flex justify-end">
                    <button className="btn btn-primary">
                      Place your order
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
          
          {/* Order summary */}
          <div className="lg:w-1/4">
            <div className="bg-white p-6 rounded shadow-sm sticky top-4">
              <button className="w-full bg-amazon-yellow hover:bg-amazon-yellow-hover py-2 rounded font-medium mb-4">
                Place your order
              </button>
              
              <div className="text-xs text-center mb-4">
                By placing your order, you agree to Amazon's <a href="#" className="text-amazon-teal hover:underline">privacy notice</a> and <a href="#" className="text-amazon-teal hover:underline">conditions of use</a>.
              </div>
              
              <h3 className="font-bold border-b border-gray-200 pb-2 mb-4">Order Summary</h3>
              
              <div className="space-y-2 text-sm mb-4">
                <div className="flex justify-between">
                  <span>Items ({itemCount}):</span>
                  <span>${total.toFixed(2)}</span>
                </div>
                
                <div className="flex justify-between">
                  <span>Shipping & handling:</span>
                  <span>$0.00</span>
                </div>
                
                <div className="flex justify-between">
                  <span>Total before tax:</span>
                  <span>${total.toFixed(2)}</span>
                </div>
                
                <div className="flex justify-between">
                  <span>Estimated tax:</span>
                  <span>${(total * 0.10).toFixed(2)}</span>
                </div>
              </div>
              
              <div className="flex justify-between font-bold text-lg border-t border-gray-200 pt-2">
                <span>Order total:</span>
                <span>${(total * 1.10).toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CheckoutPage;