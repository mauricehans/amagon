import { useEffect, useState } from 'react';
import axios from 'axios';
import ProductList from '../components/ProductList';

export default function HomePage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/product/product_list');
        setProducts(response.data);
      } catch (error) {
        console.error('Erreur lors de la récupération des produits:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Nos Produits</h1>
      {loading ? (
        <div>Chargement...</div>
      ) : (
        <ProductList products={products} />
      )}
    </div>
  );
}