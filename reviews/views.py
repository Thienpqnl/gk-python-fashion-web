from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from orders.models import Order, OrderItem
from products.models import Product
from .models import Review 
from django.apps import apps
from shop.ai_sentiment import predict_sentiment

@csrf_exempt
@login_required
@require_http_methods(["POST"])
# def submit_review_api(request):
#     try:
#         data = json.loads(request.body)
#         order_id = data.get('order_id')
#         product_id = data.get('product_id')
#         rating = int(data.get('rating'))
#         comment = data.get('comment')

#         # Logic kiểm tra giữ nguyên
#         order = Order.objects.get(id=order_id, user=request.user)
#         order_item = OrderItem.objects.filter(order=order, product_id=product_id).first()

#         if not order_item:
#              return JsonResponse({'status': 'error', 'message': 'Sản phẩm không hợp lệ'}, status=404)
        
#         if order_item.is_reviewed:
#              return JsonResponse({'status': 'error', 'message': 'Đã đánh giá rồi'}, status=400)

#         # Tạo Review
#         Review.objects.create(
#             user=request.user,
#             product_id=product_id,
#             order=order,
#             rating=rating,
#             comment=comment
#         )

#         # Update trạng thái bên OrderItem
#         order_item.is_reviewed = True
#         order_item.save()

#         return JsonResponse({'status': 'success', 'message': 'Đánh giá thành công'})

#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)








def submit_review_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            product_id = data.get('product_id')
            comment = data.get('comment', '')
            rating = int(data.get('rating', 5))


            #Update trạng thái bên OrderItem
            order = Order.objects.get(id=order_id, user=request.user)
            order_item = OrderItem.objects.filter(order=order, product_id=product_id).first()

            if not order_item:
             return JsonResponse({'status': 'error', 'message': 'Sản phẩm không hợp lệ'}, status=404)
        
            if order_item.is_reviewed:
             return JsonResponse({'status': 'error', 'message': 'Đã đánh giá rồi'}, status=400)

            if Review.objects.filter(order_id=order_id, product_id=product_id).exists():
                return JsonResponse({'status': 'error', 'message': 'Bạn đã đánh giá sản phẩm này rồi!'})


            label_id, confidence = predict_sentiment(comment)


            label_map = {
                0: 'Positive',  # Tích cực
                1: 'Negative',  # Phản cảm 
                2: 'Negative'   # Tiêu cực
            }
            
 
            sentiment_label = label_map.get(label_id, 'Neutral')

            # # (Tùy chọn) Logic bổ sung: 
            # if rating >= 4 and sentiment_label == 'Negative' and confidence < 0.6:
            #      sentiment_label = 'Positive'

            # 4. Lưu vào Database
            Review.objects.create(
                user=request.user,
                product_id=product_id,
                order_id=order_id,
                rating=rating,
                comment=comment,
                sentiment=sentiment_label 
            )


            
            order_item.is_reviewed = True
            order_item.save()
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Đánh giá thành công!',
                'ai_result': sentiment_label 
            })

        except Exception as e:
            print(f"Lỗi submit review: {e}")
            return JsonResponse({'status': 'error', 'message': 'Có lỗi xảy ra phía server'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid Method'})