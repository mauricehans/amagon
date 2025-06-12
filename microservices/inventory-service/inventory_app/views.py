from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Store, Inventory, InventoryLog, TransferRequest
import json

@api_view(['GET'])
def inventory_list(request):
    """Liste de l'inventaire"""
    inventories = Inventory.objects.all()
    inventory_data = []
    
    for inventory in inventories:
        inventory_data.append({
            'store_id': str(inventory.store.id),
            'store_name': inventory.store.name,
            'product_id': str(inventory.product_id),
            'quantity': inventory.quantity,
            'min_quantity': inventory.min_quantity,
            'reserved': inventory.reserved,
            'available': inventory.quantity - inventory.reserved,
            'updated_at': inventory.updated_at.isoformat()
        })
    
    return Response(inventory_data)

@api_view(['GET', 'PUT'])
def inventory_detail(request, store_id, product_id):
    """Détails ou modification de l'inventaire pour un produit dans un magasin"""
    store = get_object_or_404(Store, id=store_id)
    
    try:
        inventory = Inventory.objects.get(store=store, product_id=product_id)
    except Inventory.DoesNotExist:
        if request.method == 'GET':
            return Response({'error': 'Inventory not found'}, status=status.HTTP_404_NOT_FOUND)
        # Créer un nouvel inventaire si PUT
        inventory = Inventory.objects.create(
            store=store,
            product_id=product_id,
            quantity=0,
            min_quantity=10
        )
    
    if request.method == 'GET':
        return Response({
            'store_id': str(inventory.store.id),
            'store_name': inventory.store.name,
            'product_id': str(inventory.product_id),
            'quantity': inventory.quantity,
            'min_quantity': inventory.min_quantity,
            'reserved': inventory.reserved,
            'available': inventory.quantity - inventory.reserved,
            'updated_at': inventory.updated_at.isoformat()
        })
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            
            old_quantity = inventory.quantity
            
            if 'quantity' in data:
                inventory.quantity = data['quantity']
            if 'min_quantity' in data:
                inventory.min_quantity = data['min_quantity']
            
            inventory.save()
            
            # Enregistrer le log
            if 'quantity' in data:
                InventoryLog.objects.create(
                    inventory=inventory,
                    action='adjust',
                    quantity=data['quantity'] - old_quantity
                )
            
            return Response({'message': 'Inventory updated successfully'})
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def store_list(request):
    """Liste des magasins ou création d'un nouveau magasin"""
    if request.method == 'GET':
        stores = Store.objects.all()
        store_data = []
        
        for store in stores:
            store_data.append({
                'id': str(store.id),
                'name': store.name,
                'location': store.location,
                'created_at': store.created_at.isoformat()
            })
        
        return Response(store_data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            store = Store.objects.create(
                name=data['name'],
                location=data['location']
            )
            
            return Response({
                'id': str(store.id),
                'message': 'Store created successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check_availability(request):
    """Vérifier la disponibilité d'un produit"""
    try:
        data = json.loads(request.body)
        product_id = data['product_id']
        quantity_needed = data['quantity']
        store_id = data.get('store_id')
        
        if store_id:
            # Vérifier dans un magasin spécifique
            try:
                inventory = Inventory.objects.get(store_id=store_id, product_id=product_id)
                available = inventory.quantity - inventory.reserved
                return Response({
                    'available': available >= quantity_needed,
                    'quantity_available': available,
                    'store_id': str(store_id)
                })
            except Inventory.DoesNotExist:
                return Response({
                    'available': False,
                    'quantity_available': 0,
                    'store_id': str(store_id)
                })
        else:
            # Vérifier dans tous les magasins
            inventories = Inventory.objects.filter(product_id=product_id)
            total_available = sum(inv.quantity - inv.reserved for inv in inventories)
            
            return Response({
                'available': total_available >= quantity_needed,
                'quantity_available': total_available,
                'stores': [{
                    'store_id': str(inv.store.id),
                    'store_name': inv.store.name,
                    'quantity_available': inv.quantity - inv.reserved
                } for inv in inventories if inv.quantity - inv.reserved > 0]
            })
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reserve_stock(request):
    """Réserver du stock pour une commande"""
    try:
        data = json.loads(request.body)
        product_id = data['product_id']
        quantity = data['quantity']
        store_id = data['store_id']
        
        inventory = get_object_or_404(Inventory, store_id=store_id, product_id=product_id)
        
        if inventory.quantity - inventory.reserved >= quantity:
            inventory.reserved += quantity
            inventory.save()
            
            # Enregistrer le log
            InventoryLog.objects.create(
                inventory=inventory,
                action='reserve',
                quantity=quantity
            )
            
            return Response({'message': 'Stock reserved successfully'})
        else:
            return Response({
                'error': 'Insufficient stock',
                'available': inventory.quantity - inventory.reserved
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)