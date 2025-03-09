from django.urls import path
from seller_app import views

urlpatterns = [
    path('sellers/', views.seller_list, name='seller_list'),
    path('sellers/<uuid:seller_id>/', views.seller_detail, name='seller_detail'),
    path('sellers/user/<uuid:user_id>/', views.seller_detail, name='seller_detail_by_user'),
    path('sellers/<uuid:seller_id>/analytics/', views.seller_analytics, name='seller_analytics'),
]
