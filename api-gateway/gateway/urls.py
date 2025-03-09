from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Route requests to services (example)
    path('auth/', include('auth_service.urls')),  # Proxy to auth-service
]
