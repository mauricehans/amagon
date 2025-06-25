import React, { useState, useEffect } from 'react';
import ProductCard from '../product/ProductCard';
import { Product } from '../../types';
import { Link } from 'react-router-dom';

interface ProductGridProps {
  title: string;
  viewAllLink?: string;
  limit?: number;
}

const MOCK_PRODUCTS: Product[] = Array.from({ length: 10 }).map((_, i) => ({
  id: i + 1,
  name: `Mock Product ${i + 1}`,
  description: 'This is a mock product for display.',
  price: 9.99 + i,
  image_url: `https://picsum.photos/seed/mock${i + 1}/300/300`,
  rating: 4 + (i % 2) * 0.5,
  review_count: 10 + i,
  category_name: 'Mock Category',
  stock_quantity: 10 + i,
  images: [
    { url: `https://picsum.photos/seed/mock${i + 1}/300/300`, is_primary: true }
  ],
  sku: `MOCKSKU${i + 1}`,
  weight: 1.0 + i * 0.1,
  dimensions: { length: 10, width: 5, height: 2 },
  is_active: true,
  created_at: new Date().toISOString()
}));

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
        const response = await fetch('http://localhost:8004/api/products/');
        if (!response.ok) {
          setProducts(MOCK_PRODUCTS);
          setError(null);
          return;
        }
        const data = await response.json();
        setProducts(data.length ? data : MOCK_PRODUCTS);
      } catch (err) {
        setProducts(MOCK_PRODUCTS);
        setError(null);
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
        {displayProducts.map(product => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </section>
  );
};

export default ProductGrid;