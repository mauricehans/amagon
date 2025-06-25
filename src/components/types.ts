// Product interface
export interface Product {
    id: number;
    name: string;
    description: string;
    price: number;
    image_url: string;
    category_name: string;
    stock_quantity: number;
    rating: number;
    review_count: number;
}

// Cart item interface
export interface CartItem {
    id: number;
    name: string;
    price: number;
    image_url: string;
    quantity: number;
}

// Review interface
export interface Review {
    id: number;
    rating: number;
    comment: string;
    user_name: string;
    created_at: string;
    verified_purchase: boolean;
} 