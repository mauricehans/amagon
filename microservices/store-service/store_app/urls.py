from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/stores/', views.store_list, name='store_list'),
    path('api/stores/<uuid:store_id>/', views.store_detail, name='store_detail'),
    path('api/stores/seller/<uuid:seller_id>/', views.seller_stores, name='seller_stores'),
    path('api/stores/<uuid:store_id>/categories/', views.store_categories, name='store_categories'),
]