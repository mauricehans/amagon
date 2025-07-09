import React, { useState, useEffect } from 'react';
import ProductCard from '../product/ProductCard';
import { Product } from '../../types';
import { Link } from 'react-router-dom';

interface ProductGridProps {
  title: string;
  viewAllLink?: string;
  limit?: number;
}

const ProductGrid: React.FC<ProductGridProps> = ({ 
  title, 
  viewAllLink, 
  limit 
}) => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch('http://localhost:8005/api/products/');
        if (!response.ok) {
          setError('Failed to fetch products.');
          setProducts([]);
          return;
        }
        const data = await response.json();
        setProducts(data);
      } catch (err) {
        setError('Failed to fetch products.');
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, []);

  const displayProducts = limit ? products.slice(0, limit) : products;

  if (loading) return <div>Loading products...</div>;
  if (error) return <div className="text-red-500">Error: {error}</div>;

  return (
    <section className="my-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">{title}</h2>
        {viewAllLink && (
          <Link to={viewAllLink} className="text-amazon-teal hover:underline text-sm">
            View all
          </Link>
        )}
      </div>
      
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        {displayProducts.length === 0 ? (
          <div className="col-span-full text-center text-gray-500">No products found.</div>
        ) : (
          displayProducts.map(product => (
            <ProductCard key={product.id} product={product} />
          ))
        )}
      </div>
      {/* Debug: Affiche un message si une image n'est pas trouvée */}
      {/* {displayProducts.some(p => !p.image_url && (!p.images || p.images.length === 0)) && (
        <div className="text-red-500 mt-2">Attention : Certains produits n'ont pas d'image valide.</div>
      )} */}
    </section>
  );
};

export default ProductGrid;