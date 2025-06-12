from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
import json
from decimal import Decimal

@api_view(['GET', 'POST'])
def order_list(request):
    """Liste des commandes ou création d'une nouvelle commande"""
    if request.method == 'GET':
        orders = Order.objects.all().order_by('-created_at')
        order_data = []
        
        for order in orders:
            items = OrderItem.objects.filter(order=order)
            order_data.append({
                'id': str(order.id),
                'user_id': str(order.user_id),
                'total_amount': float(order.total_amount),
                'status': order.status,
                'shipping_address': order.shipping_address,
                'items': [{
                    'product_id': str(item.product_id),
                    'quantity': item.quantity,
                    'price': float(item.price)
                } for item in items],
                'created_at': order.created_at.isoformat()
            })
        
        return Response(order_data)
    
    elif request.method == 'POST':
        return create_order(request)

@api_view(['POST'])
def create_order(request):
    """Créer une nouvelle commande"""
    try:
        data = json.loads(request.body)
        
        # Créer la commande
        order = Order.objects.create(
            user_id=data['user_id'],
            total_amount=Decimal(str(data['total_amount'])),
            status=data.get('status', 'pending'),
            shipping_address=data['shipping_address']
        )
        
        # Créer les items de la commande
        for item_data in data['items']:
            OrderItem.objects.create(
                order=order,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                price=Decimal(str(item_data['price']))
            )
        
        return Response({
            'id': str(order.id),
            'message': 'Order created successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def order_detail(request, order_id):
    """Détails ou modification d'une commande"""
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'GET':
        items = OrderItem.objects.filter(order=order)
        return Response({
            'id': str(order.id),
            'user_id': str(order.user_id),
            'total_amount': float(order.total_amount),
            'status': order.status,
            'shipping_address': order.shipping_address,
            'items': [{
                'product_id': str(item.product_id),
                'quantity': item.quantity,
                'price': float(item.price)
            } for item in items],
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat()
        })
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            
            # Mettre à jour le statut de la commande
            if 'status' in data:
                order.status = data['status']
                order.save()
            
            return Response({'message': 'Order updated successfully'})
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_orders(request, user_id):
    """Commandes d'un utilisateur spécifique"""
    orders = Order.objects.filter(user_id=user_id).order_by('-created_at')
    order_data = []
    
    for order in orders:
        items = OrderItem.objects.filter(order=order)
        order_data.append({
            'id': str(order.id),
            'total_amount': float(order.total_amount),
            'status': order.status,
            'items_count': items.count(),
            'created_at': order.created_at.isoformat()
        })
    
    return Response(order_data)