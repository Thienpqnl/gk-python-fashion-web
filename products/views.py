from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category


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
