"""
Management command to test cart merge flow.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cart.models import Cart, CartItem
from products.models import Product


class Command(BaseCommand):
    help = 'Test cart merge from anonymous to authenticated user'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== CART MERGE TEST ===\n'))

        # 1. Create or get a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f'Created user: {user.username}')
        else:
            self.stdout.write(f'Using existing user: {user.username}')

        # 2. Clean up any existing carts for this user
        Cart.objects.filter(user=user).delete()
        self.stdout.write(f'Cleaned up old user carts')

        # 3. Create anonymous cart with items
        session_id = 'test_session_123'
        anon_cart, _ = Cart.objects.get_or_create(
            session_id=session_id,
            user__isnull=True
        )
        self.stdout.write(f'\nCreated anonymous cart: {anon_cart.id} (session_id={session_id})')

        # Add some products to anonymous cart
        products = Product.objects.all()[:2]
        if not products:
            self.stdout.write(self.style.ERROR('No products found! Run load_mock_data first.'))
            return

        for i, product in enumerate(products, 1):
            CartItem.objects.create(
                cart=anon_cart,
                product_id=product.id,
                quantity=i
            )
            self.stdout.write(f'  Added product {product.id} (qty={i})')

        anon_item_count = anon_cart.items.count()
        self.stdout.write(f'Anonymous cart items: {anon_item_count}\n')

        # 4. Simulate login signal
        self.stdout.write('Simulating login signal...')
        from django.contrib.auth.signals import user_logged_in
        from unittest.mock import Mock
        
        request = Mock()
        request.session = {'session_key': session_id}
        request.session.session_key = session_id
        
        # Fire the signal manually
        user_logged_in.send(sender=User, request=request, user=user)
        
        # 5. Check results
        self.stdout.write(self.style.SUCCESS('\n=== RESULTS ==='))
        
        # Check if anonymous cart still exists
        anon_cart_count = Cart.objects.filter(session_id=session_id, user__isnull=True).count()
        self.stdout.write(f'Anonymous carts after merge: {anon_cart_count}')
        
        # Check user's cart
        user_carts = Cart.objects.filter(user=user)
        self.stdout.write(f'User carts: {user_carts.count()}')
        
        for user_cart in user_carts:
            item_count = user_cart.items.count()
            self.stdout.write(f'  Cart {user_cart.id}: {item_count} items')
            for item in user_cart.items.all():
                self.stdout.write(f'    - Product {item.product_id}: qty={item.quantity}')
        
        if anon_item_count > 0 and user_carts.count() > 0:
            total_items = sum(c.items.count() for c in user_carts)
            if total_items == anon_item_count:
                self.stdout.write(self.style.SUCCESS('\n✓ MERGE SUCCESSFUL!'))
            else:
                self.stdout.write(self.style.WARNING(f'\n✗ Item count mismatch: expected {anon_item_count}, got {total_items}'))
        else:
            self.stdout.write(self.style.ERROR('\n✗ MERGE FAILED!'))
