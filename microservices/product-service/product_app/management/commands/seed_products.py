from django.core.management.base import BaseCommand
from product_app.populate_products import run

class Command(BaseCommand):
    help = 'Seeds the database with initial product data.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        run()
        self.stdout.write(self.style.SUCCESS('Successfully seeded database.'))