from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Category
from reviews.models import Review
from django.db.models import Avg, Count,Q

def list_products(request):
    """List all products in JSON format."""
    category_id = request.GET.get('category')
    
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    
    data = [
        {
            'id': p.id,
            'sku': p.sku,
            'title': p.title,
            'description': p.description,
            'price': p.price,
            'image': p.image,
            'category_id': p.category_id,
            'category_name': p.category.name if p.category else None
        }
        for p in products
    ]
    
    return JsonResponse({
        'status': 'success',
        'data': data,
        'count': len(data)
    })


def get_product_detail(request, product_id):
    """Get single product detail in JSON format."""
    product = get_object_or_404(Product, id=product_id)
    
    return JsonResponse({
        'status': 'success',
        'data': {
            'id': product.id,
            'sku': product.sku,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'image': product.image,
            'category_id': product.category_id,
            'category_name': product.category.name if product.category else None
        }
    })


def search_products(request):
    """Search products by title or description."""
    query = request.GET.get('q', '').lower()
    
    if not query:
        return JsonResponse({
            'status': 'error',
            'message': 'Search query is required'
        }, status=400)
    
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    
    data = [
        {
            'id': p.id,
            'sku': p.sku,
            'title': p.title,
            'description': p.description,
            'price': p.price,
            'image': p.image,
            'category_id': p.category_id,
            'category_name': p.category.name if p.category else None
        }
        for p in products
    ]
    
    return JsonResponse({
        'status': 'success',
        'query': query,
        'data': data,
        'count': len(data)
    })


def filter_by_category(request, category_id):
    """Filter products by category."""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category_id=category_id)
    
    if not products.exists():
        return JsonResponse({
            'status': 'error',
            'message': f'No products found for category {category_id}'
        }, status=404)
    
    data = [
        {
            'id': p.id,
            'sku': p.sku,
            'title': p.title,
            'description': p.description,
            'price': p.price,
            'image': p.image,
            'category_id': p.category_id,
            'category_name': p.category.name if p.category else None
        }
        for p in products
    ]
    
    return JsonResponse({
        'status': 'success',
        'category_id': category_id,
        'data': data,
        'count': len(data)
    })





def product_detail_view(request, product_id):
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
