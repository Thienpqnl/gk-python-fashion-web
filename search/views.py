from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from products.models import Product


def search_by_image(request):
    """Search products by image upload (mock)."""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'POST method required'
        }, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({
            'status': 'error',
            'message': 'No image file provided'
        }, status=400)
    
    # Mock: return first 4 products
    # In real app, would run ML model for image similarity
    products = Product.objects.all()[:4]
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
        'message': 'Image search completed (mock results)',
        'data': data,
        'count': len(data)
    })


def search_by_text(request):
    """Search products by text query."""
    query = request.GET.get('q', '').lower()
    
    if not query:
        return JsonResponse({
            'status': 'error',
            'message': 'Search query is required'
        }, status=400)
    
    # Search in title and description
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
    
    # Store search query
    search_record = {
        'query': query,
        'results_count': len(data),
        'timestamp': __import__('datetime').datetime.now().isoformat()
    }
    
    # Store in session
    if 'search_history' not in request.session:
        request.session['search_history'] = []
    request.session['search_history'].append(search_record)
    request.session.modified = True
    
    return JsonResponse({
        'status': 'success',
        'query': query,
        'data': data,
        'count': len(data)
    })


def get_search_history(request):
    """Get user's search history."""
    history = request.session.get('search_history', [])
    
    return JsonResponse({
        'status': 'success',
        'data': history,
        'count': len(history)
    })


def delete_search_history(request):
    """Clear search history."""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'POST method required'
        }, status=405)
    
    request.session['search_history'] = []
    request.session.modified = True
    
    return JsonResponse({
        'status': 'success',
        'message': 'Search history cleared'
    })
