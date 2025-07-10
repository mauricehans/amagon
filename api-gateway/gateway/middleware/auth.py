from django.http import JsonResponse
from rest_framework import status
import jwt
from django.conf import settings

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self._requires_auth(request.path):
            return self.get_response(request)

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse(
                {'error': 'No authorization token provided'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload.get('user_id')
        except jwt.ExpiredSignatureError:
            return JsonResponse(
                {'error': 'Token has expired'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        except (jwt.InvalidTokenError, IndexError):
            return JsonResponse(
                {'error': 'Invalid token'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        return self.get_response(request)

    def _requires_auth(self, path):
        public_paths = [
            '/api/auth/login',
            '/api/auth/register',
            '/api/products',
            '/api/search',
        ]
        return not any(path.startswith(public_path) for public_path in public_paths)