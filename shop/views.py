from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from products.models import Product, Category


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
    """Render the product detail page."""
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    context = {
        'product': product,
        'categories': categories,
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
