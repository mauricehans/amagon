from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response # Response is not used, but api_view might expect it for DRF views. Kept for safety.

@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']) # Allow all common methods
def api_catch_all(request, path_info=None): # path_info will be captured by re_path if configured to do so
    """
    This view is a fallback for requests starting with /api/ that were not
    handled by the RoutingMiddleware. This typically means the service prefix
    in the URL (e.g., /api/unknown-service/) was not recognized.
    """
    # The RoutingMiddleware should have already handled valid API requests.
    # If a request reaches here, it means it's an API path not defined in SERVICE_MAP
    # or some other issue occurred before routing.
    return JsonResponse(
        {'error': 'API endpoint not found or not routable.',
         'path': request.path},
        status=404
    )