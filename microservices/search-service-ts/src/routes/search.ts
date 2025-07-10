import { Router } from 'express';
import { searchProducts, getSearchSuggestions } from '../controllers/searchController';

const router = Router();

// Route pour rechercher des produits
router.get('/', searchProducts);

// Route pour obtenir des suggestions de recherche
router.get('/suggestions', getSearchSuggestions);

export default router; 