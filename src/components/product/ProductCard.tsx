import React from 'react';
import { Link } from 'react-router-dom';
import { Star } from 'lucide-react';
import { useCart } from '../../context/CartContext';

interface ProductCardProps {
  product: {
    id: string;
    title: string;
    price: number;
    image: string;
    rating: number;
    reviewCount: number;
    isPrime?: boolean;
  };
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const { addItem } = useCart();

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    addItem({
      id: product.id,
      title: product.title,
      price: product.price,
      image: product.image
    });
  };

  // Format price to show 2 decimal places
  const formattedPrice = product.price.toFixed(2);

  // Render rating stars
  const renderRating = () => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      if (i <= product.rating) {
        stars.push(<Star key={i} size={16} className="fill-amazon-warning text-amazon-warning" />);
      } else {
        stars.push(<Star key={i} size={16} className="text-gray-300" />);
      }
    }
    return (
      <div className="flex items-center">
        <div className="flex mr-1">
          {stars}
        </div>
        <span className="text-xs text-gray-500">({product.reviewCount})</span>
      </div>
    );
  };

  return (
    <div className="product-card group">
      <Link to={`/product/${product.id}`} className="block">
        <div className="relative pb-[100%] mb-3 bg-white overflow-hidden">
          <img 
            src={product.image} 
            alt={product.title} 
            className="absolute top-0 left-0 w-full h-full object-contain transition-transform group-hover:scale-105"
          />
        </div>
        
        <h3 className="text-sm font-medium line-clamp-2 mb-1 min-h-[40px]">{product.title}</h3>
        
        {renderRating()}
        
        <div className="mt-2">
          <span className="text-amazon-error font-bold">
            ${formattedPrice}
          </span>
        </div>
        
        {product.isPrime && (
          <div className="mt-1 flex items-center">
            <span className="text-xs px-1 bg-amazon-blue text-white font-bold rounded">Prime</span>
            <span className="text-xs text-gray-500 ml-1">FREE Delivery</span>
          </div>
        )}
        
        <button 
          onClick={handleAddToCart}
          className="mt-3 w-full py-1 bg-amazon-yellow hover:bg-amazon-yellow-hover text-black text-sm font-medium rounded transition-colors"
        >
          Add to Cart
        </button>
      </Link>
    </div>
  );
};

export default ProductCard;