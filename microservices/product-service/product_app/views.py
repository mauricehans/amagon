from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, ProductImage
import json

@api_view(['GET', 'POST'])
def product_list(request):
    """Liste des produits ou création d'un nouveau produit"""
    if request.method == 'GET':
        products = Product.objects.filter(is_active=True)
        print("DEBUG: Number of active products:", products.count())  # Debug log
        product_data = []
        
        for product in products:
            images = ProductImage.objects.filter(product=product)
            primary_image = images.filter(is_primary=True).first() or images.first()
            product_data.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': float(product.price),
                'category': {
                    'id': product.category.id,
                    'name': product.category.name
                },
                'images': [{'url': img.url, 'is_primary': img.is_primary} for img in images],
                'sku': product.sku,
                'weight': float(product.weight) if product.weight else None,
                'dimensions': product.dimensions,
                'created_at': product.created_at.isoformat(),
                # Added fields for frontend compatibility
                'image_url': primary_image.url if primary_image else None,
                'rating': 4.5,  # Mock value
                'review_count': 12,  # Mock value
                'category_name': product.category.name,
                'stock_quantity': 10,  # Mock value
            })
        
        return Response(product_data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = get_object_or_404(Category, id=data['category_id'])
            
            product = Product.objects.create(
                name=data['name'],
                description=data['description'],
                category=category,
                sku=data.get('sku', ''),
                price=data['price'],
                cost=data.get('cost', 0),
                unit=data.get('unit', 'pièce'),
                barcode=data.get('barcode'),
                weight=data.get('weight'),
                dimensions=data.get('dimensions'),
                is_active=data.get('is_active', True)
            )
            
            return Response({
                'id': product.id,
                'message': 'Product created successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, product_id):
    """Détails, modification ou suppression d'un produit"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'GET':
        images = ProductImage.objects.filter(product=product)
        primary_image = images.filter(is_primary=True).first() or images.first()
        return Response({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'category': {
                'id': product.category.id,
                'name': product.category.name
            },
            'images': [{'url': img.url, 'is_primary': img.is_primary} for img in images],
            'sku': product.sku,
            'weight': float(product.weight) if product.weight else None,
            'dimensions': product.dimensions,
            'is_active': product.is_active,
            'created_at': product.created_at.isoformat(),
            # Added fields for frontend compatibility
            'image_url': primary_image.url if primary_image else None,
            'rating': 4.5,  # Mock value
            'review_count': 12,  # Mock value
            'category_name': product.category.name,
            'stock_quantity': 10,  # Mock value
        })
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            
            for key, value in data.items():
                if hasattr(product, key) and key != 'id':
                    setattr(product, key, value)
            
            product.save()
            return Response({'message': 'Product updated successfully'})
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        product.is_active = False
        product.save()
        return Response({'message': 'Product deleted successfully'})

@api_view(['GET'])
def products_by_category(request, category_id):
    """Produits par catégorie"""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_active=True)
    
    product_data = []
    for product in products:
        images = ProductImage.objects.filter(product=product)
        product_data.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'images': [{'url': img.url, 'is_primary': img.is_primary} for img in images]
        })
    
    return Response(product_data)

@api_view(['GET'])
def category_list(request):
    """Liste des catégories"""
    categories = Category.objects.all()
    category_data = []
    
    for category in categories:
        category_data.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'parent_id': category.parent.id if category.parent else None
        })
    
    return Response(category_data)

@api_view(['GET'])
def search_products(request):
    """Recherche de produits"""
    query = request.GET.get('q', '')
    if not query:
        return Response([])
    
    products = Product.objects.filter(
        name__icontains=query,
        is_active=True
    )[:20]  # Limiter à 20 résultats
    
    product_data = []
    for product in products:
        images = ProductImage.objects.filter(product=product)
        product_data.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'images': [{'url': img.url, 'is_primary': img.is_primary} for img in images]
        })
    
    return Response(product_data)