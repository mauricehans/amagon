from django.urls import path
from admin_app import views

urlpatterns = [
    path('settings/', views.admin_settings_list, name='admin_settings_list'),
    path('settings/<uuid:setting_id>/', views.admin_settings_detail, name='admin_settings_detail'),
    path('settings/name/<str:setting_name>/', views.admin_settings_detail, name='admin_settings_by_name'),
    path('logs/', views.system_logs, name='system_logs'),
    path('logs/<uuid:log_id>/', views.system_log_detail, name='system_log_detail'),
]
