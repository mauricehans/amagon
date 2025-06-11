from django.db import models
import uuid

class Seller(models.Model):
    BUSINESS_TYPES = [
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('partnership', 'Partnership'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # En production, utiliser un hash
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPES, default='individual')
    address = models.JSONField(default=dict)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sellers'

    def __str__(self):
        return f"{self.name} ({self.email})"

class SellerProduct(models.Model):
    CATEGORIES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('books', 'Books'),
        ('home', 'Home & Garden'),
        ('sports', 'Sports'),
        ('toys', 'Toys'),
        ('beauty', 'Beauty'),
        ('automotive', 'Automotive'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORIES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sku = models.CharField(max_length=100, blank=True)
    stock_quantity = models.IntegerField(default=0)
    images = models.JSONField(default=list)  # Liste d'URLs d'images
    specifications = models.JSONField(default=dict)  # Spécifications techniques
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'seller_products'
        unique_together = ('seller', 'sku')

    def __str__(self):
        return f"{self.name} - {self.seller.name}"

class SellerOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE)
    customer_email = models.EmailField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.JSONField()
    tracking_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'seller_orders'

    def __str__(self):
        return f"Order {self.id} - {self.seller.name}"

class SellerRating(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='ratings')
    customer_email = models.EmailField()
    rating = models.IntegerField()  # 1-5
    comment = models.TextField(blank=True)
    order = models.ForeignKey(SellerOrder, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'seller_ratings'
        unique_together = ('seller', 'customer_email', 'order')

class SellerAnalytics(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_orders = models.IntegerField(default=0)
    total_products_sold = models.IntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'seller_analytics'
        unique_together = ('seller', 'date')