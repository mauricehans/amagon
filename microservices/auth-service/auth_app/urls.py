from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', views.login_user, name='login'),
    path('api/auth/register/', views.register_user, name='register'),
    path('api/auth/logout/', views.logout_user, name='logout'),
    path('api/auth/profile/', views.user_profile, name='profile'),
    path('api/auth/verify-token/', views.verify_token, name='verify_token'),
]