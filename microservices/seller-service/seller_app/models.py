from django.db import models
import uuid

class Seller(models.Model):
    SELLER_STATUS = (
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('inactive', 'Inactive'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(unique=True)  # Reference to Auth User
    company_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField()
    logo_url = models.URLField(blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    business_license = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=SELLER_STATUS, default='pending')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)  # Percentage
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class SellerAnalytics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_orders = models.IntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    products_sold = models.IntegerField(default=0)
    commission_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    views = models.IntegerField(default=0)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage
    
    class Meta:
        unique_together = ('seller', 'date')
    
    def __str__(self):
        return f"{self.seller.company_name} - {self.date}"
