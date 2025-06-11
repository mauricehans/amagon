from rest_framework import serializers
from .models import Seller, SellerProduct, SellerOrder, SellerRating, SellerAnalytics

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'name', 'email', 'phone', 'company_name', 'business_type', 
                 'address', 'is_verified', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}

class SellerProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.name', read_only=True)
    
    class Meta:
        model = SellerProduct
        fields = ['id', 'seller', 'seller_name', 'name', 'description', 'category', 
                 'price', 'cost', 'sku', 'stock_quantity', 'images', 'specifications',
                 'is_active', 'created_at', 'updated_at']

class SellerOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    seller_name = serializers.CharField(source='seller.name', read_only=True)
    
    class Meta:
        model = SellerOrder
        fields = ['id', 'seller', 'seller_name', 'product', 'product_name', 
                 'customer_email', 'quantity', 'unit_price', 'total_amount', 
                 'status', 'shipping_address', 'tracking_number', 'notes',
                 'created_at', 'updated_at']

class SellerRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerRating
        fields = ['id', 'seller', 'customer_email', 'rating', 'comment', 
                 'order', 'created_at']

class SellerAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerAnalytics
        fields = ['id', 'seller', 'date', 'total_sales', 'total_orders', 
                 'total_products_sold', 'average_order_value', 'created_at']