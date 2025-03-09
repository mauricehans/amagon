import json
from seller_app.models import Seller, SellerAnalytics

class SellerSerializer:
    @staticmethod
    def serialize(seller):
        return {
            'id': str(seller.id),
            'user_id': str(seller.user_id),
            'company_name': seller.company_name,
            'description': seller.description,
            'contact_email': seller.contact_email,
            'contact_phone': seller.contact_phone,
            'address': seller.address,
            'logo_url': seller.logo_url,
            'tax_id': seller.tax_id,
            'business_license': seller.business_license,
            'status': seller.status,
            'commission_rate': float(seller.commission_rate),
            'created_at': seller.created_at.isoformat(),
            'updated_at': seller.updated_at.isoformat(),
        }
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

class SellerAnalyticsSerializer:
    @staticmethod
    def serialize(analytics):
        return {
            'id': str(analytics.id),
            'seller_id': str(analytics.seller.id),
            'date': analytics.date.isoformat(),
            'total_sales': float(analytics.total_sales),
            'total_orders': analytics.total_orders,
            'average_order_value': float(analytics.average_order_value),
            'products_sold': analytics.products_sold,
            'commission_paid': float(analytics.commission_paid),
            'views': analytics.views,
            'conversion_rate': float(analytics.conversion_rate),
        }
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data
