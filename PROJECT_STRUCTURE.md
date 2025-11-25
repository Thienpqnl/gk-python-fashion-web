# 📋 Project Structure & File Organization

## 📁 Complete Directory Tree

```
fashion-python-web1/
│
├── 📄 manage.py                    ← Django management script
├── 📄 db.sqlite3                   ← Database file (auto-created)
├── 📄 create_admin.py              ← Script to create admin user
├── 📄 requirements.txt             ← Python dependencies (Django)
├── 📄 tailwind.config.js           ← Tailwind CSS config
├── 📄 README.md                    ← Original project README
│
├── 📚 DOCUMENTATION FILES
│   ├── 📄 README_IMPLEMENTATION.md ← Implementation summary
│   ├── 📄 API_DOCUMENTATION.md     ← Full API reference
│   ├── 📄 TEMPLATE_MODEL_MAPPING.md ← Data flow & connections
│   ├── 📄 USAGE_GUIDE.md           ← Quick start guide
│   └── 📄 PROJECT_STRUCTURE.md     ← This file
│
├── 📁 fashion_backend/             ← Django project configuration
│   ├── 📄 __init__.py
│   ├── 📄 settings.py              ← Django settings
│   ├── 📄 urls.py                  ← Main URL router
│   └── 📄 wsgi.py                  ← WSGI configuration
│
├── 📁 fixtures/                    ← Data fixtures
│   ├── 📄 __init__.py
│   ├── 📄 mock_data.py            ← 12 mock products + 3 categories
│   └── 📄 products.json           ← JSON fixture (optional)
│
├── 📁 shop/                        ← Main app - Web pages
│   ├── 📄 __init__.py
│   ├── 📄 models.py               ← (No custom models)
│   ├── 📄 admin.py                ← Admin configuration
│   ├── 📄 apps.py
│   ├── 📄 views.py                ← 7 Shop page views
│   ├── 📄 urls.py                 ← 7 Shop page routes
│   └── 📁 migrations/
│       └── 📄 __init__.py
│
├── 📁 products/                    ← Products app - API
│   ├── 📄 __init__.py
│   ├── 📄 models.py               ← Product, Category models
│   ├── 📄 admin.py                ← Admin interface
│   ├── 📄 apps.py
│   ├── 📄 views.py                ← 4 API endpoints
│   ├── 📄 urls.py                 ← 4 API routes
│   └── 📁 migrations/
│       ├── 📄 __init__.py
│       └── 📄 0001_initial.py
│
├── 📁 cart/                        ← Cart app - Session-based
│   ├── 📄 __init__.py
│   ├── 📄 models.py               ← Cart, CartItem models
│   ├── 📄 admin.py                ← Admin interface
│   ├── 📄 apps.py
│   ├── 📄 views.py                ← 5 API endpoints
│   ├── 📄 urls.py                 ← 5 API routes
│   └── 📁 migrations/
│       ├── 📄 __init__.py
│       └── 📄 0001_initial.py
│
├── 📁 orders/                      ← Orders app - Mock storage
│   ├── 📄 __init__.py
│   ├── 📄 models.py               ← Order, OrderItem models
│   ├── 📄 admin.py                ← Admin interface
│   ├── 📄 apps.py
│   ├── 📄 views.py                ← 5 API endpoints
│   ├── 📄 urls.py                 ← 5 API routes
│   └── 📁 migrations/
│       ├── 📄 __init__.py
│       └── 📄 0001_initial.py
│
├── 📁 search/                      ← Search app
│   ├── 📄 __init__.py
│   ├── 📄 models.py               ← SearchQuery, SearchResult models
│   ├── 📄 admin.py                ← Admin interface
│   ├── 📄 apps.py
│   ├── 📄 views.py                ← 4 API endpoints
│   ├── 📄 urls.py                 ← 4 API routes
│   └── 📁 migrations/
│       ├── 📄 __init__.py
│       └── 📄 0001_initial.py
│
├── 📁 templates/                   ← HTML templates
│   ├── 📄 index.html              ← Home page
│   ├── 📄 products.html           ← Product listing
│   ├── 📄 product-detail.html     ← Product detail
│   ├── 📄 cart.html               ← Shopping cart
│   ├── 📄 checkout.html           ← Checkout form
│   ├── 📄 ai-search.html          ← Image search
│   └── 📄 order-history.html      ← Order history
│
└── 📁 static/                      ← Static files
    ├── 📁 images/                 ← Product images
    │   ├── 📄 logo1.png
    │   ├── 📄 product-001.svg
    │   ├── 📄 product-002.svg
    │   └── ... (12 total)
    └── 📁 js/
        └── 📄 cart.js             ← Cart JavaScript helpers

```

---

## 🔄 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  USER BROWSER                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  HTML Templates (7 files)                        │  │
│  │  - index.html                                    │  │
│  │  - products.html                                 │  │
│  │  - product-detail.html                           │  │
│  │  - cart.html (AJAX loaded)                       │  │
│  │  - checkout.html                                 │  │
│  │  - ai-search.html                                │  │
│  │  - order-history.html                            │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────┬──────────────────────────────────────┘
                  │
        HTTP/AJAX Requests
                  │
        ┌─────────▼──────────┐
        │ URL Router         │
        │ (fashion_backend   │
        │  .urls)            │
        └─────────┬──────────┘
                  │
    ┌─────────────┼──────────────┐
    │             │              │
    ▼             ▼              ▼
