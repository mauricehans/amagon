from django.db import models

class Inventory(models.Model):
    product_id = models.UUIDField(unique=True)
    quantity = models.IntegerField(default=0)
    reserved = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory'

class InventoryLog(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_logs'