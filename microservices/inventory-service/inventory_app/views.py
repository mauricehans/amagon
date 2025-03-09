import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import F

from inventory_app.models import Inventory, InventoryMovement
from inventory_app.serializers import InventorySerializer, InventoryMovementSerializer

def parse_request_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return {}

@csrf_exempt
def inventory_list(request):
    if request.method == 'GET':
        # Filter parameters
        product_id = request.GET.get('product')
        store_id = request.GET.get('store')
        low_stock = request.GET.get('low_stock')
        
        inventories = Inventory.objects.all()
        
        if product_id:
            inventories = inventories.filter(product_id=product_id)
        
        if store_id:
            inventories = inventories.filter(store_id=store_id)
        
        if low_stock and low_stock.lower() == 'true':
            inventories = inventories.filter(quantity__lte=F('low_stock_threshold'))
        
        result = [InventorySerializer.serialize(inventory) for inventory in inventories]
        return JsonResponse(result, safe=False)
    
    elif request.method == 'POST':
        data = parse_request_body(request)
        required_fields = ['product_id', 'store_id', 'quantity']
        
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        try:
            # Check if inventory already exists for this product and store
            inventory = Inventory.objects.filter(
                product_id=data['product_id'],
                store_id=data['store_id']
            ).first()
            
            if inventory:
                return JsonResponse({'error': 'Inventory for this product and store already exists'}, status=400)
            
            # Create new inventory
            inventory = Inventory.objects.create(
                product_id=data['product_id'],
                store_id=data['store_id'],
                quantity=data['quantity'],
                sku=data.get('sku'),
                low_stock_threshold=data.get('low_stock_threshold', 5)
            )
            
            # Create inventory movement for initial stock
            if data['quantity'] > 0:
                InventoryMovement.objects.create(
                    inventory=inventory,
                    movement_type='in',
                    quantity=data['quantity'],
                    notes='Initial stock',
                    performed_by=data.get('performed_by')
                )
            
            return JsonResponse(InventorySerializer.serialize(inventory), status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def inventory_detail(request, inventory_id):
    try:
        inventory = Inventory.objects.get(id=inventory_id)
        
        if request.method == 'GET':
            include_movements = request.GET.get('movements', 'false').lower() == 'true'
            return JsonResponse(InventorySerializer.serialize(inventory, include_movements))
        
        elif request.method == 'PUT':
            data = parse_request_body(request)
            
            # Can't directly update quantity, must use movements
            if 'sku' in data:
                inventory.sku = data['sku']
            if 'low_stock_threshold' in data:
                inventory.low_stock_threshold = data['low_stock_threshold']
                
            inventory.save()
            return JsonResponse(InventorySerializer.serialize(inventory))
        
        elif request.method == 'DELETE':
            # Check if there are any movements before deleting
            if InventoryMovement.objects.filter(inventory=inventory).exists():
                return JsonResponse({'error': 'Cannot delete inventory with movement history'}, status=400)
                
            inventory.delete()
            return JsonResponse({'message': 'Inventory deleted successfully'})
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except Inventory.DoesNotExist:
        return JsonResponse({'error': 'Inventory not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def inventory_movement(request, inventory_id):
    try:
        inventory = Inventory.objects.get(id=inventory_id)
        
        if request.method == 'GET':
            movements = InventoryMovement.objects.filter(inventory=inventory).order_by('-created_at')
            result = [InventoryMovementSerializer.serialize(movement) for movement in movements]
            return JsonResponse(result, safe=False)
        
        elif request.method == 'POST':
            data = parse_request_body(request)
            required_fields = ['movement_type', 'quantity', 'performed_by']
            
            if not all(field in data for field in required_fields):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            if data['movement_type'] not in dict(InventoryMovement.MOVEMENT_TYPES):
                return JsonResponse({'error': 'Invalid movement type'}, status=400)
            
            if data['quantity'] <= 0:
                return JsonResponse({'error': 'Quantity must be positive'}, status=400)
            
            try:
                with transaction.atomic():
                    # Update inventory quantity based on movement type
                    if data['movement_type'] in ['in', 'return']:
                        inventory.quantity += data['quantity']
                    elif data['movement_type'] == 'out':
                        if inventory.quantity < data['quantity']:
                            return JsonResponse({'error': 'Not enough stock available'}, status=400)
                        inventory.quantity -= data['quantity']
                    elif data['movement_type'] == 'adjustment':
                        # For adjustments, quantity can be positive or negative
                        inventory.quantity = max(0, inventory.quantity + data['quantity'])
                    
                    inventory.save()
                    
                    # Create movement record
                    movement = InventoryMovement.objects.create(
                        inventory=inventory,
                        movement_type=data['movement_type'],
                        quantity=data['quantity'],
                        reference=data.get('reference'),
                        notes=data.get('notes'),
                        performed_by=data['performed_by']
                    )
                    
                    return JsonResponse(InventoryMovementSerializer.serialize(movement), status=201)
            
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    except Inventory.DoesNotExist:
        return JsonResponse({'error': 'Inventory not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
