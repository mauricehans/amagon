from django.http import JsonResponse
from django.contrib.auth import authenticate

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Votre logique d'authentification ici
        
        # Cette ligne doit avoir la même indentation que les autres lignes dans cette méthode
        return self.get_response(request)