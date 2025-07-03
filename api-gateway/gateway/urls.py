from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls), # Django admin interface
    # All /api/... requests will be primarily handled by the RoutingMiddleware.
    # If the middleware doesn't handle it (e.g., path not in SERVICE_MAP but starts with /api/),
    # it will fall through. This catch-all can then return a 404.
    re_path(r'^api/', views.api_catch_all),
]