from django.contrib import admin
from .models import Seller, SellerProduct, SellerOrder, SellerRating, SellerAnalytics

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company_name', 'business_type', 'is_verified', 'is_active', 'created_at']
    list_filter = ['business_type', 'is_verified', 'is_active', 'created_at']
    search_fields = ['name', 'email', 'company_name']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(SellerProduct)
class SellerProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'category', 'price', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'sku', 'seller__name']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(SellerOrder)
class SellerOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'product', 'customer_email', 'quantity', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_email', 'seller__name', 'product__name']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(SellerRating)
class SellerRatingAdmin(admin.ModelAdmin):
    list_display = ['seller', 'customer_email', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['seller__name', 'customer_email']

@admin.register(SellerAnalytics)
class SellerAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['seller', 'date', 'total_sales', 'total_orders', 'total_products_sold']
    list_filter = ['date']
    search_fields = ['seller__name']