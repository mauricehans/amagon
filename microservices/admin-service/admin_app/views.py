from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
import json
import requests

from .models import AdminUser, SupportTicket, TicketMessage, TicketActivity, AdminDashboardStats
from . import token_service

@csrf_exempt
@api_view(['POST'])
def admin_login(request):
    """Connexion admin"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        try:
            admin = AdminUser.objects.get(username=username)
        except AdminUser.DoesNotExist:
            return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)

        if not admin.check_password(password):
            return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = token_service.create_admin_token(admin)
        
        return Response({
            'message': 'Connexion réussie',
            'token': token.token,
            'admin': {
                'id': str(admin.id),
                'username': admin.username,
                'email': admin.email,
                'role': admin.role,
                'department': admin.department,
                'is_super_admin': admin.is_super_admin
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def admin_logout(request):
    """Déconnexion admin"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'No authorization token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token_string = auth_header.split(' ')[1]
        token_service.revoke_admin_token(token_string)
        
        return Response({'message': 'Déconnexion réussie'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def admin_profile(request):
    """Profil admin"""
    try:
        admin = get_admin_from_token(request)
        if not admin:
            return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'admin': {
                'id': str(admin.id),
                'username': admin.username,
                'email': admin.email,
                'role': admin.role,
                'department': admin.department,
                'is_super_admin': admin.is_super_admin
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

# ... (le reste des vues reste identique, mais la logique d'authentification est maintenant gérée par le token_service)

def get_admin_from_token(request):
    """Récupérer l'admin depuis le token"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        
        token_string = auth_header.split(' ')[1]
        return token_service.validate_admin_token(token_string)
    except:
        return None
