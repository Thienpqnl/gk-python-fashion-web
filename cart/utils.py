# cart/utils.py
from django.contrib.sessions.models import Session
from .models import Cart, CartItem
from products.models import Product

def merge_session_cart_into_user_cart(request, user):
    session_cart = request.session.get('cart', {})
    if not session_cart:
        return

    # Get or create user's Cart
    user_cart, _ = Cart.objects.get_or_create(user=user)

    # Merge each item
    for product_id_str, quantity in session_cart.items():
        try:
            product_id = int(product_id_str)
            # Optional: validate product exists
            Product.objects.get(id=product_id)

            # Get or update CartItem
            item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                product_id=product_id,
                defaults={'quantity': quantity}
            )
            if not created:
                # If already exists, sum quantities
                item.quantity += quantity
                item.save()

        except (ValueError, Product.DoesNotExist):
            # Skip invalid or deleted products
            continue

    # Xóa giỏ hàng trong session sau khi merge
    if 'cart' in request.session:
        del request.session['cart']
        # ensure session is saved after modifying
        request.session.modified = True