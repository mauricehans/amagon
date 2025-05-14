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