┌──────────────┬──────────────┬──────────────┐
│  Shop Views  │  API Views   │ Admin Site   │
├──────────────┼──────────────┼──────────────┤
│ Renders HTML │ Returns JSON │ Django Admin │
│ • index      │ • products   │ • Models     │
│ • products   │ • cart       │ • Create/Edit│
│ • detail     │ • orders     │              │
│ • cart page  │ • search     │              │
│ • checkout   │              │              │
│ • ai-search  │              │              │
│ • history    │              │              │
└──────────────┴──────────────┴──────────────┘
    │              │              │
    └──────────────┼──────────────┘
                   │
    ┌──────────────▼──────────────┐
    │   Data Sources              │
    ├─────────────────────────────┤
    │ • MOCK_PRODUCTS (12)        │
    │ • MOCK_CATEGORIES (3)       │
    │ • Session['cart']           │
    │ • Session['search_history'] │
    │ • In-memory Orders dict     │
    │ • localStorage (lastOrder)  │
    └─────────────────────────────┘
```

---

## 📊 Models & Databases

### Model Relationships

```
Product ─── ForeignKey ──► Category
   │                          │
   │                          │
   └──◄─ Category.product_set

Cart ─── OneToOneField ──► User (optional)
 │
 └─ CartItem (many)
     │
     └─ product_id (int ref to Product)

Order ─── ForeignKey ──► User (optional)
 │
 └─ OrderItem (many)
     │
     ├─ product_id (int ref)
     ├─ product_price (snapshot)
     └─ quantity

SearchQuery ─── (Session stored)
 │
 └─ SearchResult (many)
     └─ product_id (int ref)
```

### Database Tables (Auto-created)
```
✓ products_category
✓ products_product
✓ cart_cart
✓ cart_cartitem
✓ orders_order
✓ orders_orderitem
✓ search_searchquery
✓ search_searchresult
✓ auth_user
✓ auth_group
✓ django_session
+ (auto admin/content_type tables)
```

---

## 🛣️ URL Routing Map

### Shop URLs (Template Pages)
```
/                                    → index (home)
/products/                           → products_page (list all)
/products/?category=1                → filter by category
/product/<id>/                       → product_detail_page
/cart/                               → cart_page
/checkout/                           → checkout_page
/ai-search/                          → ai_search_page
/order-history/                      → order_history_page
```

### API URLs (JSON Endpoints)
```
/api/products/                       → GET list products
/api/products/<id>/                  → GET product detail
/api/products/search/?q=...          → GET search
/api/products/category/<id>/         → GET by category

/api/cart/                           → GET cart
/api/cart/add/                       → POST add item
/api/cart/update/                    → POST update qty
/api/cart/remove/                    → POST remove item
/api/cart/clear/                     → POST clear cart

/api/orders/                         → GET list orders
/api/orders/<id>/                    → GET order detail
/api/orders/create/                  → POST create order
/api/orders/<id>/update-status/      → POST update status
/api/orders/<id>/cancel/             → POST cancel

/api/search/text/?q=...              → GET text search
/api/search/image/                   → POST image search
/api/search/history/                 → GET history
/api/search/history/delete/          → POST clear history
```

### Admin URLs
```
/admin/                              → Login
/admin/auth/user/                    → Manage users
/admin/products/product/             → Manage products
/admin/products/category/            → Manage categories
/admin/orders/order/                 → Manage orders
/admin/cart/cart/                    → View carts
/admin/search/searchquery/           → View searches
```

---

## 📝 View Functions Summary

### Shop App (7 views)
| View | URL | Template | Data Context |
|------|-----|----------|--------------|
| index | / | index.html | featured_products, categories |
| products_page | /products/ | products.html | products, categories, selected_category |
| product_detail_page | /product/<id>/ | product-detail.html | product, categories |
| cart_page | /cart/ | cart.html | categories |
| checkout_page | /checkout/ | checkout.html | categories |
| ai_search_page | /ai-search/ | ai-search.html | categories |
| order_history_page | /order-history/ | order-history.html | categories |

### Products API (4 endpoints)
| Endpoint | Method | Response | Data |
|----------|--------|----------|------|
| /api/products/ | GET | JSON list | MOCK_PRODUCTS, filtered |
| /api/products/<id>/ | GET | JSON object | Single product |
| /api/products/search/ | GET | JSON list | Filtered by query |
| /api/products/category/<id>/ | GET | JSON list | Filtered by category |

### Cart API (5 endpoints)
| Endpoint | Method | Storage | Purpose |
|----------|--------|---------|---------|
| /api/cart/ | GET | Session | Get cart contents |
| /api/cart/add/ | POST | Session | Add item |
| /api/cart/update/ | POST | Session | Update quantity |
| /api/cart/remove/ | POST | Session | Remove item |
| /api/cart/clear/ | POST | Session | Clear all |

### Orders API (5 endpoints)
| Endpoint | Method | Storage | Purpose |
|----------|--------|---------|---------|
| /api/orders/ | GET | Memory | List orders |
| /api/orders/<id>/ | GET | Memory | Get order detail |
| /api/orders/create/ | POST | Memory | Create from cart |
| /api/orders/<id>/update-status/ | POST | Memory | Update status |
| /api/orders/<id>/cancel/ | POST | Memory | Cancel order |

### Search API (4 endpoints)
| Endpoint | Method | Storage | Purpose |
|----------|--------|---------|---------|
| /api/search/text/ | GET | Session | Text search |
| /api/search/image/ | POST | Session | Image search mock |
| /api/search/history/ | GET | Session | Get history |
| /api/search/history/delete/ | POST | Session | Clear history |

---

## 🔐 Security Features

### Implemented
```
✓ CSRF Protection (CsrfViewMiddleware)
✓ Session Security (HTTPS ready)
✓ Admin Authentication (username/password)
✓ XFrame Options (X-Frame-Options middleware)
```

### Settings in fashion_backend/settings.py
```python
DEBUG = True                          # Set False for production
SECRET_KEY = 'replace-with-secure'   # Change for production
ALLOWED_HOSTS = []                   # Add domains for production

