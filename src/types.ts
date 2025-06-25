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