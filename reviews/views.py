from django.shortcuts import render


# reviews/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from orders.models import Order, OrderItem
from products.models import Product
from .models import Review # Import model từ chính app này

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def submit_review_api(request):
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        product_id = data.get('product_id')
        rating = int(data.get('rating'))
        comment = data.get('comment')

        # Logic kiểm tra giữ nguyên
        order = Order.objects.get(id=order_id, user=request.user)
        order_item = OrderItem.objects.filter(order=order, product_id=product_id).first()

        if not order_item:
             return JsonResponse({'status': 'error', 'message': 'Sản phẩm không hợp lệ'}, status=404)
        
        if order_item.is_reviewed:
             return JsonResponse({'status': 'error', 'message': 'Đã đánh giá rồi'}, status=400)

        # Tạo Review
        Review.objects.create(
            user=request.user,
            product_id=product_id,
            order=order,
            rating=rating,
            comment=comment
        )

        # Update trạng thái bên OrderItem
        order_item.is_reviewed = True
        order_item.save()

        return JsonResponse({'status': 'success', 'message': 'Đánh giá thành công'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)