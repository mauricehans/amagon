import jwt
import requests
from django.conf import settings
from django.http import JsonResponse

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip authentication for login and register endpoints
        if '/api/auth/login' in request.path or '/api/auth/register' in request.path:
            return self.get_response(request)

        # Check for JWT token in headers
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authorization required'}, status=401)

        token = auth_header.split(" ")[1]
        try:
            # Verify the token with auth microservice
            response = requests.post(
                f"{settings.MICROSERVICE_URLS['auth']}/verify-token/",
                json={'token': token}
            )
            
            if response.status_code != 200:
                return JsonResponse({'error': 'Invalid or expired token'}, status=401)
            
            # Add user info to request
            request.user_info = response.json()
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return self.get_response(request)
