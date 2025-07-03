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
import jwt
from django.conf import settings
from .models import Seller, SellerProduct, SellerOrder, SellerAnalytics
from .serializers import SellerSerializer, SellerProductSerializer, SellerOrderSerializer

@csrf_exempt
@api_view(['POST'])
def seller_register(request):
    """Inscription d'un nouveau vendeur"""
    try:
        data = json.loads(request.body)
        
        # Vérifier si l'email existe déjà
        if Seller.objects.filter(email=data['email']).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Créer le vendeur
        seller = Seller.objects.create(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            company_name=data.get('company_name', ''),
            business_type=data.get('business_type', 'individual'),
            address=data.get('address', {}),
            password=data['password']  # En production, hasher le mot de passe
        )
        
        # Générer un token JWT
        token = jwt.encode({
            'seller_id': str(seller.id),
            'email': seller.email,
            'exp': timezone.now() + timedelta(days=7)
        }, settings.SECRET_KEY, algorithm='HS256')
        
        return Response({
            'message': 'Seller registered successfully',
            'token': token,
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
        
        # Vérifier les identifiants
        seller = Seller.objects.filter(email=email, password=password).first()
        if not seller:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Générer un token JWT
        token = jwt.encode({
            'seller_id': str(seller.id),
            'email': seller.email,
            'exp': timezone.now() + timedelta(days=7)
        }, settings.SECRET_KEY, algorithm='HS256')
        
        return Response({
            'message': 'Login successful',
            'token': token,
            'seller': SellerSerializer(seller).data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def seller_profile(request):
    """Profil du vendeur"""
    try:
        # Récupérer le vendeur depuis le token
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'No authorization token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        seller = get_object_or_404(Seller, id=payload['seller_id'])
        
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
        # Récupérer le vendeur
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        seller = get_object_or_404(Seller, id=payload['seller_id'])
        
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
        # Récupérer le vendeur
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        seller = get_object_or_404(Seller, id=payload['seller_id'])
        
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
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        seller = get_object_or_404(Seller, id=payload['seller_id'])
        
        product = get_object_or_404(SellerProduct, id=product_id, seller=seller)
        return Response(SellerProductSerializer(product).data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_product(request, product_id):
    """Mettre à jour un produit"""
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        seller = get_object_or_404(Seller, id=payload['seller_id'])
        
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
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        seller = get_object_or_404(Seller, id=payload['seller_id'])
        
        product = get_object_or_404(SellerProduct, id=product_id, seller=seller)
        product.delete()
        
        return Response({'message': 'Product deleted successfully'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def seller_orders(request):
    """Commandes du vendeur"""
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        seller = get_object_or_404(Seller, id=payload['seller_id'])
        
        orders = SellerOrder.objects.filter(seller=seller).order_by('-created_at')
        return Response(SellerOrderSerializer(orders, many=True).data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def seller_analytics(request):
    """Analyses et statistiques détaillées"""
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        seller = get_object_or_404(Seller, id=payload['seller_id'])
        
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