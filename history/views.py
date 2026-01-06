# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from orders.models import Order, OrderItem 

# --- 1. RENDER HTML (Giao diện) ---
@login_required(login_url='/accounts/login/') # Chuyển hướng nếu chưa đăng nhập
def order_history_view(request):
    return render(request, 'order-history.html')

# --- 2. API DỮ LIỆU (JSON) ---

@login_required
def list_user_orders(request):
    """API lấy danh sách đơn hàng của user"""
    # Chỉ lấy đơn của user đang đăng nhập
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'status': order.status, 
            'total_money': order.total_price, # Chú ý: trong Model bạn đặt là total_price hay total_money? Sửa cho khớp nhé.
            'created_at': order.created_at.strftime("%d/%m/%Y %H:%M"),
        })
    
    return JsonResponse({'status': 'success', 'data': data})

@login_required
def get_order_detail(request, order_id):
    """API lấy chi tiết 1 đơn hàng (kèm sản phẩm)"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Không tìm thấy đơn hàng'}, status=404)
    
    items = []
    for item in order.items.all():
        items.append({
            'product_title': item.product_title,
            'price': item.product_price,
            'quantity': item.quantity,
            # Nếu item.product là ForeignKey -> item.product.image.url
            # Nếu bạn lưu cứng link ảnh trong OrderItem -> item.product_image
            'image': '', # Tạm để trống hoặc xử lý tùy Model của bạn
            'product_id': item.product_id, # ID sản phẩm thật
            'is_reviewed': item.is_reviewed  # Trạng thái đã đánh giá chưa
        })
        
    return JsonResponse({
        'status': 'success',
        'data': {
            'id': order.id,
            'status': order.status,
            'total_money': order.total_price,
            'created_at': order.created_at.strftime("%H:%M %d/%m/%Y"),
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
        return JsonResponse({'status': 'error', 'message': 'Đơn hàng đã xử lý, không thể hủy!'}, status=400)
        
    order.status = 'cancelled'
    order.save()
    return JsonResponse({'status': 'success', 'message': 'Đã hủy đơn hàng thành công'})