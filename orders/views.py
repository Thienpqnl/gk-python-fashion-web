# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from products.models import Product 
from cart.models import Cart
from .momo_utils import create_momo_payment # Import hàm xử lý MoMo
from django.shortcuts import render

@csrf_exempt
@login_required
def create_order(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ'}, status=405)

    try:
        data = json.loads(request.body)
        selected_ids = data.get('items', [])
        payment_method = data.get('payment_method') # Lấy phương thức thanh toán (COD hoặc MOMO)

        if not selected_ids:
            return JsonResponse({'status': 'error', 'message': 'Không có sản phẩm nào để đặt'}, status=400)
        
        cart = Cart.objects.get(user=request.user)
        items_to_buy = cart.items.filter(product_id__in=selected_ids)
        
        if not items_to_buy.exists():
            return JsonResponse({'status': 'error', 'message': 'Sản phẩm chọn mua không còn trong giỏ hàng'}, status=400)

        # 3. Tính toán lại tổng tiền
        total_money = 0
        order_items_buffer = []

        for item in items_to_buy:
            try:
                product = Product.objects.get(id=item.product_id)
                current_price = product.price
                item_total = current_price * item.quantity
                total_money += item_total
                
                order_items_buffer.append({
                    'product_id': product.id,
                    'title': product.title,
                    'price': current_price,
                    'qty': item.quantity
                })
            except Product.DoesNotExist:
                continue 

        # 4. Tạo Đơn hàng (Order)
        order = Order.objects.create(
            user=request.user,
            fullname=data.get('fullname'),
            phone=data.get('phone'),
            email=data.get('email'),
            shipping_address=data.get('address'), 
            payment_method=payment_method,
            total_price=total_money,
            status='pending' 
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

        # ========================================================
        if payment_method == 'MOMO':
            pay_url = create_momo_payment(order.id, total_money)           
            if pay_url:
                items_to_buy.delete() 
                return JsonResponse({
                    'status': 'momo_redirect', 
                    'order_id': order.id,
                    'url': pay_url
                })
            else:
                order.delete()
                return JsonResponse({'status': 'error', 'message': 'Lỗi kết nối đến cổng thanh toán MoMo'}, status=500)
        
    
            
        # Nếu là COD (Thanh toán khi nhận hàng) 
        items_to_buy.delete() 

        return JsonResponse({
            'status': 'success', 
            'message': 'Đặt hàng thành công',
            'order_id': order.id
        })

    except Exception as e:
        print(f"Error creating order: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    




def payment_return(request):
    resultCode = request.GET.get('resultCode')
    message = request.GET.get('message')
    momo_order_id = request.GET.get('orderId') 

    real_order_id = momo_order_id
    if momo_order_id and '-' in momo_order_id:
        real_order_id = momo_order_id.split('-')[0] 

    if resultCode == '0':
        try:
            order = Order.objects.get(id=real_order_id)
        
            if order.status == 'pending': 
                order.status = 'delivered'
                order.save()


            items = OrderItem.objects.filter(order=order)

            context = {
                'result': 'success',
                'order': order,      
                'items': items,
                'message': 'Giao dịch thành công!',
                'momo_trans_id': request.GET.get('transId') 
            }
            return render(request, 'payment_success.html', context)

        except Order.DoesNotExist:
            return render(request, 'payment_failed.html', {'message': 'Không tìm thấy đơn hàng'})
    else:
        return render(request, 'payment_failed.html', {'message': message})
    



# def order_success(request, order_id):
#     try:
#         order = Order.objects.get(id=order_id, user=request.user)
#         items = OrderItem.objects.filter(order=order)
#         context = {
#             'result': 'success',
#             'order': order,
#             'items': items,
#             'message': 'Đặt hàng thành công!',
#             'momo_trans_id': 'Thanh toán khi nhận hàng (COD)'
#         }
#         return render(request, 'payment_success.html', context)

#     except Order.DoesNotExist:
#         return render(request, 'payment_failed.html', {'message': 'Không tìm thấy đơn hàng'})