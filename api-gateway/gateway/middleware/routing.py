import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponse

class RoutingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Format: {'service_prefix': 'microservice_key_in_settings', ...}
        # Example: {'products': 'product', 'orders': 'order'}
        self.SERVICE_MAP = {
            'auth': 'auth',
            'products': 'product',
            'orders': 'order',
            'inventory': 'inventory',
            'sellers': 'seller',
            'stores': 'store',
            'admin': 'admin', # For /api/admin/...
            'support': 'admin', # For /api/support/... routed to admin service
        }

    def __call__(self, request):
        path_parts = request.path.strip('/').split('/')

        # We are interested in paths like /api/service_prefix/...
        if path_parts and path_parts[0] == 'api' and len(path_parts) > 1:
            service_prefix = path_parts[1]

            if service_prefix in self.SERVICE_MAP:
                microservice_key = self.SERVICE_MAP[service_prefix]
                microservice_base_url = settings.MICROSERVICES.get(microservice_key)

                if microservice_base_url:
                    # Construct the target URL for the microservice
                    # Original path: /api/products/some/endpoint
                    # We need to pass /some/endpoint to the microservice
                    # So, the microservice_path will be path_parts[2:]
                    microservice_path_segments = path_parts[2:]
                    microservice_path = '/'.join(microservice_path_segments)

                    # Preserve query parameters
                    query_params = request.GET.urlencode()
                    target_url = f"{microservice_base_url}/{microservice_path}"
                    if query_params:
                        target_url += f"?{query_params}"

                    try:
                        # Forward the request
                        response = requests.request(
                            method=request.method,
                            url=target_url,
                            headers={key: value for key, value in request.headers.items()
                                     if key.lower() not in ['host', 'content-length']}, # Content-Length will be recalculated by requests
                            data=request.body if request.body else None,
                            allow_redirects=False # Usually, API gateways don't follow redirects themselves
                        )

                        # Return the response from the microservice
                        # Ensure content is bytes for HttpResponse
                        content_type = response.headers.get('Content-Type', 'application/json')

                        # If the microservice returns JSON and it's not already parsed by `response.json()`
                        # we can try to parse it for JsonResponse, otherwise, pass raw content.
                        # However, simply passing raw content is safer and more generic.
                        return HttpResponse(
                            response.content,
                            status=response.status_code,
                            content_type=content_type
                        )
                    except requests.exceptions.RequestException as e:
                        return JsonResponse({'error': f'Microservice communication error: {str(e)}'}, status=502) # Bad Gateway
                else:
                    # This case should ideally not happen if SERVICE_MAP and settings.MICROSERVICES are consistent
                    return JsonResponse({'error': f'Microservice URL for {service_prefix} not configured'}, status=500)
            else:
                # If the prefix is not in our map, but starts with /api/, let it fall through
                # or return a specific "service not found" error.
                # For now, let it fall through to be handled by Django's URL routing (e.g., 404).
                pass # Will eventually call self.get_response(request)

        # If the path is not /api/... or not handled above, proceed to the next middleware or view
        return self.get_response(request)