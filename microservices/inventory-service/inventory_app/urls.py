from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/inventory/', views.inventory_list, name='inventory_list'),
    path('api/inventory/<uuid:store_id>/<uuid:product_id>/', views.inventory_detail, name='inventory_detail'),
    path('api/stores/', views.store_list, name='store_list'),
    path('api/inventory/check/', views.check_availability, name='check_availability'),
    path('api/inventory/reserve/', views.reserve_stock, name='reserve_stock'),
]