from django.contrib import admin
from django.urls import path
from gateway.views import proxy_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirection vers les microservices
    path('auth/<path:path>', lambda request, path: proxy_view(request, path, 'auth')),
    path('product/<path:path>', lambda request, path: proxy_view(request, path, 'product')),
    path('order/<path:path>', lambda request, path: proxy_view(request, path, 'order')),
    path('store/<path:path>', lambda request, path: proxy_view(request, path, 'store')),
    path('inventory/<path:path>', lambda request, path: proxy_view(request, path, 'inventory')),
    path('seller/<path:path>', lambda request, path: proxy_view(request, path, 'seller')),
    path('admin-service/<path:path>', lambda request, path: proxy_view(request, path, 'admin')),
]
