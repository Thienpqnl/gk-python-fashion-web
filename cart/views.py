from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from products.models import Product


def _get_cart_from_session(request):
    """Get cart from session or create empty one."""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']


def _save_cart_to_session(request, cart):
    """Save cart to session."""
    request.session['cart'] = cart
    request.session.modified = True


def get_cart(request):
    """Get current user's cart with calculated totals."""
    cart = _get_cart_from_session(request)
    
    # Calculate cart details
    items = []
    total_price = 0
    total_quantity = 0
    
    for product_id_str, qty in cart.items():
        product_id = int(product_id_str)
        try:
            product = Product.objects.get(id=product_id)
            item_total = product.price * qty
            items.append({
                'product_id': product.id,
                'product_title': product.title,
                'product_price': product.price,
                'product_image': product.image,
                'quantity': qty,
                'item_total': item_total
            })
            total_price += item_total
            total_quantity += qty
        except Product.DoesNotExist:
            # Remove product if it doesn't exist
            del cart[product_id_str]
            _save_cart_to_session(request, cart)
    
    return JsonResponse({
        'status': 'success',
        'data': {
            'items': items,
            'total_price': total_price,
            'total_quantity': total_quantity,
            'item_count': len(items)
        }
    })


@require_http_methods(["POST"])
def add_to_cart(request):
    """Add product to cart."""
    try:
        data = json.loads(request.body)
        product_id = int(data.get('product_id'))
        qty = int(data.get('quantity', 1))
        
        # Validate product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Product not found'
            }, status=404)
        
        cart = _get_cart_from_session(request)
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            cart[product_id_str] += qty
        else:
            cart[product_id_str] = qty
        
        _save_cart_to_session(request, cart)
        
        return JsonResponse({
            'status': 'success',
            'message': f'Added {qty} {product.title} to cart'
        })
    
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Invalid request: {str(e)}'
        }, status=400)


@require_http_methods(["POST"])
def remove_from_cart(request):
    """Remove item from cart."""
    try:
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        
        cart = _get_cart_from_session(request)
        if product_id in cart:
            del cart[product_id]
            _save_cart_to_session(request, cart)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Item removed from cart'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Item not in cart'
            }, status=404)
    
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Invalid request: {str(e)}'
        }, status=400)


@require_http_methods(["POST"])
def update_cart_item(request):
    """Update quantity of item in cart."""
    try:
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        new_qty = int(data.get('quantity', 1))
        
        if new_qty < 0:
            return JsonResponse({
                'status': 'error',
                'message': 'Quantity must be positive'
            }, status=400)
        
        cart = _get_cart_from_session(request)
        
        if product_id not in cart:
            return JsonResponse({
                'status': 'error',
                'message': 'Item not in cart'
            }, status=404)
        
        if new_qty == 0:
            del cart[product_id]
        else:
            cart[product_id] = new_qty
        
        _save_cart_to_session(request, cart)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Cart updated'
        })
    
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Invalid request: {str(e)}'
        }, status=400)


@require_http_methods(["POST"])
def clear_cart(request):
    """Clear all items from cart."""
    request.session['cart'] = {}
    request.session.modified = True
    
    return JsonResponse({
        'status': 'success',
        'message': 'Cart cleared'
    })
