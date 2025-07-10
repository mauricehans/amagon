import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def auth_proxy(request):
    response = requests.request(
        method=request.method,
        url=f"{settings.MICROSERVICES['auth']}{request.path}",
        headers={key: value for key, value in request.headers.items()
                if key.lower() not in ['host']},
        data=request.body if request.body else None,
    )
    return JsonResponse(response.json(), status=response.status_code)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def product_proxy(request):
    response = requests.request(
        method=request.method,
        url=f"{settings.MICROSERVICES['product']}{request.path}",
        headers={key: value for key, value in request.headers.items()
                if key.lower() not in ['host']},
        data=request.body if request.body else None,
    )
    return JsonResponse(response.json(), status=response.status_code)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def order_proxy(request):
    response = requests.request(
        method=request.method,
        url=f"{settings.MICROSERVICES['order']}{request.path}",
        headers={key: value for key, value in request.headers.items()
                if key.lower() not in ['host']},
        data=request.body if request.body else None,
    )
    return JsonResponse(response.json(), status=response.status_code)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def inventory_proxy(request):
    response = requests.request(
        method=request.method,
        url=f"{settings.MICROSERVICES['inventory']}{request.path}",
        headers={key: value for key, value in request.headers.items()
                if key.lower() not in ['host']},
        data=request.body if request.body else None,
    )
    return JsonResponse(response.json(), status=response.status_code)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def seller_proxy(request):
    response = requests.request(
        method=request.method,
        url=f"{settings.MICROSERVICES['seller']}{request.path}",
        headers={key: value for key, value in request.headers.items()
                if key.lower() not in ['host']},
        data=request.body if request.body else None,
    )
    return JsonResponse(response.json(), status=response.status_code)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def store_proxy(request):
    response = requests.request(
        method=request.method,
        url=f"{settings.MICROSERVICES['store']}{request.path}",
        headers={key: value for key, value in request.headers.items()
                if key.lower() not in ['host']},
        data=request.body if request.body else None,
    )
    return JsonResponse(response.json(), status=response.status_code)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def admin_proxy(request):
    response = requests.request(
        method=request.method,
        url=f"{settings.MICROSERVICES['admin']}{request.path}",
        headers={key: value for key, value in request.headers.items()
                if key.lower() not in ['host']},
        data=request.body if request.body else None,
    )
    return JsonResponse(response.json(), status=response.status_code)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def search_proxy(request):
    try:
        target_url = f"{settings.MICROSERVICES['search']}{request.path}?{request.META['QUERY_STRING']}" if request.META['QUERY_STRING'] else f"{settings.MICROSERVICES['search']}{request.path}"
        print(f"Search proxy: Forwarding request to {target_url}")
        
        # Headers à transmettre
        headers = {key: value for key, value in request.headers.items() 
                  if key.lower() not in ['host', 'content-length']}
        
        # Ajouter des headers CORS si nécessaire
        headers['Content-Type'] = 'application/json'
        
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.body if request.body else None,
            timeout=15,  # Timeout plus court
            verify=False  # Ignorer les erreurs SSL en développement
        )
        
        print(f"Search proxy: Response status {response.status_code}")
        
        # Vérifier que la réponse est valide
        if response.status_code >= 400:
            print(f"Search proxy: Error response {response.status_code}: {response.text}")
            return JsonResponse(
                {'error': f'Search service error: {response.status_code}'}, 
                status=response.status_code
            )
        
        return JsonResponse(response.json(), status=response.status_code)
        
    except requests.exceptions.Timeout:
        print("Search proxy: Timeout error")
        return JsonResponse(
            {'error': 'Search service timeout'}, 
            status=504
        )
    except requests.exceptions.ConnectionError:
        print("Search proxy: Connection error")
        return JsonResponse(
            {'error': 'Search service unavailable'}, 
            status=503
        )
    except requests.exceptions.RequestException as e:
        print(f"Search proxy error: {e}")
        return JsonResponse(
            {'error': f'Search service error: {str(e)}'}, 
            status=503
        )
    except Exception as e:
        print(f"Search proxy unexpected error: {e}")
        return JsonResponse(
            {'error': 'Internal server error'}, 
            status=500
        )