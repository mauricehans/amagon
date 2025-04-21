from django.http import JsonResponse
from django.contrib.auth import authenticate

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip authentication for login and register endpoints
        if '/api/auth/login' in request.path or '/api/auth/register' in request.path:
            return self.get_response(request)

        # Check for JWT token in headers
if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        return self.get_response(request)
