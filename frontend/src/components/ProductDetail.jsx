import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

export default function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/product/product_detail/${id}`);
        setProduct(response.data);
      } catch (error) {
        console.error('Erreur lors de la récupération du produit:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  if (loading) return <div>Chargement...</div>;
  if (!product) return <div>Produit non trouvé</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">{product.name}</h1>
      <div className="grid md:grid-cols-2 gap-8">
        <img src={product.image} alt={product.name} className="rounded-lg" />
        <div>
          <p className="text-xl mb-4">{product.description}</p>
          <p className="text-2xl font-bold">{product.price} €</p>
          <button className="mt-4 bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700">
            Ajouter au panier
          </button>
        </div>
      </div>
    </div>
  );
}