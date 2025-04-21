import json
import jwt
import bcrypt
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction
from django.conf import settings

from auth_app.models import User, Role, Permission, RolePermission
from auth_app.serializers import UserSerializer, RoleSerializer, PermissionSerializer

def parse_request_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return {}

@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    data = parse_request_body(request)
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    
    # Check if user already exists
    if User.objects.filter(username=data['username']).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)
    
    if User.objects.filter(email=data['email']).exists():
        return JsonResponse({'error': 'Email already exists'}, status=400)
    
    # Hash password
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        with transaction.atomic():
            # Create user
            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                password=hashed_password,
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', '')
            )
            
            # Assign default role if exists
            default_role = Role.objects.filter(name='user').first()
            if default_role:
                user.roles.add(default_role)
            
            return JsonResponse({
                'message': 'User registered successfully',
                'user': UserSerializer.serialize(user)
            }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    data = parse_request_body(request)
    if 'username' not in data or 'password' not in data:
        return JsonResponse({'error': 'Missing username or password'}, status=400)
    
    try:
        # Find user by username
        user = User.objects.get(username=data['username'])
        
        # Check password
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        # Update last login
        user.last_login = timezone.now()
        user.save()
        
        # Generate JWT token
        payload = {
            'user_id': str(user.id),
            'username': user.username,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        
        return JsonResponse({'status': 'authenticated'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def verify_token(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    data = parse_request_body(request)
    if 'token' not in data:
        return JsonResponse({'error': 'Token is required'}, status=400)
    
    try:
        # Decode and verify token
        payload = jwt.decode(data['token'], settings.SECRET_KEY, algorithms=['HS256'])
        
        # Check if user exists
        user = User.objects.get(id=payload['user_id'])
        
        return JsonResponse({
            'user_id': str(user.id),
            'username': user.username,
            'email': user.email
        })
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token has expired'}, status=401)
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return JsonResponse({'error': 'Invalid token'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        if request.method == 'GET':
            return JsonResponse(UserSerializer.serialize(user))
        
        elif request.method == 'PUT':
            data = parse_request_body(request)
            
            # Update user fields
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            if 'password' in data:
                user.password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'is_active' in data:
                user.is_active = data['is_active']
                
            user.save()
            return JsonResponse(UserSerializer.serialize(user))
        
        elif request.method == 'DELETE':
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
