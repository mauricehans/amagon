from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sellers/', include([
        path('register/', views.seller_register, name='seller_register'),
        path('login/', views.seller_login, name='seller_login'),
        path('profile/', views.seller_profile, name='seller_profile'),
        path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
        path('products/', views.seller_products, name='seller_products'),
        path('products/create/', views.create_product, name='create_product'),
        path('products/<uuid:product_id>/', views.product_detail, name='product_detail'),
        path('products/<uuid:product_id>/update/', views.update_product, name='update_product'),
        path('products/<uuid:product_id>/delete/', views.delete_product, name='delete_product'),
        path('orders/', views.seller_orders, name='seller_orders'),
        path('analytics/', views.seller_analytics, name='seller_analytics'),
    ])),
]