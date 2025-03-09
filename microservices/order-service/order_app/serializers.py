import json
from order_app.models import Cart, CartItem, Order, OrderItem

class CartItemSerializer:
    @staticmethod
    def serialize(cart_item):
        return {
            'id': str(cart_item.id),
            'cart_id': str(cart_item.cart.id),
            'product_id': str(cart_item.product_id),
            'quantity': cart_item.quantity,
            'price': float(cart_item.price),
            'subtotal': float(cart_item.price * cart_item.quantity),
            'created_at': cart_item.created_at.isoformat(),
            'updated_at': cart_item.updated_at.isoformat(),
        }
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

class CartSerializer:
    @staticmethod
    def serialize(cart, include_items=True):
        result = {
            'id': str(cart.id),
            'user_id': str(cart.user_id),
            'created_at': cart.created_at.isoformat(),
            'updated_at': cart.updated_at.isoformat(),
        }
        
        if include_items:
            items = CartItem.objects.filter(cart=cart)
            result['items'] = [CartItemSerializer.serialize(item) for item in items]
            result['total'] = sum(item.price * item.quantity for item in items)
        
        return result
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

class OrderItemSerializer:
    @staticmethod
    def serialize(order_item):
        return {
            'id': str(order_item.id),
            'order_id': str(order_item.order.id),
            'product_id': str(order_item.product_id),
            'product_name': order_item.product_name,
            'quantity': order_item.quantity,
            'price': float(order_item.price),
            'subtotal': float(order_item.price * order_item.quantity),
            'created_at': order_item.created_at.isoformat(),
        }
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

class OrderSerializer:
    @staticmethod
    def serialize(order, include_items=True):
        result = {
            'id': str(order.id),
            'user_id': str(order.user_id),
            'status': order.status,
            'total_amount': float(order.total_amount),
            'shipping_address': order.shipping_address,
            'billing_address': order.billing_address,
            'payment_method': order.payment_method,
            'payment_id': order.payment_id,
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat(),
        }
        
        if include_items:
            items = OrderItem.objects.filter(order=order)
            result['items'] = [OrderItemSerializer.serialize(item) for item in items]
        
        return result
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data
