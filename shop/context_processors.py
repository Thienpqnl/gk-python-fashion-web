from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
import json
from orders.models import Order
from reviews.models import Review

def admin_statistics(request):
    if request.path.startswith('/admin/'):
        # 1. Lấy năm
        current_year = timezone.now().year
        selected_year = request.GET.get('year')
        
        try:
            selected_year = int(selected_year)
        except (TypeError, ValueError):
            selected_year = current_year

        # 2. Tạo danh sách 12 tháng 
        labels = [f"{str(m).zfill(2)}/{selected_year}" for m in range(1, 13)]

        # 3. Truy vấn dữ liệu theo năm
        orders_query = Order.objects.filter(created_at__year=selected_year) \
            .annotate(month=TruncMonth('created_at')) \
            .values('month') \
            .annotate(count=Count('id'), rev=Sum('total_price')) \
            .order_by('month')

        order_counts = [0] * 12
        revenue_amounts = [0] * 12
        total_revenue = 0

        for item in orders_query:
            month_idx = item['month'].month - 1
            order_counts[month_idx] = item['count']
            rev_val = float(item['rev'] or 0)
            revenue_amounts[month_idx] = rev_val
            total_revenue += rev_val


        # 4. Thống kê Đánh giá & Bình luận
        pos = Review.objects.filter(rating__gt=3).count()
        neg = Review.objects.filter(rating__lte=3).count()
        rating_stats = Review.objects.values('rating').annotate(total=Count('id'))
        rating_counts = [0] * 5
        for item in rating_stats:
            if 1 <= item['rating'] <= 5:
                rating_counts[item['rating']-1] = item['total']

        return {
            'selected_year': selected_year,
            'total_revenue': total_revenue,
            # 'top_products': top_products,
            'chart_labels': json.dumps(labels),
            'chart_rev_data': json.dumps(revenue_amounts),
            'chart_order_data': json.dumps(order_counts),
            'chart_rating_data': json.dumps(rating_counts),
            'sentiment_data': json.dumps([pos, neg]),
        }
    return {}