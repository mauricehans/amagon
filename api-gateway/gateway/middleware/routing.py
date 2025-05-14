class RoutingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add service routing logic here if needed
        return self.get_response(request)