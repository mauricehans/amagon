export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  image_url: string;
  category_name: string;
  stock_quantity: number;
  rating: number;
  review_count: number;
  seller_name?: string; // Nom du vendeur (optionnel, pour les produits vendeurs)
  images?: Array<{url: string; is_primary: boolean}>; // Images du produit
}

export interface CartItem {
  id: string;
  name: string;
  price: number;
  image_url: string;
  quantity: number;
}

export interface Review {
  id: string;
  rating: number;
  comment: string;
  user_name: string;
  created_at: string;
  verified_purchase: boolean;
} 