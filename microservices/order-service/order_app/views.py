import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.conf import settings

from order_app.models import Cart, CartItem, Order, OrderItem
from order_app.serializers import CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer

def parse_request_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return {}

@csrf_exempt
def cart_view(request, user_id):
    try:
        # Get or create cart for user
        cart, created = Cart.objects.get_or_create(user_id=user_id)
        
        if request.method == 'GET':
            return JsonResponse(CartSerializer.serialize(cart))
        
        elif request.method == 'POST':
            data = parse_request_body(request)
            required_fields = ['product_id', 'quantity', 'price']
            
            if not all(field in data for field in required_fields):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Check if item already exists in cart
            cart_item = CartItem.objects.filter(cart=cart, product_id=data['product_id']).first()
            
            if cart_item:
                # Update quantity if item exists
                cart_item.quantity += data['quantity']
                cart_item.save()
            else:
                # Create new cart item
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product_id=data['product_id'],
                    quantity=data['quantity'],
                    price=data['price']
                )
            
            return JsonResponse(CartItemSerializer.serialize(cart_item), status=201)
        
        elif request.method == 'DELETE':
            # Clear cart
            CartItem.objects.filter(cart=cart).delete()
            return JsonResponse({'message': 'Cart cleared successfully'})
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def cart_item_view(request, user_id, item_id):
    try:
        cart = Cart.objects.get(user_id=user_id)
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        
        if request.method == 'PUT':
            data = parse_request_body(request)
            
            if 'quantity' in data:
                if data['quantity'] <= 0:
                    cart_item.delete()
                    return JsonResponse({'message': 'Item removed from cart'})
                else:
                    cart_item.quantity = data['quantity']
            
            if 'price' in data:
                cart_item.price = data['price']
            
            cart_item.save()
            return JsonResponse(CartItemSerializer.serialize(cart_item))
        
        elif request.method == 'DELETE':
            cart_item.delete()
            return JsonResponse({'message': 'Item removed from cart'})
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart not found'}, status=404)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def order_list(request, user_id=None):
    if request.method == 'GET':
        if user_id:
            orders = Order.objects.filter(user_id=user_id).order_by('-created_at')
        else:
            orders = Order.objects.all().order_by('-created_at')
        
        result = [OrderSerializer.serialize(order, include_items=False) for order in orders]
        return JsonResponse(result, safe=False)
    
    elif request.method == 'POST':
        data = parse_request_body(request)
        required_fields = ['user_id', 'shipping_address', 'billing_address', 'payment_method']
        
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        try:
            with transaction.atomic():
                # Get user's cart
                cart = Cart.objects.get(user_id=data['user_id'])
                cart_items = CartItem.objects.filter(cart=cart)
                
                if not cart_items:
                    return JsonResponse({'error': 'Cart is empty'}, status=400)
                
                # Calculate total amount
                total_amount = sum(item.price * item.quantity for item in cart_items)
                
                # Create order
                order = Order.objects.create(
                    user_id=data['user_id'],
                    total_amount=total_amount,
                    shipping_address=data['shipping_address'],
                    billing_address=data['billing_address'],
                    payment_method=data['payment_method'],
                    payment_id=data.get('payment_id'),
                    status='pending'
                )
                
                # Create order items
                for cart_item in cart_items:
                    # Get product name from product service
                    try:
                        product_response = requests.get(f"{settings.MICROSERVICE_URLS['product']}/products/{cart_item.product_id}/")
                        product_data = product_response.json()
                        product_name = product_data.get('name', 'Unknown Product')
                    except:
                        product_name = 'Unknown Product'
                    
                    OrderItem.objects.create(
                        order=order,
                        product_id=cart_item.product_id,
                        product_name=product_name,
                        quantity=cart_item.quantity,
                        price=cart_item.price
                    )
                
                # Clear cart after successful order
                cart_items.delete()
                
                return JsonResponse(OrderSerializer.serialize(order), status=201)
        
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        
        if request.method == 'GET':
            return JsonResponse(OrderSerializer.serialize(order))
        
        elif request.method == 'PUT':
            data = parse_request_body(request)
            
            if 'status' in data:
                order.status = data['status']
            
            order.save()
            return JsonResponse(OrderSerializer.serialize(order))
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
