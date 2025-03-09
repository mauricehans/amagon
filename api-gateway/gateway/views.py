import requests
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import json

def proxy_view(request, path, service):
    """
    Proxy view for forwarding requests to microservices
    """
    service_url = settings.MICROSERVICE_URLS.get(service)
    if not service_url:
        return JsonResponse({'error': 'Service not found'}, status=404)
    
    url = f"{service_url}/{path}"
    method = request.method.lower()
    
    # Get the request body if it exists
    request_data = None
    if method in ['post', 'put', 'patch']:
        try:
            request_data = json.loads(request.body)
        except json.JSONDecodeError:
            request_data = request.POST
    
    # Forward the request to the microservice
    headers = {key: value for key, value in request.headers.items()
               if key.lower() not in ['host', 'content-length']}
    
    # Add the Authorization header if it exists
    if 'HTTP_AUTHORIZATION' in request.META:
        headers['Authorization'] = request.META['HTTP_AUTHORIZATION']
    
    # Make the request to the microservice
    response = getattr(requests, method)(
        url,
        headers=headers,
        json=request_data if method in ['post', 'put', 'patch'] else None,
        params=request.GET if method == 'get' else None,
        files=request.FILES if method == 'post' and request.FILES else None,
    )
    
    # Return the response from the microservice
    django_response = HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers.get('Content-Type', 'application/json')
    )
    
    # Add headers from the microservice response
    for key, value in response.headers.items():
        if key.lower() not in ['content-length', 'content-encoding', 'transfer-encoding']:
            django_response[key] = value
    
    return django_response
