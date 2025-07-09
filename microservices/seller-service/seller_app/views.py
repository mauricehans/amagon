from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import Seller, SellerProduct, SellerOrder, SellerAnalytics
from .serializers import SellerSerializer, SellerProductSerializer, SellerOrderSerializer
from . import token_service

@csrf_exempt
@api_view(['POST'])
def seller_register(request):
    """Inscription d'un nouveau vendeur"""
    try:
        data = json.loads(request.body)
        
        if Seller.objects.filter(email=data['email']).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        seller = Seller(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            company_name=data.get('company_name', ''),
            business_type=data.get('business_type', 'individual'),
            address=data.get('address', {})
        )
        seller.set_password(data['password'])
        seller.save()
        
        token = token_service.create_seller_token(seller)
        
        return Response({
            'message': 'Seller registered successfully',
            'token': token.token,
            'seller': SellerSerializer(seller).data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def seller_login(request):
    """Connexion vendeur"""
    try:
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        
        try:
            seller = Seller.objects.get(email=email)
        except Seller.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not seller.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = token_service.create_seller_token(seller)
        
        return Response({
            'message': 'Login successful',
            'token': token.token,
            'seller': SellerSerializer(seller).data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def seller_profile(request):
    """Profil du vendeur"""
    try:
        seller = get_seller_from_token(request)
        if not seller:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.method == 'GET':
            return Response(SellerSerializer(seller).data)
        
        elif request.method == 'PUT':
            data = json.loads(request.body)
            for key, value in data.items():
                if hasattr(seller, key):
                    setattr(seller, key, value)
            seller.save()
            return Response(SellerSerializer(seller).data)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def seller_dashboard(request):
    """Tableau de bord du vendeur"""
    try:
        seller = get_seller_from_token(request)
        if not seller:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Statistiques générales
        total_products = SellerProduct.objects.filter(seller=seller).count()
        active_products = SellerProduct.objects.filter(seller=seller, is_active=True).count()
        total_orders = SellerOrder.objects.filter(seller=seller).count()
        total_revenue = SellerOrder.objects.filter(seller=seller, status='completed').aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        # Commandes récentes
        recent_orders = SellerOrder.objects.filter(seller=seller).order_by('-created_at')[:5]
        
        # Produits les plus vendus
        top_products = SellerProduct.objects.filter(seller=seller).annotate(
            order_count=Count('sellerorder')
        ).order_by('-order_count')[:5]
        
        # Ventes par mois (6 derniers mois)
        six_months_ago = timezone.now() - timedelta(days=180)
        monthly_sales = []
        for i in range(6):
            month_start = six_months_ago + timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            sales = SellerOrder.objects.filter(
                seller=seller,
                created_at__gte=month_start,
                created_at__lt=month_end,
                status='completed'
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            monthly_sales.append({
                'month': month_start.strftime('%B'),
                'sales': float(sales)
            })
        
        return Response({
            'stats': {
                'total_products': total_products,
                'active_products': active_products,
                'total_orders': total_orders,
                'total_revenue': float(total_revenue),
            },
            'recent_orders': SellerOrderSerializer(recent_orders, many=True).data,
            'top_products': SellerProductSerializer(top_products, many=True).data,
            'monthly_sales': monthly_sales
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def seller_products(request):
    """Gestion des produits du vendeur"""
    try:
        seller = get_seller_from_token(request)
        if not seller:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.method == 'GET':
            products = SellerProduct.objects.filter(seller=seller)
            return Response(SellerProductSerializer(products, many=True).data)
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            product = SellerProduct.objects.create(
                seller=seller,
                name=data['name'],
                description=data['description'],
                category=data['category'],
                price=data['price'],
                cost=data.get('cost', 0),
                sku=data.get('sku', ''),
                stock_quantity=data.get('stock_quantity', 0),
                images=data.get('images', []),
                specifications=data.get('specifications', {}),
                is_active=data.get('is_active', True)
            )
            return Response(SellerProductSerializer(product).data, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_product(request):
    """Créer un nouveau produit"""
    return seller_products(request)

@api_view(['GET'])
def product_detail(request, product_id):
    """Détails d'un produit"""
    try:
        seller = get_seller_from_token(request)
        if not seller:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        product = get_object_or_404(SellerProduct, id=product_id, seller=seller)
        return Response(SellerProductSerializer(product).data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_product(request, product_id):
    """Mettre à jour un produit"""
    try:
        seller = get_seller_from_token(request)
        if not seller:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        product = get_object_or_404(SellerProduct, id=product_id, seller=seller)
        data = json.loads(request.body)
        
        for key, value in data.items():
            if hasattr(product, key):
                setattr(product, key, value)
        product.save()
        
        return Response(SellerProductSerializer(product).data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_product(request, product_id):
    """Supprimer un produit"""
    try:
        seller = get_seller_from_token(request)
        if not seller:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        product = get_object_or_404(SellerProduct, id=product_id, seller=seller)
        product.delete()
        
        return Response({'message': 'Product deleted successfully'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def seller_orders(request):
    """Commandes du vendeur"""
    try:
        seller = get_seller_from_token(request)
        if not seller:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        orders = SellerOrder.objects.filter(seller=seller).order_by('-created_at')
        return Response(SellerOrderSerializer(orders, many=True).data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def seller_analytics(request):
    """Analyses et statistiques détaillées"""
    try:
        seller = get_seller_from_token(request)
        if not seller:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Analyses par période
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Ventes par période
        today_sales = SellerOrder.objects.filter(
            seller=seller, created_at__date=today, status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        week_sales = SellerOrder.objects.filter(
            seller=seller, created_at__date__gte=week_ago, status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        month_sales = SellerOrder.objects.filter(
            seller=seller, created_at__date__gte=month_ago, status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Produits par catégorie
        category_stats = SellerProduct.objects.filter(seller=seller).values('category').annotate(
            count=Count('id'),
            total_sales=Sum('sellerorder__total_amount')
        )
        
        return Response({
            'sales_by_period': {
                'today': float(today_sales),
                'week': float(week_sales),
                'month': float(month_sales)
            },
            'category_stats': list(category_stats)
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def seller_password_reset(request):
    """Réinitialisation du mot de passe vendeur (simulation d'envoi d'email)"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        # Simule la présence de l'email (ne révèle pas si l'email existe)
        # Ici, vous pouvez envoyer un vrai email si besoin
        print(f"[INFO] Password reset requested for: {email}")
        return Response({'message': 'Si ce compte existe, un email de réinitialisation a été envoyé.'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def get_seller_from_token(request):
    """Récupérer le vendeur depuis le token"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        
        token_string = auth_header.split(' ')[1]
        return token_service.validate_seller_token(token_string)
    except:
        return None