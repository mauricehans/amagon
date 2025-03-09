from django.urls import path
from inventory_app import views

urlpatterns = [
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/<uuid:inventory_id>/', views.inventory_detail, name='inventory_detail'),
    path('inventory/<uuid:inventory_id>/movements/', views.inventory_movement, name='inventory_movement'),
]
