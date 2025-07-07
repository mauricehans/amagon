import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import ProductCard from '../components/product/ProductCard';
import { Product, Category } from '../types';

const CategoryPage: React.FC = () => {
  const { categoryName } = useParams<{ categoryName: string }>();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [category, setCategory] = useState<Category | null>(null);

  // Function to convert URL slug to category name
  const getCategoryNameFromSlug = (slug: string) => {
    switch (slug) {
      case 'home-kitchen':
        return 'Home & Kitchen';
      case 'toys-games':
        return 'Toys & Games';
      default:
        return slug.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    }
  };

  const displayCategoryName = getCategoryNameFromSlug(categoryName || '');

  useEffect(() => {
    const fetchCategoryAndProducts = async () => {
      setLoading(true);
      setError(null);
      try {
        let categories: Category[] = [];
        const cachedCategories = localStorage.getItem('amagon_categories');

        if (cachedCategories) {
          categories = JSON.parse(cachedCategories);
        } else {
          const categoriesResponse = await fetch('http://localhost:8004/api/categories/');
          if (!categoriesResponse.ok) {
            throw new Error('Failed to fetch categories.');
          }
          categories = await categoriesResponse.json();
          localStorage.setItem('amagon_categories', JSON.stringify(categories));
        }

        const foundCategory = categories.find(cat => cat.name.toLowerCase() === displayCategoryName.toLowerCase());

        if (foundCategory) {
          setCategory(foundCategory);
          const productsResponse = await fetch(`http://localhost:8004/api/products/category/${foundCategory.id}/`);
          if (!productsResponse.ok) {
            throw new Error(`Failed to fetch products for category ${displayCategoryName}.`);
          }
          const data: Product[] = await productsResponse.json();
          setProducts(data);
        } else {
          setError(`Category '${displayCategoryName}' not found.`);
          setProducts([]);
        }
      } catch (err: any) {
        setError(err.message || 'An unknown error occurred.');
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCategoryAndProducts();
  }, [categoryName, displayCategoryName]);

  if (loading) return <div className="container mx-auto px-4 py-8">Loading products...</div>;
  if (error) return <div className="container mx-auto px-4 py-8 text-red-500">Error: {error}</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">
        {category ? category.name : displayCategoryName} Products
      </h1>
      {products.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      ) : (
        <p>No products found for this category.</p>
      )}
    </div>
  );
};

export default CategoryPage;
