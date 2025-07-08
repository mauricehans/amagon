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
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'No authorization token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token_string = auth_header.split(' ')[1]
        seller = token_service.validate_seller_token(token_string)
        
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

# ... (le reste des vues reste identique, mais la logique d'authentification est maintenant gérée par le token_service)
