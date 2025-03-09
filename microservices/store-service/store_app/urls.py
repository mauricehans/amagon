from django.urls import path
from store_app import views

urlpatterns = [
    path('stores/', views.store_list, name='store_list'),
    path('stores/<uuid:store_id>/', views.store_detail, name='store_detail'),
    path('stores/<uuid:store_id>/reviews/', views.store_reviews, name='store_reviews'),
    path('stores/<uuid:store_id>/social-media/', views.store_social_media, name='store_social_media'),
]
