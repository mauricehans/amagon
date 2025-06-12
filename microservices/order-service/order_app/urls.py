from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/orders/', views.order_list, name='order_list'),
    path('api/orders/<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('api/orders/create/', views.create_order, name='create_order'),
    path('api/orders/user/<int:user_id>/', views.user_orders, name='user_orders'),
]