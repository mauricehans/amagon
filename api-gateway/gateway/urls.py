from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', views.auth_proxy),
    path('api/products/', views.product_proxy),
    path('api/orders/', views.order_proxy),
    path('api/inventory/', views.inventory_proxy),
    path('api/sellers/', views.seller_proxy),
    path('api/stores/', views.store_proxy),
    path('api/admin/', views.admin_proxy),
    path('api/support/', views.admin_proxy),  # Support tickets via admin service
    path('api/search/', views.search_proxy),
]