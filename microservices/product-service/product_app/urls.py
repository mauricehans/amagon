from django.urls import path
from product_app import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<uuid:product_id>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('products/<uuid:product_id>/reviews/', views.product_reviews, name='product_reviews'),
]
