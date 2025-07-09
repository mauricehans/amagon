from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
import json

from .models import User
from . import token_service

User = get_user_model()

@csrf_exempt
@api_view(['POST'])
def register_user(request):
    """Inscription d'un nouvel utilisateur"""
    try:
        data = json.loads(request.body)
        
        if User.objects.filter(email=data['email']).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User(
            username=data['email'],
            email=data['email'],
            first_name=data.get('name', '').split(' ')[0] if data.get('name') else '',
            last_name=' '.join(data.get('name', '').split(' ')[1:]) if data.get('name') and len(data.get('name', '').split(' ')) > 1 else ''
        )
        user.set_password(data['password'])
        user.save()
        
        token = token_service.create_user_token(user)
        
        return Response({
            'message': 'User registered successfully',
            'token': token.token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}".strip()
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    """Connexion utilisateur"""
    try:
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = token_service.create_user_token(user)
        
        return Response({
            'message': 'Login successful',
            'token': token.token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}".strip()
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    """Déconnexion utilisateur"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'No authorization token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token_string = auth_header.split(' ')[1]
        token_service.revoke_user_token(token_string)
        
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_profile(request):
    """Profil utilisateur"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'No authorization token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token_string = auth_header.split(' ')[1]
        user = token_service.validate_user_token(token_string)
        
        if not user:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}".strip()
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def verify_token(request):
    """Vérification de token"""
    try:
        data = json.loads(request.body)
        token_string = data['token']
        
        user = token_service.validate_user_token(token_string)
        
        if not user:
            return Response({'valid': False, 'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'valid': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}".strip()
            }
        })
        
    except Exception as e:
        return Response({'valid': False, 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)