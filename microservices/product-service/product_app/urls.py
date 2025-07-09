from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('api/products/category/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('api/categories/', views.category_list, name='category_list'),
    path('api/products/search/', views.search_products, name='search_products'),
]