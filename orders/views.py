from django.shortcuts import render
from django.http import JsonResponse
import json
from datetime import datetime
from orders.models import Order, OrderItem
from products.models import Product


def list_user_orders(request):
    """List all orders for current user."""
    # For unauthenticated users, we'll use session
    orders = Order.objects.all().order_by('-created_at')
    
    data = []
    for order in orders:
        items = []
        for item in order.items.all():
            items.append({
                'product_id': item.product_id,
                'product_title': item.product_title,
                'product_price': item.product_price,
                'quantity': item.quantity,
                'item_total': item.product_price * item.quantity
            })
        
        data.append({
            'id': order.id,
            'status': order.status,
            'total_price': order.total_price,
            'items': items,
            'shipping_address': order.shipping_address,
            'created_at': order.created_at.isoformat()
        })
    
    return JsonResponse({
        'status': 'success',
        'data': data,
        'count': len(data)
    })


def get_order_detail(request, order_id):
    """Get details of a specific order."""
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Order not found'
        }, status=404)
    
    items = []
    for item in order.items.all():
        items.append({
            'product_id': item.product_id,
            'product_title': item.product_title,
            'product_price': item.product_price,
            'quantity': item.quantity,
            'item_total': item.product_price * item.quantity
        })
    
    return JsonResponse({
        'status': 'success',
        'data': {
            'id': order.id,
            'status': order.status,
            'total_price': order.total_price,
            'items': items,
            'shipping_address': order.shipping_address,
            'created_at': order.created_at.isoformat()
        }
    })


def create_order_from_cart(request):
    """Create order from cart."""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'POST method required'
        }, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Get cart from session
        cart = request.session.get('cart', {})
        if not cart:
            return JsonResponse({
                'status': 'error',
                'message': 'Cart is empty'
            }, status=400)
        
        # Build order items
        order_items_data = []
        total_price = 0
        
        for product_id_str, qty in cart.items():
            product_id = int(product_id_str)
            try:
                product = Product.objects.get(id=product_id)
                item_total = product.price * qty
                order_items_data.append({
                    'product': product,
                    'qty': qty,
                    'price': product.price,
                    'title': product.title
                })
                total_price += item_total
            except Product.DoesNotExist:
                continue
        
        if not order_items_data:
            return JsonResponse({
                'status': 'error',
                'message': 'No valid products in cart'
            }, status=400)
        
        # Create order
        order = Order.objects.create(
            status='pending',
            total_price=total_price,
            shipping_address=data.get('shipping_address', '')
        )
        
        # Create order items
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product_id=item_data['product'].id,
                product_title=item_data['title'],
                product_price=item_data['price'],
                quantity=item_data['qty']
            )
        
        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True
        
        return JsonResponse({
            'status': 'success',
            'message': 'Order created successfully',
            'data': {
                'id': order.id,
                'status': order.status,
                'total_price': order.total_price,
                'created_at': order.created_at.isoformat()
            }
        })
    
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Invalid request: {str(e)}'
        }, status=400)


def update_order_status(request, order_id):
    """Update order status."""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'POST method required'
        }, status=405)
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Order not found'
        }, status=404)
    
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        
        valid_statuses = [choice[0] for choice in Order.ORDER_STATUS_CHOICES]
        if new_status not in valid_statuses:
            return JsonResponse({
                'status': 'error',
                'message': f'Invalid status. Valid: {valid_statuses}'
            }, status=400)
        
        order.status = new_status
        order.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Order status updated to {new_status}',
            'data': {
                'id': order.id,
                'status': order.status
            }
        })
    
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Invalid request: {str(e)}'
        }, status=400)


def cancel_order(request, order_id):
    """Cancel an order."""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'POST method required'
        }, status=405)
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Order not found'
        }, status=404)
    
    if order.status in ['shipped', 'delivered', 'cancelled']:
        return JsonResponse({
            'status': 'error',
            'message': f'Cannot cancel order with status: {order.status}'
        }, status=400)
    
    order.status = 'cancelled'
    order.save()
    
    return JsonResponse({
        'status': 'success',
        'message': 'Order cancelled',
        'data': {
            'id': order.id,
            'status': order.status
        }
    })
