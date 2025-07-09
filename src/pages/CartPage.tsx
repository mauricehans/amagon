import React from 'react';
import { Link } from 'react-router-dom';
import { Trash2, Check } from 'lucide-react';
import { useCart } from '../context/CartContext';
import ProductGrid from '../components/home/ProductGrid';

const CartPage: React.FC = () => {
  const { items, removeItem, updateQuantity, total, clearCart, itemCount } = useCart();
  
  if (items.length === 0) {
    return (
      <div className="container-custom py-8">
        <h1 className="text-2xl font-medium mb-6">Your Amazon Cart is empty</h1>
        
        <div className="bg-white p-6 rounded shadow-sm mb-8">
          <p className="mb-6">Your shopping cart is waiting. Give it purpose – fill it with groceries, clothing, household supplies, electronics, and more.</p>
          <Link to="/" className="btn btn-primary">
            Continue shopping
          </Link>
        </div>
        
        <div className="my-8">
          <h2 className="text-xl font-bold mb-4">Recommended for you</h2>
          <ProductGrid limit={5} />
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-100 min-h-screen">
      <div className="container-custom py-8">
        <h1 className="text-2xl font-medium mb-6">Shopping Cart</h1>
        
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Cart items */}
          <div className="lg:w-3/4">
            <div className="bg-white p-6 rounded shadow-sm mb-4">
              <div className="flex justify-between border-b border-gray-200 pb-4 mb-4">
                <h2 className="font-bold">Cart ({itemCount} items)</h2>
                <button 
                  onClick={clearCart}
                  className="text-amazon-teal hover:underline text-sm"
                >
                  Clear cart
                </button>
              </div>
              
              <div className="divide-y divide-gray-200">
                {items.map((item) => (
                  <div key={item.id} className="py-4 flex">
                    <div className="w-20 h-20 flex-shrink-0">
                      <img 
                        src={item.image_url || item.image || "https://via.placeholder.com/300x300?text=No+Image"} 
                        alt={item.name || item.title || "Product"} 
                        className="w-full h-full object-contain"
                      />
                    </div>
                    
                    <div className="ml-4 flex-grow">
                      <Link to={`/product/${item.id}`} className="font-medium hover:text-amazon-teal">
                        {item.name || item.title}
                      </Link>
                      
                      <div className="text-amazon-success text-sm mt-1">In Stock</div>
                      
                      <div className="text-amazon-error font-bold mt-1">
                        ${Number(item.price).toFixed(2)}
                      </div>
                      
                      <div className="flex items-center mt-2">
                        <select 
                          value={item.quantity}
                          onChange={(e) => updateQuantity(item.id, parseInt(e.target.value))}
                          className="border border-gray-300 rounded p-1 mr-4"
                        >
                          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                            <option key={num} value={num}>Qty: {num}</option>
                          ))}
                        </select>
                        
                        <button 
                          onClick={() => removeItem(item.id)}
                          className="text-amazon-teal hover:underline text-sm flex items-center"
                        >
                          <Trash2 size={16} className="mr-1" />
                          Remove
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="flex justify-end pt-4 border-t border-gray-200 mt-4">
                <div className="text-xl">
                  Subtotal ({itemCount} items): <span className="font-bold">${Number(total).toFixed(2)}</span>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded shadow-sm">
              <h3 className="font-bold mb-3">Saved for later (0 items)</h3>
              <p className="text-sm text-gray-600">
                You don't have any saved items right now. Items that you save for later will be moved here.
              </p>
            </div>
          </div>
          
          {/* Order summary */}
          <div className="lg:w-1/4">
            <div className="bg-white p-6 rounded shadow-sm mb-4 sticky top-4">
              <div className="text-green-600 flex items-center mb-4">
                <Check size={18} className="mr-2" />
                <span>Your order qualifies for FREE Shipping.</span>
              </div>
              
              <div className="text-xl mb-4">
                Subtotal ({itemCount} items): <span className="font-bold">${Number(total).toFixed(2)}</span>
              </div>
              
              <div className="flex items-center mb-4">
                <input type="checkbox" id="gift" className="mr-2" />
                <label htmlFor="gift">This order contains a gift</label>
              </div>
              
              <Link 
                to="/checkout" 
                className="block w-full py-2 bg-amazon-yellow hover:bg-amazon-yellow-hover text-center rounded font-medium mb-2"
              >
                Proceed to checkout
              </Link>
            </div>
            
            <div className="bg-white p-6 rounded shadow-sm">
              <h3 className="font-bold mb-3">Frequently bought together</h3>
              <div className="flex items-center border-b border-gray-200 pb-4 mb-4">
                <div className="w-20 h-20 flex-shrink-0">
                  <img 
                    src="https://images.pexels.com/photos/1279107/pexels-photo-1279107.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" 
                    alt="Accessory" 
                    className="w-full h-full object-contain"
                  />
                </div>
                <div className="ml-3">
                  <div className="font-medium text-sm">Compatible Accessory Kit</div>
                  <div className="text-amazon-error font-bold">$24.99</div>
                  <button className="text-amazon-teal hover:underline text-sm">
                    Add to Cart
                  </button>
                </div>
              </div>
              <div className="flex items-center">
                <div className="w-20 h-20 flex-shrink-0">
                  <img 
                    src="https://images.pexels.com/photos/1619651/pexels-photo-1619651.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" 
                    alt="Protection Plan" 
                    className="w-full h-full object-contain"
                  />
                </div>
                <div className="ml-3">
                  <div className="font-medium text-sm">2-Year Protection Plan</div>
                  <div className="text-amazon-error font-bold">$16.99</div>
                  <button className="text-amazon-teal hover:underline text-sm">
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="my-8">
          <h2 className="text-xl font-bold mb-4">Customers who bought items in your cart also bought</h2>
          <ProductGrid limit={5} />
        </div>
      </div>
    </div>
  );
};

export default CartPage;