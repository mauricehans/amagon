from django.db import models
import uuid

class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stores'

class Inventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='inventories')
    product_id = models.UUIDField()
    quantity = models.IntegerField(default=0)
    min_quantity = models.IntegerField(default=10)  # Seuil d'alerte
    reserved = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory'
        unique_together = ('store', 'product_id')

class InventoryLog(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)  # 'add', 'remove', 'transfer', 'adjust'
    quantity = models.IntegerField()
    from_store = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL, related_name='outgoing_logs')
    to_store = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL, related_name='incoming_logs')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_logs'

class TransferRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.UUIDField()
    quantity = models.IntegerField()
    from_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='outgoing_transfers')
    to_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='incoming_transfers')
    status = models.CharField(max_length=20, default='pending')  # pending, approved, rejected, completed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transfer_requests'