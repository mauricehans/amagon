import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Star, ChevronDown, ChevronUp, Check, Truck, ShieldCheck, Info } from 'lucide-react';
import { mockProducts } from '../data/mockData';
import { useCart } from '../context/CartContext';
import ProductGrid from '../components/home/ProductGrid';

const ProductDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { addItem } = useCart();
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState(0);
  const [expandedSection, setExpandedSection] = useState<string | null>('description');
  
  // Find the product by ID
  const product = mockProducts.find(p => p.id === id);
  
  if (!product) {
    return (
      <div className="container-custom py-12 text-center">
        <h1 className="text-2xl font-bold mb-4">Product Not Found</h1>
        <p className="mb-6">Sorry, the product you are looking for doesn't exist.</p>
        <Link to="/" className="btn btn-primary">
          Return to Home
        </Link>
      </div>
    );
  }

  const handleAddToCart = () => {
    addItem({
      id: product.id,
      title: product.title,
      price: product.price,
      image: product.image
    });
  };

  const toggleSection = (section: string) => {
    if (expandedSection === section) {
      setExpandedSection(null);
    } else {
      setExpandedSection(section);
    }
  };

  // Mock data for product images
  const productImages = [
    product.image,
    'https://images.pexels.com/photos/1294886/pexels-photo-1294886.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    'https://images.pexels.com/photos/1667088/pexels-photo-1667088.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
  ];

  // Render rating stars
  const renderRating = () => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      if (i <= product.rating) {
        stars.push(<Star key={i} size={18} className="fill-amazon-warning text-amazon-warning" />);
      } else {
        stars.push(<Star key={i} size={18} className="text-gray-300" />);
      }
    }
    return (
      <div className="flex items-center">
        <div className="flex mr-2">
          {stars}
        </div>
        <a href="#reviews" className="text-amazon-teal hover:underline">
          {product.reviewCount} ratings
        </a>
      </div>
    );
  };

  return (
    <div className="bg-white">
      <div className="container-custom py-8">
        {/* Breadcrumb */}
        <nav className="flex text-sm mb-6">
          <Link to="/" className="text-amazon-teal hover:underline">Home</Link>
          <span className="mx-2">/</span>
          <Link to="/category/electronics" className="text-amazon-teal hover:underline">Electronics</Link>
          <span className="mx-2">/</span>
          <span className="text-gray-500 truncate">{product.title}</span>
        </nav>

        {/* Product Details */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Product Images */}
          <div className="col-span-1">
            <div className="sticky top-4">
              <div className="flex">
                {/* Thumbnail images */}
                <div className="hidden md:flex flex-col gap-2 mr-2">
                  {productImages.map((img, index) => (
                    <div 
                      key={index}
                      className={`w-16 h-16 border-2 cursor-pointer ${selectedImage === index ? 'border-amazon-orange' : 'border-gray-200'}`}
                      onClick={() => setSelectedImage(index)}
                    >
                      <img 
                        src={img} 
                        alt={`${product.title} - view ${index + 1}`} 
                        className="w-full h-full object-contain"
                      />
                    </div>
                  ))}
                </div>
                
                {/* Main product image */}
                <div className="flex-1 border border-gray-200 rounded">
                  <img 
                    src={productImages[selectedImage]} 
                    alt={product.title}
                    className="w-full h-auto object-contain"
                  />
                </div>
              </div>
              
              {/* Mobile thumbnails */}
              <div className="flex justify-center gap-2 mt-2 md:hidden">
                {productImages.map((_, index) => (
                  <button 
                    key={index}
                    className={`w-2 h-2 rounded-full ${selectedImage === index ? 'bg-amazon-orange' : 'bg-gray-300'}`}
                    onClick={() => setSelectedImage(index)}
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Product Info */}
          <div className="col-span-1">
            <h1 className="text-xl md:text-2xl font-medium mb-2">{product.title}</h1>
            
            <div className="mb-4">
              {renderRating()}
            </div>
            
            <div className="border-b border-gray-200 pb-4 mb-4">
              <div className="text-sm mb-2">List Price: <span className="line-through">${(product.price * 1.2).toFixed(2)}</span></div>
              <div className="flex items-baseline">
                <span className="text-amazon-error text-2xl font-bold">${product.price.toFixed(2)}</span>
                <span className="ml-2 text-amazon-success">Save 20%</span>
              </div>
            </div>
            
            {/* Available colors */}
            <div className="mb-4">
              <h3 className="font-medium mb-2">Color:</h3>
              <div className="flex gap-2">
                <button className="w-10 h-10 border-2 border-amazon-orange rounded-full bg-black"></button>
                <button className="w-10 h-10 border border-gray-300 rounded-full bg-white"></button>
                <button className="w-10 h-10 border border-gray-300 rounded-full bg-gray-200"></button>
                <button className="w-10 h-10 border border-gray-300 rounded-full bg-blue-500"></button>
              </div>
            </div>
            
            {/* Product description */}
            <div className="mb-4">
              <button 
                className="w-full flex justify-between items-center py-2 border-b border-gray-200"
                onClick={() => toggleSection('description')}
              >
                <span className="font-medium">About this item</span>
                {expandedSection === 'description' ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
              </button>
              
              {expandedSection === 'description' && (
                <div className="py-3 text-sm">
                  <ul className="list-disc pl-5 space-y-2">
                    <li>High-performance product with advanced features for optimal user experience</li>
                    <li>Energy efficient design with long battery life</li>
                    <li>Premium build quality with durable materials</li>
                    <li>Compatible with a wide range of devices and accessories</li>
                    <li>Intuitive interface that's easy to use for all skill levels</li>
                  </ul>
                </div>
              )}
            </div>
            
            {/* Product specs */}
            <div className="mb-4">
              <button 
                className="w-full flex justify-between items-center py-2 border-b border-gray-200"
                onClick={() => toggleSection('specs')}
              >
                <span className="font-medium">Technical Details</span>
                {expandedSection === 'specs' ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
              </button>
              
              {expandedSection === 'specs' && (
                <div className="py-3 text-sm">
                  <div className="grid grid-cols-2 gap-2">
                    <div className="text-gray-600">Brand</div>
                    <div>Amazon</div>
                    
                    <div className="text-gray-600">Model</div>
                    <div>A12345</div>
                    
                    <div className="text-gray-600">Weight</div>
                    <div>0.5 pounds</div>
                    
                    <div className="text-gray-600">Dimensions</div>
                    <div>5.5 x 2.5 x 0.4 inches</div>
                    
                    <div className="text-gray-600">Warranty</div>
                    <div>1 year limited</div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Purchase Box */}
          <div className="col-span-1">
            <div className="border border-gray-200 rounded p-4 sticky top-4">
              <div className="text-amazon-error text-xl font-bold mb-2">
                ${product.price.toFixed(2)}
              </div>
              
              <div className="text-amazon-success text-sm mb-4">
                FREE delivery <span className="font-bold">Tomorrow</span> if you order within 12 hrs 30 mins
              </div>
              
              <div className="flex items-center mb-4">
                <MapPin size={16} className="text-amazon-teal mr-2" />
                <div>
                  <div className="text-sm">Deliver to France</div>
                </div>
              </div>
              
              <div className="text-amazon-success font-bold text-lg mb-4">
                In Stock
              </div>
              
              <div className="flex items-center mb-4">
                <label htmlFor="quantity" className="text-sm mr-2">Quantity:</label>
                <select 
                  id="quantity"
                  value={quantity}
                  onChange={(e) => setQuantity(parseInt(e.target.value))}
                  className="border border-gray-300 rounded p-1"
                >
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                    <option key={num} value={num}>{num}</option>
                  ))}
                </select>
              </div>
              
              <button 
                onClick={handleAddToCart}
                className="w-full py-2 mb-2 rounded bg-amazon-yellow hover:bg-amazon-yellow-hover"
              >
                Add to Cart
              </button>
              
              <button className="w-full py-2 mb-4 rounded bg-amazon-orange text-white hover:bg-amazon-orange-hover">
                Buy Now
              </button>
              
              <div className="text-sm">
                <div className="flex items-center mb-2">
                  <Check size={16} className="text-amazon-success mr-2" />
                  <span>Secure transaction</span>
                </div>
                
                <div className="flex items-center mb-2">
                  <Truck size={16} className="mr-2" />
                  <span>Ships from and sold by Amazon.com</span>
                </div>
                
                <div className="flex items-center mb-2">
                  <ShieldCheck size={16} className="mr-2" />
                  <span>Return policy: Eligible for Return, Refund or Replacement</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Customer reviews */}
        <div id="reviews" className="my-8">
          <h2 className="text-xl font-bold mb-4">Customer Reviews</h2>
          
          <div className="flex flex-col md:flex-row">
            <div className="md:w-1/3 mb-6 md:mb-0 pr-6">
              <div className="flex items-baseline mb-2">
                <span className="text-amazon-warning text-xl font-bold mr-2">{product.rating.toFixed(1)}</span>
                <span>out of 5</span>
              </div>
              
              <div className="flex mb-4">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star key={i} size={18} className={i < Math.floor(product.rating) ? "fill-amazon-warning text-amazon-warning" : "text-gray-300"} />
                ))}
              </div>
              
              <div className="text-sm text-gray-600 mb-4">{product.reviewCount} global ratings</div>
              
              <div className="space-y-2">
                {[5, 4, 3, 2, 1].map((star) => (
                  <div key={star} className="flex items-center">
                    <a href="#" className="text-amazon-teal hover:underline mr-2">{star} star</a>
                    <div className="flex-1 bg-gray-200 h-4 rounded-full overflow-hidden mr-2">
                      <div 
                        className="bg-amazon-warning h-full" 
                        style={{ width: `${star === 5 ? 70 : star === 4 ? 20 : star === 3 ? 5 : star === 2 ? 3 : 2}%` }}
                      ></div>
                    </div>
                    <span className="text-sm">{star === 5 ? 70 : star === 4 ? 20 : star === 3 ? 5 : star === 3 ? 3 : 2}%</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="md:w-2/3">
              <div className="border-b border-gray-200 pb-6 mb-6">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-bold">Light weight and comfortable to use</h3>
                  <div className="flex">
                    {Array.from({ length: 5 }).map((_, i) => (
                      <Star key={i} size={16} className={i < 5 ? "fill-amazon-warning text-amazon-warning" : "text-gray-300"} />
                    ))}
                  </div>
                </div>
                
                <div className="text-sm text-gray-600 mb-2">Reviewed in the United States on July 10, 2025</div>
                <div className="mb-2">Verified Purchase</div>
                <p className="text-sm">
                  This product exceeds all my expectations! The quality is outstanding, and it works perfectly for what I need. 
                  I would highly recommend this to anyone looking for a reliable and high-performance device.
                </p>
              </div>
              
              <div className="border-b border-gray-200 pb-6 mb-6">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-bold">Great value for the money</h3>
                  <div className="flex">
                    {Array.from({ length: 5 }).map((_, i) => (
                      <Star key={i} size={16} className={i < 4 ? "fill-amazon-warning text-amazon-warning" : "text-gray-300"} />
                    ))}
                  </div>
                </div>
                
                <div className="text-sm text-gray-600 mb-2">Reviewed in the United States on June 25, 2025</div>
                <div className="mb-2">Verified Purchase</div>
                <p className="text-sm">
                  I'm very satisfied with this purchase. The product arrived quickly and was easy to set up. 
                  The performance is solid, and the price point makes it an excellent value compared to similar products.
                </p>
              </div>
              
              <a href="#" className="btn btn-outline">See all reviews</a>
            </div>
          </div>
        </div>
        
        {/* Similar products */}
        <div className="my-8">
          <h2 className="text-xl font-bold mb-4">Products related to this item</h2>
          <ProductGrid limit={6} />
        </div>
      </div>
    </div>
  );
};

export default ProductDetailPage;