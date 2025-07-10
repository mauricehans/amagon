import { Request, Response } from 'express';
import { ProductSearchService } from '../services/productSearchService';

const searchService = new ProductSearchService();

export const searchProducts = async (req: Request, res: Response) => {
  try {
    const { q, category, minPrice, maxPrice, sortBy, page = 1, limit = 20 } = req.query;
    
    const searchParams = {
      query: q as string,
      category: category as string,
      minPrice: minPrice ? parseFloat(minPrice as string) : undefined,
      maxPrice: maxPrice ? parseFloat(maxPrice as string) : undefined,
      sortBy: sortBy as string,
      page: parseInt(page as string),
      limit: parseInt(limit as string)
    };

    const results = await searchService.searchProducts(searchParams);
    
    res.json({
      success: true,
      data: results.products,
      pagination: results.pagination,
      total: results.total
    });
  } catch (error) {
    console.error('Search error:', error);
    res.status(500).json({
      success: false,
      error: 'Erreur lors de la recherche'
    });
  }
};

export const getSearchSuggestions = async (req: Request, res: Response) => {
  try {
    const { q } = req.query;
    
    if (!q || typeof q !== 'string') {
      return res.status(400).json({
        success: false,
        error: 'Le paramètre de recherche est requis'
      });
    }

    const suggestions = await searchService.getSearchSuggestions(q);
    
    res.json({
      success: true,
      data: suggestions
    });
  } catch (error) {
    console.error('Suggestions error:', error);
    res.status(500).json({
      success: false,
      error: 'Erreur lors de la récupération des suggestions'
    });
  }
}; 