# Middleware includes CSRF & auth checks
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',        # ← CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

## 📦 Dependencies

### Installed Packages
```
Django>=4.2,<5           ← Web framework
asgiref<4,>=3.6.0        ← ASGI (auto-installed)
sqlparse>=0.3.1          ← SQL parsing (auto-installed)
tzdata                   ← Timezone data (auto-installed)
```

### Not Included (Optional for Production)
- djangorestframework (for advanced APIs)
- django-cors-headers (for CORS)
- Pillow (for image processing)
- celery (for async tasks)

---

## 🚀 Key Files to Understand

### Start Here
1. `fixtures/mock_data.py` - See what products exist
2. `shop/views.py` - How pages are rendered
3. `templates/index.html` - How templates use data

### Then Study
4. `products/views.py` - API logic
5. `cart/views.py` - Session management
6. `orders/views.py` - Order creation

### Advanced
7. `fashion_backend/settings.py` - Django configuration
8. `fashion_backend/urls.py` - URL routing

---

## 💾 Data Persistence

### Session Data (expires)
```
request.session['cart'] = {
    '1': 2,      # 2x product 1
    '3': 1       # 1x product 3
}

request.session['search_history'] = [
    {'query': 'jeans', 'results_count': 1, 'timestamp': '...'},
    {'query': 'áo', 'results_count': 4, 'timestamp': '...'}
]
```

### In-Memory Storage (lost on restart)
```python
# In orders/views.py
_mock_orders = {
    1001: {'id': 1001, 'status': 'pending', ...},
    1002: {'id': 1002, 'status': 'shipped', ...}
}
```

### Browser Storage (localStorage)
```javascript
// Order info saved by checkout.html
localStorage.setItem('lastOrder', JSON.stringify({
    id: 'O-1234567890',
    fullname: '...',
    email: '...',
    address: '...'
}))
```

---

## ✅ Development Checklist

- [x] Django project setup
- [x] 5 apps created (shop, products, cart, orders, search)
- [x] Models defined for all entities
- [x] Admin interface configured
- [x] Migrations created & applied
- [x] Mock data created
- [x] Templates created & linked to views
- [x] Shop views render pages with context
- [x] API endpoints return JSON
- [x] Session-based cart management
- [x] Order mock storage
- [x] Search functionality
- [x] Static files configured
- [x] CSRF protection enabled
- [x] Documentation completed

---

## 🔧 Common Commands

### Django Management
```bash
# Create/apply migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# or use: python create_admin.py

# Load fixtures
python manage.py loaddata fixtures/products.json

# Run development server
python manage.py runserver

# Django shell (interactive)
python manage.py shell

# Check for issues
python manage.py check
```

---

## 📞 File Organization Tips

### By Feature
- `shop/` - Everything for customer-facing pages
- `products/` - Product API endpoints
- `cart/` - Shopping cart operations
- `orders/` - Order management
- `search/` - Search functionality

### By Type
- `*/models.py` - Database models
- `*/views.py` - View/API logic
- `*/urls.py` - URL routes
- `*/admin.py` - Admin customization
- `templates/` - HTML files
- `static/` - CSS, JS, images
- `fixtures/` - Mock data

---

## 🎯 Summary

This project structure implements:
1. **Clean Separation of Concerns** - Each app has a specific role
2. **RESTful API Design** - JSON endpoints for all operations
3. **Template Rendering** - Django templates with context data
4. **Mock Data Pattern** - Easy to swap for real database
5. **Session Management** - Server-side cart storage
6. **Admin Interface** - Built-in management panel

Perfect for understanding Django MVC architecture while keeping complexity manageable!

---

**For questions, see: USAGE_GUIDE.md or API_DOCUMENTATION.md**
