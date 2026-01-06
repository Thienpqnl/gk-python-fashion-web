from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Order

# --- 1. RENDER HTML (Giao diện) ---
@login_required
def order_history_view(request):
    return render(request, 'order_history.html')

@login_required
def order_detail_view(request, order_id):
    if not Order.objects.filter(id=order_id, user=request.user).exists():
        return render(request, '404.html') 
    return render(request, 'order_detail.html', {'order_id': order_id})

# --- 2. API DỮ LIỆU (JSON) ---

@login_required
def list_user_orders(request):
    """API lấy danh sách đơn hàng của user"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'status': order.status,
            'status_display': order.get_status_display(), 
            'total_money': order.total_money,
            'item_count': order.items.count(),
            'created_at': order.created_at.strftime("%d/%m/%Y %H:%M"),
        })
    
    return JsonResponse({'status': 'success', 'data': data})

@login_required
def get_order_detail(request, order_id):
    """API lấy chi tiết 1 đơn hàng"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Không tìm thấy đơn hàng'}, status=404)
    
    items = []
    for item in order.items.all():
        items.append({
            'product_title': item.product_title,
            'price': item.price,
            'quantity': item.quantity,
            'total': item.price * item.quantity,
            'image': item.product.image.url if item.product.image else ''
        })
        
    return JsonResponse({
        'status': 'success',
        'data': {
            'id': order.id,
            'status': order.status,
            'status_display': order.get_status_display(),
            'created_at': order.created_at.strftime("%H:%M %d/%m/%Y"),
            'fullname': order.fullname,
            'phone': order.phone,
            'address': order.address,
            'payment_method': order.payment_method,
            'total_money': order.total_money,
            'items': items
        }
    })


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def cancel_order(request, order_id):
    """API Hủy đơn hàng"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Không tìm thấy đơn hàng'}, status=404)
        
    if order.status != 'pending':
        return JsonResponse({'status': 'error', 'message': 'Đơn hàng đã được xử lý, không thể hủy!'}, status=400)
        
    order.status = 'cancelled'
    order.save()
    return JsonResponse({'status': 'success', 'message': 'Đã hủy đơn hàng thành công'})




# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from products.models import Product 
from cart.models import Cart

@csrf_exempt
@login_required
def create_order(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ'}, status=405)

    try:
        data = json.loads(request.body)
        selected_ids = data.get('items', [])
        
        if not selected_ids:
            return JsonResponse({'status': 'error', 'message': 'Không có sản phẩm nào để đặt'}, status=400)
        cart = Cart.objects.get(user=request.user)
        items_to_buy = cart.items.filter(product_id__in=selected_ids)
        
        if not items_to_buy.exists():
            return JsonResponse({'status': 'error', 'message': 'Sản phẩm chọn mua không còn trong giỏ hàng'}, status=400)

        # 3. Tính toán lại tổng tiền (Backend tự tính để bảo mật, không tin client)
        total_money = 0
        order_items_buffer = []

        for item in items_to_buy:
            # Lấy thông tin mới nhất từ bảng Product (giá có thể đã đổi)
            try:
                product = Product.objects.get(id=item.product_id)
                current_price = product.price
                item_total = current_price * item.quantity
                total_money += item_total
                
                # Lưu tạm vào buffer để tí nữa tạo OrderItem
                order_items_buffer.append({
                    'product_id': product.id,
                    'title': product.title,
                    'price': current_price,
                    'qty': item.quantity
                })
            except Product.DoesNotExist:
                continue # Bỏ qua nếu sản phẩm gốc đã bị xóa

        # 4. Tạo Đơn hàng (Order)
        order = Order.objects.create(
            user=request.user,
            fullname=data.get('fullname'),
            phone=data.get('phone'),
            email=data.get('email'),
            shipping_address=data.get('address'), 
            payment_method=data.get('payment_method'),
            total_price=total_money,
            status='delivered'
        )

        # 5. Tạo các chi tiết đơn hàng (OrderItem)
        for buffer in order_items_buffer:
            OrderItem.objects.create(
                order=order,
                product_id=buffer['product_id'],
                product_title=buffer['title'],
                product_price=buffer['price'],
                quantity=buffer['qty']
            )


        items_to_buy.delete() 

        return JsonResponse({
            'status': 'success', 
            'message': 'Đặt hàng thành công',
            'order_id': order.id
        })

    except Exception as e:
        print(f"Error creating order: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)