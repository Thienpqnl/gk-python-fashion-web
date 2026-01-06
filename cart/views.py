# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.http import require_http_methods
# import json
# from products.models import Product
# from .models import Cart, CartItem

# def _get_or_create_session_id(request):
#     if not request.session.session_key:
#         request.session.create()
#     return request.session.session_key

# def _get_cart_for_request(request):
#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(user=request.user) 
#     else:
#         session_id = _get_or_create_session_id(request)
#         cart, created = Cart.objects.get_or_create(session_id=session_id)
#     return cart


#     cart = _get_cart_for_request(request)
    
#     items = []
#     total_price = 0
#     total_quantity = 0
    
#     for item in cart.items.all():
#         try:
#             product = Product.objects.get(id=item.product_id)
#             # Ensure numeric types for JSON/JS formatting
#             product_price = int(product.price)
#             item_total = product_price * int(item.quantity)

#             items.append({
#                 'product_id': product.id,
#                 'product_title': product.title,
#                 'product_price': product_price,
#                 'product_image': product.image,
#                 'quantity': int(item.quantity),
#                 'item_total': item_total
#             })
#             total_price += item_total
#             total_quantity += int(item.quantity)
#         except Product.DoesNotExist:
#             item.delete()
#     return JsonResponse({
#         'status': 'success',
#         'data': {
#             'items': items,
#             'total_price': total_price,
#             'total_quantity': total_quantity,
#             'item_count': len(items)
#         }
# <<<<<<< Updated upstream
# =======
#     })  



# def get_cart(request):
#     cart = _get_cart_for_request(request)
#     cart_items = cart.items.all()
    
#     # 1. Lấy danh sách ID
#     product_ids = [item.product_id for item in cart_items]
    
#     # 2. Query 1 lần (Tối ưu DB)
#     products_map = Product.objects.in_bulk(product_ids)
    
#     items = []
#     total_price = 0
#     total_quantity = 0
    
#     for item in cart_items:
#         product = products_map.get(item.product_id)
        
#         # Xử lý trường hợp sản phẩm bị xóa
#         if not product:
#             item.delete()
#             continue
            
#         item_total = product.price * item.quantity
        
#         # --- XỬ LÝ ẢNH AN TOÀN ---
#         # Kiểm tra xem field image có thuộc tính .url không (đề phòng trường hợp là CharField)
#         image_val = ''
#         if product.image:
#             if hasattr(product.image, 'url'):
#                 image_val = product.image.url # Dành cho ImageField
#             else:
#                 image_val = str(product.image) # Dành cho CharField
        
#         items.append({
#             'product_id': product.id,
#             'product_title': product.title,
#             'product_price': product.price,
#             'product_image': image_val, # Đã xử lý an toàn
#             'quantity': item.quantity,
#             'item_total': item_total
#         })
        
#         total_price += item_total
#         total_quantity += item.quantity

#     return JsonResponse({
#         'status': 'success',
#         'data': {
#             'items': items,
#             'total price': total_price,      # Đã đổi lại thành 'total price' (có dấu cách) giống code cũ
#             'total_quantity': total_quantity,
#             'item_count': len(items)
#         }
# >>>>>>> Stashed changes
#     })
    
# @require_http_methods(["POST"])
# def add_to_cart(request):
#     try:
#         data = json.loads(request.body)
#         product_id  = int(data.get('product_id'))
#         qty = int(data.get('quantity', 1))
        
#         product = Product.objects.get(id=product_id)
#         cart = _get_cart_for_request(request)
        
        
#         cart_item, created = CartItem.objects.get_or_create(
            
#             cart = cart,
#             product_id = product_id,
#             defaults= {'quantity': qty}
#         )   
#         if not created : 
#             cart_item.quantity += qty
#             cart_item.save()
            
#         return JsonResponse({
#             'status': 'success',
#             'message': f'Added {qty} {product.title} to cart' 
#         })    
        
#     except Product.DoesNotExist:
#         return JsonResponse({'status' : 'error', 'message' : 'Product not found'}, status = 404)
#     except (json.JSONDecodeError, ValueError, KeyError) as e:
#         return JsonResponse({'status': 'error', 'message': f'Invalid request: {str(e)}'}, status=400)
    
# @require_http_methods(["POST"])
# def remove_from_cart(request):
#     try:
#         data = json.loads(request.body)
#         product_id = int(data.get('product_id'))
        
#         cart = _get_cart_for_request(request)
        
#         try:
#             item = cart.items.get(product_id = product_id)
#             item.delete()   
#             return JsonResponse({'status': 'success', 'message': 'Item removed from cart'})
#         except CartItem.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Item not in cart'}, status = 404)
#     except (json.JSONDecodeError, ValueError, KeyError) as e:
#         return JsonResponse({'status': 'error', 'message': f'Invalid request: {str(e)}'}, status=400)
    
    
# @require_http_methods(["POST"])
# def update_cart_item(request):
#     try: 
#         data = json.loads(request.body)
#         product_id = int(data.get('product_id'))
#         new_qty = int(data.get('quantity', 1))
        
