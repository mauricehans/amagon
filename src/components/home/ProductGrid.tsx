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
    const fetchAllProducts = async () => {
      try {
        setLoading(true);
        setError(null);
        
        let allProducts: Product[] = [];
        
        // Récupérer les produits du service produit (port 8004)
        try {
          const productResponse = await fetch('http://localhost:8004/api/products/');
          if (productResponse.ok) {
            const productData = await productResponse.json();
            console.log('Product service data:', productData);
            
            if (Array.isArray(productData)) {
              // Adapter les produits du service produit au format attendu
              const adaptedProducts: Product[] = productData.map((p: any) => ({
                id: p.id?.toString() || '',
                name: p.name || 'Produit sans nom',
                description: p.description || '',
                price: Number(p.price) || 0,
                image_url: p.image_url || (p.images && p.images.length > 0 ? p.images[0].url : 'https://via.placeholder.com/300x300?text=No+Image'),
                category_name: p.category_name || p.category?.name || 'Autre',
                stock_quantity: p.stock_quantity || 0,
                rating: p.rating || 4.5,
                review_count: p.review_count || 12,
                images: p.images || []
              }));
              allProducts = [...allProducts, ...adaptedProducts];
            }
          }
        } catch (err) {
          console.warn('Erreur service produit:', err);
        }
        
        // Récupérer les produits du service vendeur (port 8005)
        try {
          const sellerResponse = await fetch('http://localhost:8005/api/sellers/products/');
          if (sellerResponse.ok) {
            const sellerData = await sellerResponse.json();
            console.log('Seller service data:', sellerData);
            
            if (Array.isArray(sellerData)) {
              // Adapter les produits vendeurs au format attendu
              const adaptedSellerProducts: Product[] = sellerData.map((p: any) => ({
                id: p.id?.toString() || '',
                name: p.name || 'Produit sans nom',
                description: p.description || '',
                price: Number(p.price) || 0,
                image_url: p.image_url || (p.images && p.images.length > 0 ? p.images[0].url : 'https://via.placeholder.com/300x300?text=No+Image'),
                category_name: p.category_name || p.category || 'Autre',
                stock_quantity: p.stock_quantity || 0,
                rating: p.rating || 4.5,
                review_count: p.review_count || 12,
                seller_name: p.seller_name || 'Vendeur',
                images: p.images || []
              }));
              allProducts = [...allProducts, ...adaptedSellerProducts];
            }
          }
        } catch (err) {
          console.warn('Erreur service vendeur:', err);
        }
        
        console.log('Tous les produits récupérés:', allProducts);
        
        // Si aucun produit n'est trouvé, utiliser des produits de démonstration
        if (allProducts.length === 0) {
          console.log('Aucun produit trouvé, utilisation de produits de démonstration');
          allProducts = getDemoProducts();
        }
        
        setProducts(allProducts);
        
      } catch (err) {
        console.error('Erreur générale:', err);
        setError('Erreur lors du chargement des produits');
        // Utiliser des produits de démonstration en cas d'erreur
        setProducts(getDemoProducts());
      } finally {
        setLoading(false);
      }
    };
    
    fetchAllProducts();
  }, []);

  // Produits de démonstration en cas d'échec
  const getDemoProducts = (): Product[] => {
    return [
      {
        id: 'demo-1',
        name: 'Smartphone Pro Max',
        description: 'Smartphone dernière génération avec appareil photo avancé',
        price: 999.99,
        image_url: 'https://images.pexels.com/photos/1841841/pexels-photo-1841841.jpeg?auto=compress&cs=tinysrgb&w=400',
        category_name: 'Electronics',
        stock_quantity: 10,
        rating: 4.5,
        review_count: 128,
        images: []
      },
      {
        id: 'demo-2',
        name: 'Écouteurs Sans Fil',
        description: 'Écouteurs Bluetooth avec réduction de bruit active',
        price: 199.99,
        image_url: 'https://images.pexels.com/photos/1649771/pexels-photo-1649771.jpeg?auto=compress&cs=tinysrgb&w=400',
        category_name: 'Electronics',
        stock_quantity: 25,
        rating: 4.7,
        review_count: 89,
        images: []
      },
      {
        id: 'demo-3',
        name: 'Ordinateur Portable',
        description: 'Laptop haute performance pour le travail et les jeux',
        price: 1299.99,
        image_url: 'https://images.pexels.com/photos/205421/pexels-photo-205421.jpeg?auto=compress&cs=tinysrgb&w=400',
        category_name: 'Electronics',
        stock_quantity: 8,
        rating: 4.6,
        review_count: 156,
        images: []
      },
      {
        id: 'demo-4',
        name: 'Montre Connectée',
        description: 'Smartwatch avec suivi de santé et notifications',
        price: 299.99,
        image_url: 'https://images.pexels.com/photos/437037/pexels-photo-437037.jpeg?auto=compress&cs=tinysrgb&w=400',
        category_name: 'Electronics',
        stock_quantity: 15,
        rating: 4.4,
        review_count: 203,
        images: []
      },
      {
        id: 'demo-5',
        name: 'Appareil Photo Numérique',
        description: 'Appareil photo professionnel avec objectif 18-55mm',
        price: 749.99,
        image_url: 'https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?auto=compress&cs=tinysrgb&w=400',
        category_name: 'Electronics',
        stock_quantity: 5,
        rating: 4.8,
        review_count: 67,
        images: []
      },
      {
        id: 'demo-6',
        name: 'Enceinte Bluetooth',
        description: 'Enceinte portable avec son stéréo puissant',
        price: 89.99,
        image_url: 'https://images.pexels.com/photos/1279107/pexels-photo-1279107.jpeg?auto=compress&cs=tinysrgb&w=400',
        category_name: 'Electronics',
        stock_quantity: 20,
        rating: 4.3,
        review_count: 145,
        images: []
      }
    ];
  };

  const displayProducts = limit ? products.slice(0, limit) : products;

  if (loading) {
    return (
      <section className="my-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">{title}</h2>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
          {[...Array(6)].map((_, index) => (
            <div key={index} className="bg-white p-4 rounded shadow-product animate-pulse">
              <div className="bg-gray-300 h-40 mb-3 rounded"></div>
              <div className="bg-gray-300 h-4 mb-2 rounded"></div>
              <div className="bg-gray-300 h-4 w-3/4 rounded"></div>
            </div>
          ))}
        </div>
      </section>
    );
  }

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
      
      {error && (
        <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded mb-4">
          {error} - Affichage des produits de démonstration
        </div>
      )}
      
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        {displayProducts.length === 0 ? (
          <div className="col-span-full text-center text-gray-500 py-8">
            Aucun produit disponible pour le moment.
          </div>
        ) : (
          displayProducts.map(product => (
            <ProductCard key={product.id} product={product} />
          ))
        )}
      </div>
    </section>
  );
};

export default ProductGrid;