from django.urls import path
from order_app import views

urlpatterns = [
    path('carts/<uuid:user_id>/', views.cart_view, name='cart_view'),
    path('carts/<uuid:user_id>/items/<uuid:item_id>/', views.cart_item_view, name='cart_item_view'),
    path('orders/', views.order_list, name='all_orders'),
    path('orders/<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('users/<uuid:user_id>/orders/', views.order_list, name='user_orders'),
]
