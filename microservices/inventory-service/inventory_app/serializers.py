import json
from inventory_app.models import Inventory, InventoryMovement

class InventorySerializer:
    @staticmethod
    def serialize(inventory, include_movements=False):
        result = {
            'id': str(inventory.id),
            'product_id': str(inventory.product_id),
            'store_id': str(inventory.store_id),
            'quantity': inventory.quantity,
            'sku': inventory.sku,
            'low_stock_threshold': inventory.low_stock_threshold,
            'created_at': inventory.created_at.isoformat(),
            'updated_at': inventory.updated_at.isoformat(),
        }
        
        if include_movements:
            movements = InventoryMovement.objects.filter(inventory=inventory).order_by('-created_at')
            result['movements'] = [InventoryMovementSerializer.serialize(movement) for movement in movements]
            
        return result
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

class InventoryMovementSerializer:
    @staticmethod
    def serialize(movement):
        return {
            'id': str(movement.id),
            'inventory_id': str(movement.inventory.id),
            'movement_type': movement.movement_type,
            'quantity': movement.quantity,
            'reference': movement.reference,
            'notes': movement.notes,
            'performed_by': str(movement.performed_by),
            'created_at': movement.created_at.isoformat(),
        }
    
    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data
