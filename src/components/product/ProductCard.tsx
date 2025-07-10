import React from 'react';
import { Link } from 'react-router-dom';
import { Star } from 'lucide-react';
import { useCart } from '../../context/CartContext';
import { Product } from '../../types';

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const { addItem } = useCart();

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    addItem({
      id: product.id,
      name: product.name,
      price: product.price,
      image_url: product.image_url
    });
  };

  // Format price to show 2 decimal places
  const formattedPrice = Number(product.price || 0).toFixed(2);

  // Render rating stars
  const renderRating = () => {
    const stars = [];
    const rating = product.rating || 4.5;
    for (let i = 1; i <= 5; i++) {
      if (i <= rating) {
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
        <span className="text-xs text-gray-500">({product.review_count || 0})</span>
      </div>
    );
  };

  // Déterminer l'image principale
  let mainImage = "";
  if (product.images && product.images.length > 0) {
    const primary = product.images.find(img => img.is_primary);
    mainImage = primary ? primary.url : product.images[0].url;
  } else if (product.image_url) {
    mainImage = product.image_url;
  } else {
    mainImage = "https://via.placeholder.com/300x300?text=No+Image";
  }

  // Vérifier que l'image est valide
  if (!mainImage || mainImage === 'undefined' || mainImage === 'null') {
    mainImage = "https://via.placeholder.com/300x300?text=No+Image";
  }

  return (
    <div className="product-card group">
      <Link to={`/product/${product.id}`} className="block">
        <div className="relative pb-[100%] mb-3 bg-white overflow-hidden">
          <img 
            src={mainImage}
            alt={product.name || 'Produit'} 
            className="absolute top-0 left-0 w-full h-full object-contain transition-transform group-hover:scale-105"
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.src = "https://via.placeholder.com/300x300?text=No+Image";
            }}
          />
        </div>
        
        <h3 className="text-sm font-medium line-clamp-2 mb-1 min-h-[40px]">
          {product.name || 'Produit sans nom'}
        </h3>
        
        {product.seller_name && (
          <p className="text-xs text-gray-500 mb-1">Vendu par {product.seller_name}</p>
        )}
        
        {renderRating()}
        
        <div className="mt-2">
          <span className="text-amazon-error font-bold">
            ${formattedPrice}
          </span>
        </div>
      </Link>
      <button 
        onClick={handleAddToCart}
        className="mt-3 w-full py-1 bg-amazon-yellow hover:bg-amazon-yellow-hover text-black text-sm font-medium rounded transition-colors"
      >
        Add to Cart
      </button>
    </div>
  );
};

export default ProductCard;