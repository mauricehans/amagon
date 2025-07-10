import axios from 'axios';
import { Product, SearchParams, SearchResult, SearchSuggestion } from '../types/product';

export class ProductSearchService {
  private productServiceUrl = 'http://localhost:8004/api/products/';

  async searchProducts(params: SearchParams): Promise<SearchResult> {
    try {
      // Appel à l'API Django pour récupérer tous les produits
      console.log('Fetching products from:', this.productServiceUrl);
      const response = await axios.get(this.productServiceUrl);
      console.log('Response from Django service:', response.data);
      
      // Gérer différents formats de réponse possibles
      let products: Product[] = [];
      if (response.data && Array.isArray(response.data)) {
        products = response.data;
      } else if (response.data && Array.isArray(response.data.results)) {
        products = response.data.results;
      } else if (response.data && response.data.products) {
        products = response.data.products;
      }
      
      // Transformer les données si nécessaire (adapter les noms de champs)
      products = products.map((product: any) => ({
        id: product.id.toString(),
        name: product.name,
        description: product.description,
        price: product.price,
        image_url: product.images?.[0]?.url || product.image_url || '',
        category_name: product.category?.name || product.category_name || '',
        stock_quantity: product.stock_quantity || 0,
        rating: product.rating || 0,
        review_count: product.review_count || 0
      }));
      
            console.log('Products found:', products.length);
      console.log('Sample product:', products[0]);
      
      // Filtrage par requête de recherche
      if (params.query) {
        const query = params.query.toLowerCase();
        console.log('Searching for query:', query);
        const beforeFilter = products.length;
        products = products.filter(product =>
          product.name.toLowerCase().includes(query) ||
          product.description.toLowerCase().includes(query) ||
          product.category_name.toLowerCase().includes(query)
        );
        console.log('Products after filter:', products.length, 'out of', beforeFilter);
      }

      // Filtrage par catégorie
      if (params.category) {
        products = products.filter(product =>
          product.category_name.toLowerCase() === params.category!.toLowerCase()
        );
      }

      // Filtrage par prix
      if (params.minPrice !== undefined) {
        products = products.filter(product => product.price >= params.minPrice!);
      }
      if (params.maxPrice !== undefined) {
        products = products.filter(product => product.price <= params.maxPrice!);
      }

      // Tri
      if (params.sortBy) {
        switch (params.sortBy) {
          case 'price_asc':
            products.sort((a, b) => a.price - b.price);
            break;
          case 'price_desc':
            products.sort((a, b) => b.price - a.price);
            break;
          case 'rating':
            products.sort((a, b) => b.rating - a.rating);
            break;
          case 'name':
            products.sort((a, b) => a.name.localeCompare(b.name));
            break;
        }
      }

      // Pagination
      const total = products.length;
      const startIndex = (params.page - 1) * params.limit;
      const endIndex = startIndex + params.limit;
      const paginatedProducts = products.slice(startIndex, endIndex);

      return {
        products: paginatedProducts,
        pagination: {
          page: params.page,
          limit: params.limit,
          total,
          totalPages: Math.ceil(total / params.limit)
        },
        total
      };
    } catch (error: any) {
      console.error('Error fetching products from Django service:', error);
      console.error('Error details:', {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      });
      
      // En cas d'erreur, retourner un résultat vide
      return {
        products: [],
        pagination: {
          page: params.page,
          limit: params.limit,
          total: 0,
          totalPages: 0
        },
        total: 0
      };
    }
  }

  async getSearchSuggestions(query: string): Promise<SearchSuggestion[]> {
    try {
      const response = await axios.get(this.productServiceUrl);
      const products: Product[] = response.data.results || response.data || [];
      const suggestions: SearchSuggestion[] = [];
      const queryLower = query.toLowerCase();

      // Suggestions basées sur les noms de produits
      const productSuggestions = products
        .filter(product => product.name.toLowerCase().includes(queryLower))
        .slice(0, 5)
        .map(product => ({
          type: 'product' as const,
          text: product.name,
          id: product.id
        }));

      // Suggestions basées sur les catégories
      const categories = [...new Set(products.map(p => p.category_name))];
      const categorySuggestions = categories
        .filter(category => category.toLowerCase().includes(queryLower))
        .slice(0, 3)
        .map(category => ({
          type: 'category' as const,
          text: category,
          id: category
        }));

      suggestions.push(...productSuggestions, ...categorySuggestions);
      return suggestions.slice(0, 8);
    } catch (error) {
      console.error('Error fetching suggestions from Django service:', error);
      return [];
    }
  }
} 