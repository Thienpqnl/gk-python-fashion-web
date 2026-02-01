from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from products.models import Product, Category
from reviews.models import Review
from django.db.models import Avg, Count,Q
from orders.models import Order, OrderItem
def index(request):
    """Render the home page with seasonal discounted products (limit 4)."""
    from django.conf import settings
    current_season = getattr(settings, 'CURRENT_SEASON', Product.SEASON_ALL)

    # Products explicitly for current season with a discount
    seasonal_qs = Product.objects.filter(seasonal_discount_percent__gt=0, season=current_season).order_by('-seasonal_discount_percent')
    seasonal_products = list(seasonal_qs[:4])

    # Fill with all-season discounted products if less than 4
    if len(seasonal_products) < 4:
        needed = 4 - len(seasonal_products)
        fallback = Product.objects.filter(seasonal_discount_percent__gt=0, season=Product.SEASON_ALL).exclude(id__in=[p.id for p in seasonal_products]).order_by('-seasonal_discount_percent')[:needed]
        seasonal_products.extend(list(fallback))

    categories = Category.objects.all()
    context = {
        'seasonal_products': seasonal_products,
        'categories': categories,
    }
    return render(request, 'index.html', context)


def seasonal_sales_page(request):
    """Page that lists all products on seasonal sale for the current season."""
    from django.conf import settings
    current_season = getattr(settings, 'CURRENT_SEASON', Product.SEASON_ALL)

    products = Product.objects.filter(seasonal_discount_percent__gt=0).filter(Q(season=current_season) | Q(season=Product.SEASON_ALL)).order_by('-seasonal_discount_percent')
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'sale_season': current_season,
    }
    return render(request, 'seasonal-sales.html', context)


def products_page(request):
    """Render the products listing page."""
    category_id = request.GET.get('category')
    
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    }
    return render(request, 'products.html', context)


def product_detail_page(request, product_id):
    # 1. Lấy thông tin sản phẩm
    product = get_object_or_404(Product, id=product_id)
    

    reviews = Review.objects.filter(product=product).select_related('user').order_by('-created_at')
    
    total_reviews = reviews.count()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    sentiment_stats = reviews.aggregate(
        pos=Count('id', filter=Q(sentiment='Positive')),
        neg=Count('id', filter=Q(sentiment='Negative')),
    )
    
    pos_count = sentiment_stats['pos']
    neg_count = sentiment_stats['neg']
    
    # Tính phần trăm
    if total_reviews > 0:
        pos_percent = int((pos_count / total_reviews) * 100)
        neg_percent = int((neg_count / total_reviews) * 100)
        neu_percent = 100 - pos_percent - neg_percent
    else:
        pos_percent = 0
        neg_percent = 0
        neu_percent = 0


    context = {
        'product': product,
        'reviews': reviews,     
        'review_count': total_reviews,
        'avg_rating': round(avg_rating, 1),
        'pos_percent': pos_percent,
        'neg_percent': neg_percent,
        'neu_percent': neu_percent,
    }
    

    return render(request, 'product-detail.html', context)


def cart_page(request):
    """Render the shopping cart page."""
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'cart.html', context)


def checkout_page(request):
    """Render the checkout page."""
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'checkout.html', context)


def ai_search_page(request):
    """Render the AI search page."""
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'ai-search.html', context)


def order_history_page(request):
    """Render the order history page."""
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'order-history.html', context)



def order_success(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        if order.status == 'pending': 
            order.status = 'delivered'
            order.save()
        items = OrderItem.objects.filter(order=order)
        context = {
            'result': 'success',
            'order': order,
            'items': items,
            'message': 'Đặt hàng thành công!',
            'momo_trans_id': 'Thanh toán khi nhận hàng (COD)'
        }
        return render(request, 'payment_success.html', context)

    except Order.DoesNotExist:
        return render(request, 'payment_failed.html', {'message': 'Không tìm thấy đơn hàng'})
