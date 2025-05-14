import React from 'react';
import ProductCard from '../product/ProductCard';
import { mockProducts } from '../../data/mockData';

interface ProductGridProps {
  title: string;
  viewAllLink?: string;
  products?: typeof mockProducts;
  limit?: number;
}

const ProductGrid: React.FC<ProductGridProps> = ({ 
  title, 
  viewAllLink, 
  products = mockProducts,
  limit
}) => {
  const displayProducts = limit ? products.slice(0, limit) : products;

  return (
    <section className="my-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">{title}</h2>
        {viewAllLink && (
          <a href={viewAllLink} className="text-amazon-teal hover:underline text-sm">
            View all
          </a>
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