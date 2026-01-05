from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem

@receiver(user_logged_in)
def assign_session_cart_to_user(sender, request, user, **kwargs):
    user_cart, _ = Cart.objects.get_or_create(user=user)
    print(f"[SIGNAL] User cart: {user_cart.id} with {user_cart.items.count()} items")
    
    anon_carts = Cart.objects.filter(user__isnull=True)
    total_anon_items = sum(c.items.count() for c in anon_carts)
    
    if total_anon_items > 0:
        print(f"[SIGNAL] Found {anon_carts.count()} anonymous carts with {total_anon_items} total items")
        for anon_cart in anon_carts:
            item_count = anon_cart.items.count()
            if item_count > 0:
                CartItem.objects.filter(cart=anon_cart).update(cart=user_cart)
                print(f"[SIGNAL] Moved {item_count} items from cart {anon_cart.id} to user cart")

            anon_cart.delete()
        
        print(f"[SIGNAL] Merge complete! User cart now has {user_cart.items.count()} items")
    else:
        print(f"[SIGNAL] No anonymous carts to merge")