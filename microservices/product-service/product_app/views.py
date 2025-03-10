from django.http import JsonResponse
from .models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer

def product_list(request):
    """Renvoie la liste de tous les produits"""
    products = Product.objects.filter(is_active=True)
    data = [ProductSerializer.serialize(product) for product in products]
    return JsonResponse(data, safe=False)

def product_detail(request, product_id):
    """Renvoie les détails d'un produit spécifique"""
    try:
        product = Product.objects.get(id=product_id)
        data = ProductSerializer.serialize(product, include_reviews=True)
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Produit non trouvé"}, status=404)

def category_list(request):
    """Renvoie la liste de toutes les catégories"""
    categories = Category.objects.all()
    data = [CategorySerializer.serialize(category) for category in categories]
    return JsonResponse(data, safe=False)

def product_reviews(request, product_id):
    """Renvoie les avis pour un produit spécifique"""
    try:
        product = Product.objects.get(id=product_id)
        reviews = Review.objects.filter(product=product)
        data = [ReviewSerializer.serialize(review) for review in reviews]
        return JsonResponse(data, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Produit non trouvé"}, status=404)
