from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from products.models import Product, Category
from reviews.models import Review
from django.db.models import Avg, Count,Q
def index(request):
    """Render the home page with featured products."""
    featured_products = Product.objects.all()[:4]
    categories = Category.objects.all()
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'index.html', context)


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
