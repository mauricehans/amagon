from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentification admin
    path('api/admin/auth/login/', views.admin_login, name='admin_login'),
    path('api/admin/auth/logout/', views.admin_logout, name='admin_logout'),
    path('api/admin/auth/profile/', views.admin_profile, name='admin_profile'),
    
    # Dashboard
    path('api/admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('api/admin/stats/', views.dashboard_stats, name='dashboard_stats'),
    
    # Gestion des tickets de support
    path('api/admin/tickets/', views.ticket_list, name='ticket_list'),
    path('api/admin/tickets/<uuid:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('api/admin/tickets/<uuid:ticket_id>/assign/', views.assign_ticket, name='assign_ticket'),
    path('api/admin/tickets/<uuid:ticket_id>/status/', views.update_ticket_status, name='update_ticket_status'),
    path('api/admin/tickets/<uuid:ticket_id>/messages/', views.ticket_messages, name='ticket_messages'),
    path('api/admin/tickets/<uuid:ticket_id>/messages/add/', views.add_ticket_message, name='add_ticket_message'),
    
    # API publique pour créer des tickets
    path('api/support/tickets/create/', views.create_support_ticket, name='create_support_ticket'),
    path('api/support/tickets/user/<uuid:user_id>/', views.user_tickets, name='user_tickets'),
    
    # Gestion des utilisateurs et vendeurs
    path('api/admin/users/', views.user_management, name='user_management'),
    path('api/admin/sellers/', views.seller_management, name='seller_management'),
    path('api/admin/admins/', views.admin_management, name='admin_management'),
]