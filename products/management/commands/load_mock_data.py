from django.core.management.base import BaseCommand
from products.models import Category, Product
from fixtures.mock_data import MOCK_PRODUCTS, MOCK_CATEGORIES


class Command(BaseCommand):
    help = 'Load mock data into the database'

    def handle(self, *args, **options):
        self.stdout.write("Starting to load mock data...")
        
        # Clear existing data
        Category.objects.all().delete()
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✓ Cleared existing data"))
        
        # Load categories
        category_map = {}
        for cat_data in MOCK_CATEGORIES:
            category, created = Category.objects.get_or_create(
                id=cat_data['id'],
                defaults={'name': cat_data['name']}
            )
            category_map[cat_data['id']] = category
            status = "Created" if created else "Already exists"
            self.stdout.write(f"  {status}: Category '{category.name}'")
        
        self.stdout.write(self.style.SUCCESS(f"✓ Loaded {len(MOCK_CATEGORIES)} categories"))
        
        # Load products
        for product_data in MOCK_PRODUCTS:
            category = category_map.get(product_data['category_id'])
            product, created = Product.objects.get_or_create(
                id=product_data['id'],
                defaults={
                    'sku': product_data['sku'],
                    'title': product_data['title'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'image': product_data['image'],
                    'category': category
                }
            )
            status = "Created" if created else "Already exists"
            self.stdout.write(f"  {status}: Product '{product.title}' (${product.price})")
        
        self.stdout.write(self.style.SUCCESS(f"✓ Loaded {len(MOCK_PRODUCTS)} products"))
        self.stdout.write(self.style.SUCCESS("\n✓ Mock data loaded successfully!"))
