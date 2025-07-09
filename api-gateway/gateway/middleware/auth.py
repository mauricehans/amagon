from django.http import JsonResponse
from rest_framework import status
import requests

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
            
            # Déterminer le service d'authentification en fonction du chemin
            auth_service_url = self._get_auth_service_url(request.path)
            if not auth_service_url:
                return JsonResponse(
                    {'error': 'Invalid authentication service for this path'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Valider le token auprès du service d'authentification
            response = requests.post(f"{auth_service_url}/verify_token/", json={'token': token})

            if response.status_code != 200:
                return JsonResponse(
                    {'error': 'Invalid or expired token'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Ajouter les informations utilisateur à la requête
            user_data = response.json().get('user')
            if user_data:
                request.user_id = user_data.get('id')

        except (requests.exceptions.RequestException, IndexError):
            return JsonResponse(
                {'error': 'Invalid token or authentication service unavailable'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return self.get_response(request)

    def _requires_auth(self, path):
        public_paths = [
            '/api/auth/login',
            '/api/auth/register',
            '/api/seller/login',
            '/api/seller/register',
            '/api/admin/login',
            '/api/products',
        ]
        return not any(path.startswith(public_path) for public_path in public_paths)

    def _get_auth_service_url(self, path):
        if path.startswith('/api/seller'):
            return 'http://localhost:8006/api/seller'
        elif path.startswith('/api/admin'):
            return 'http://localhost:8007/api/admin'
        else:
            return 'http://localhost:8002/api/auth'
