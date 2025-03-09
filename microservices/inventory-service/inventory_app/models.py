from django.db import models
import uuid

class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.UUIDField()
    store_id = models.UUIDField() 
    quantity = models.IntegerField(default=0)
    sku = models.CharField(max_length=100, blank=True, null=True)
    low_stock_threshold = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventory: Product {self.product_id} - {self.quantity} units"
    
    class Meta:
        unique_together = ('product_id', 'store_id')

class InventoryMovement(models.Model):
    MOVEMENT_TYPES = (
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
        ('return', 'Return'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reference = models.CharField(max_length=255, blank=True, null=True)  # Order ID, return ID, etc.
    notes = models.TextField(blank=True, null=True)
    performed_by = models.UUIDField()  # User ID who performed the movement
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type}: {self.quantity} units"
