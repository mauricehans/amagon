from django.core.management.base import BaseCommand
from product_app.models import Category, Product, ProductImage

class Command(BaseCommand):
    help = 'Seed the database with sample products'

    def handle(self, *args, **kwargs):
        # Étape 1: S'assurer que la catégorie existe
        category, created = Category.objects.get_or_create(
            name="Electronics",
            defaults={'description': "Electronic devices and accessories"}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created category "Electronics"'))

        # Étape 2: Récupérer la catégorie fraîchement depuis la BDD pour être sûr
        try:
            category = Category.objects.get(name="Electronics")
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR('FATAL: Could not retrieve category after ensuring its existence.'))
            return

        # Créer quelques produits
        products_data = [
            {
                "name": "Smartphone Pro Max",
                "description": "Latest smartphone with advanced features",
                "sku": "SP001",
                "price": "999.99",
                "cost": "600.00",
                "unit": "piece",
                "barcode": "123456789",
                "weight": "0.2",
                "dimensions": {"length": 15, "width": 7, "height": 0.8}
            },
            {
                "name": "Wireless Earbuds",
                "description": "High-quality wireless earbuds with noise cancellation",
                "sku": "WE001",
                "price": "199.99",
                "cost": "80.00",
                "unit": "piece",
                "barcode": "987654321",
                "weight": "0.05",
                "dimensions": {"length": 5, "width": 5, "height": 2}
            },
            {
                "name": "4K Smart TV",
                "description": "55-inch 4K Smart TV with HDR",
                "sku": "TV001",
                "price": "699.99",
                "cost": "400.00",
                "unit": "piece",
                "barcode": "456789123",
                "weight": "20.0",
                "dimensions": {"length": 123, "width": 71, "height": 8}
            }
        ]

        for data in products_data:
            # Plan Z: J'utilise category_id=1 directement au lieu d'un objet
            product = Product.objects.create(
                category_id=1, 
                **data
            )
            
            ProductImage.objects.create(
                product=product,
                url=f"https://picsum.photos/seed/{product.id}/400/400",
                is_primary=True
            )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created product: {product.name} (ID: {product.id})')
            ) 