#         if new_qty < 0:
#             return JsonResponse({'status': 'error', 'message': 'Quantity must be positive'}, status=400)
        
#         cart = _get_cart_for_request(request)
        
#         try: 
#             item = cart.items.get(product_id=product_id)
            
#             if new_qty == 0:
#                 item.delete()
#             else:
#                 item.quantity = new_qty
#                 item.save()
                
#             return JsonResponse({'status' : 'success', 'message' : 'Cart update'})
#         except CartItem.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Item not in cart'}, status=404)

#     except (json.JSONDecodeError, ValueError, KeyError) as e:
#         return JsonResponse({'status': 'error', 'message': f'Invalid request: {str(e)}'}, status=400)
    
# @require_http_methods(["POST"])
# def clear_cart(request):
#     cart = _get_cart_for_request(request)
#     cart.items.all().delete()
#     return JsonResponse({'status': 'success', 'message': 'Cart cleared'})    

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from products.models import Product
from .models import Cart, CartItem

def _get_or_create_session_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def _get_cart_for_request(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user) 
    else:
        session_id = _get_or_create_session_id(request)
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def get_cart(request):
    cart = _get_cart_for_request(request)
    cart_items = cart.items.all()
    
    # 1. Lấy danh sách ID
    product_ids = [item.product_id for item in cart_items]
    
    # 2. Query 1 lần (Tối ưu DB - thay vì query trong vòng lặp)
    products_map = Product.objects.in_bulk(product_ids)
    
    items = []
    total_price = 0
    total_quantity = 0
    
    for item in cart_items:
        product = products_map.get(item.product_id)
        
        # Xử lý trường hợp sản phẩm bị xóa khỏi DB nhưng vẫn còn trong giỏ
        if not product:
            item.delete()
            continue
            
        item_total = product.price * item.quantity
        
        # --- XỬ LÝ ẢNH AN TOÀN ---
        # Kiểm tra xem field image có thuộc tính .url không
        image_val = ''
        if product.image:
            if hasattr(product.image, 'url'):
                image_val = product.image.url # Dành cho ImageField
            else:
                image_val = str(product.image) # Dành cho CharField
        
        items.append({
            'product_id': product.id,
            'product_title': product.title,
            'product_price': product.price,
            'product_image': image_val, 
            'quantity': item.quantity,
            'item_total': item_total
        })
        
        total_price += item_total
        total_quantity += item.quantity

    return JsonResponse({
        'status': 'success',
        'data': {
            'items': items,
            'total price': total_price,      # Giữ nguyên key có dấu cách theo logic cũ của bạn
            'total_quantity': total_quantity,
            'item_count': len(items)
        }
    })
    
@require_http_methods(["POST"])
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id  = int(data.get('product_id'))
        qty = int(data.get('quantity', 1))
        
        product = Product.objects.get(id=product_id)
        cart = _get_cart_for_request(request)
        
        
        cart_item, created = CartItem.objects.get_or_create(
            
            cart = cart,
            product_id = product_id,
            defaults= {'quantity': qty}
        )   
        if not created : 
            cart_item.quantity += qty
            cart_item.save()
            
        return JsonResponse({
            'status': 'success',
            'message': f'Added {qty} {product.title} to cart' 
        })    
        
    except Product.DoesNotExist:
        return JsonResponse({'status' : 'error', 'message' : 'Product not found'}, status = 404)
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        return JsonResponse({'status': 'error', 'message': f'Invalid request: {str(e)}'}, status=400)
    
@require_http_methods(["POST"])
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        product_id = int(data.get('product_id'))
        
        cart = _get_cart_for_request(request)
        
        try:
            item = cart.items.get(product_id = product_id)
            item.delete()   
            return JsonResponse({'status': 'success', 'message': 'Item removed from cart'})
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not in cart'}, status = 404)
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        return JsonResponse({'status': 'error', 'message': f'Invalid request: {str(e)}'}, status=400)
    
    
@require_http_methods(["POST"])
def update_cart_item(request):
    try: 
        data = json.loads(request.body)
        product_id = int(data.get('product_id'))
        new_qty = int(data.get('quantity', 1))
        
        if new_qty < 0:
            return JsonResponse({'status': 'error', 'message': 'Quantity must be positive'}, status=400)
        
        cart = _get_cart_for_request(request)
        
        try: 
            item = cart.items.get(product_id=product_id)
            
            if new_qty == 0:
                item.delete()
            else:
                item.quantity = new_qty
                item.save()
                
            return JsonResponse({'status' : 'success', 'message' : 'Cart update'})
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not in cart'}, status=404)

    except (json.JSONDecodeError, ValueError, KeyError) as e:
        return JsonResponse({'status': 'error', 'message': f'Invalid request: {str(e)}'}, status=400)
    
@require_http_methods(["POST"])
def clear_cart(request):
    cart = _get_cart_for_request(request)
    cart.items.all().delete()
    return JsonResponse({'status': 'success', 'message': 'Cart cleared'})
