from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Store, StoreCategory
import json

@api_view(['GET', 'POST'])
def store_list(request):
    """Liste des boutiques ou création d'une nouvelle boutique"""
    if request.method == 'GET':
        stores = Store.objects.all()
        store_data = []
        
        for store in stores:
            categories = StoreCategory.objects.filter(store=store)
            store_data.append({
                'id': str(store.id),
                'seller_id': str(store.seller_id),
                'name': store.name,
                'description': store.description,
                'logo': store.logo,
                'banner': store.banner,
                'categories': [cat.name for cat in categories],
                'created_at': store.created_at.isoformat()
            })
        
        return Response(store_data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            store = Store.objects.create(
                seller_id=data['seller_id'],
                name=data['name'],
                description=data.get('description', ''),
                logo=data.get('logo'),
                banner=data.get('banner')
            )
            
            # Ajouter les catégories si fournies
            if 'categories' in data:
                for category_name in data['categories']:
                    StoreCategory.objects.create(
                        store=store,
                        name=category_name
                    )
            
            return Response({
                'id': str(store.id),
                'message': 'Store created successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def store_detail(request, store_id):
    """Détails, modification ou suppression d'une boutique"""
    store = get_object_or_404(Store, id=store_id)
    
    if request.method == 'GET':
        categories = StoreCategory.objects.filter(store=store)
        return Response({
            'id': str(store.id),
            'seller_id': str(store.seller_id),
            'name': store.name,
            'description': store.description,
            'logo': store.logo,
            'banner': store.banner,
            'categories': [{'id': cat.id, 'name': cat.name} for cat in categories],
            'created_at': store.created_at.isoformat(),
            'updated_at': store.updated_at.isoformat()
        })
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            
            for key, value in data.items():
                if hasattr(store, key) and key not in ['id', 'seller_id']:
                    setattr(store, key, value)
            
            store.save()
            return Response({'message': 'Store updated successfully'})
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        store.delete()
        return Response({'message': 'Store deleted successfully'})

@api_view(['GET'])
def seller_stores(request, seller_id):
    """Boutiques d'un vendeur spécifique"""
    stores = Store.objects.filter(seller_id=seller_id)
    store_data = []
    
    for store in stores:
        categories = StoreCategory.objects.filter(store=store)
        store_data.append({
            'id': str(store.id),
            'name': store.name,
            'description': store.description,
            'logo': store.logo,
            'banner': store.banner,
            'categories': [cat.name for cat in categories],
            'created_at': store.created_at.isoformat()
        })
    
    return Response(store_data)

@api_view(['GET', 'POST'])
def store_categories(request, store_id):
    """Catégories d'une boutique"""
    store = get_object_or_404(Store, id=store_id)
    
    if request.method == 'GET':
        categories = StoreCategory.objects.filter(store=store)
        return Response([{
            'id': cat.id,
            'name': cat.name,
            'created_at': cat.created_at.isoformat()
        } for cat in categories])
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            category = StoreCategory.objects.create(
                store=store,
                name=data['name']
            )
            
            return Response({
                'id': category.id,
                'message': 'Category created successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)