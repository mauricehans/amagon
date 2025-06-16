from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdminUser, SupportTicket, TicketMessage, TicketActivity, AdminDashboardStats

@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'department', 'is_super_admin', 'is_active', 'created_at']
    list_filter = ['role', 'department', 'is_super_admin', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'role', 'department']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Admin', {
            'fields': ('role', 'department', 'phone', 'is_super_admin')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'subject', 'requester_name', 'requester_type', 'status', 'priority', 'assigned_to', 'created_at']
    list_filter = ['status', 'priority', 'category', 'requester_type', 'created_at']
    search_fields = ['ticket_number', 'subject', 'requester_name', 'requester_email']
    readonly_fields = ['id', 'ticket_number', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Informations du ticket', {
            'fields': ('ticket_number', 'subject', 'description', 'category', 'priority', 'status')
        }),
        ('Demandeur', {
            'fields': ('requester_type', 'requester_name', 'requester_email', 'requester_id')
        }),
        ('Assignation', {
            'fields': ('assigned_to',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at', 'resolved_at')
        }),
    ]

@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'author_name', 'message_type', 'is_internal', 'created_at']
    list_filter = ['message_type', 'is_internal', 'created_at']
    search_fields = ['ticket__ticket_number', 'author_name', 'content']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(TicketActivity)
class TicketActivityAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'activity_type', 'actor_name', 'actor_type', 'created_at']
    list_filter = ['activity_type', 'actor_type', 'created_at']
    search_fields = ['ticket__ticket_number', 'actor_name', 'description']
    readonly_fields = ['id', 'created_at']

@admin.register(AdminDashboardStats)
class AdminDashboardStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_tickets', 'open_tickets', 'resolved_tickets', 'new_users', 'new_sellers']
    list_filter = ['date']
    readonly_fields = ['created_at', 'updated_at']