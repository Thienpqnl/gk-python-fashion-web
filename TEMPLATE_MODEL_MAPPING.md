# Template - Model - Data Linking Summary

## 🔗 Connection Overview

### Web Pages & Views

| Page URL | View Function | Models Used | Data Source |
|----------|---------------|-------------|-------------|
| `/` | `shop.views.index` | Product, Category | Database — `Product.objects.all()[:4]` |
| `/products/` | `shop.views.products_page` | Product, Category | Database — `Product.objects.all()` |
| `/product/<id>/` | `shop.views.product_detail_page` | Product | Database — `Product.objects.get(id=...)` |
| `/cart/` | `shop.views.cart_page` | Cart (Session) | Session cart data (products from DB) |
| `/checkout/` | `shop.views.checkout_page` | Order | Session cart → creates `orders.Order` records |
| `/ai-search/` | `shop.views.ai_search_page` | Search | Placeholder/sample results (integrate ML later) |
| `/order-history/` | `shop.views.order_history_page` | Order | Database — `orders.Order` (persisted orders) |

### API Endpoints & Data Flow

```
┌─────────────────┐
│   Frontend      │
│   (Templates)   │
└────────┬────────┘
         │
    API Calls (AJAX)
         │
         ▼
┌─────────────────────────────────────────────────────┐
│         Django API Views (JSON Response)             │
├─────────────────────────────────────────────────────┤
│  /api/products/          → List/Filter Products     │
│  /api/products/<id>/     → Product Detail           │
│  /api/cart/              → Cart Operations          │
│  /api/orders/            → Order Management         │
│  /api/search/            → Search & History         │
└────────┬──────────────────────────────────────────┬─┘
         │                                           │
   Database (seeded)                          Session/DB
       │                                           │
       ▼                                           ▼
┌────────────────────────────┐             ┌─────────────────────┐
│  Product / Category tables  │             │  Django Session     │
│  (seeded into DB via       │             │  (Cart, History)    │
│   management command)      │             │                     │
└────────────────────────────┘             └─────────────────────┘
```

## 📦 Data Model Mapping

### Products

**Model: `products.models.Product`**
```python
{
    'id': int,
    'sku': str,
    'title': str,
    'description': str,
    'price': int,
    'image': str,
    'category': ForeignKey → Category,
    'created_at': datetime
}
```

**Seed Data:** products and categories are created in the database (12 products across 3 categories)
 - Categories: Áo (4), Quần (4), Đầm (4)
 - Price range: ₫149,000 - ₫699,000

---

### Cart

**Model: `cart.models.Cart`**
```python
{
    'user': ForeignKey → User (optional),
    'session_id': str,
    'created_at': datetime,
    'updated_at': datetime
}
```

**Storage: Django Session**
```python
request.session['cart'] = {
    'product_id_str': quantity,
    '1': 2,  # 2x product #1
    '3': 1   # 1x product #3
}
```

**API Response**
```json
{
    "items": [
        {
            "product_id": 1,
            "product_title": "...",
            "product_price": 199000,
            "quantity": 2,
            "item_total": 398000
        }
    ],
    "total_price": 398000,
    "total_quantity": 2
}
```

---

### Orders

**Model: `orders.models.Order`**
```python
{
    'id': int,
    'user': ForeignKey → User (optional),
    'status': str,  # pending, processing, shipped, delivered
    'total_price': int,
    'shipping_address': str,
    'created_at': datetime,
    'updated_at': datetime
}
```

**Orders Storage: Database (`orders.Order`)**
Orders are created as `Order` and `OrderItem` records in the database when checkout is completed.

**Frontend Storage: localStorage**
```javascript
localStorage.setItem('lastOrder', JSON.stringify({
    id: 'O-1234567890',
    fullname: 'Nguyễn Văn A',
    email: 'user@example.com',
    address: '123 Street, City',
    payment_method: 'cod',
    total: 598000,
    createdAt: '2025-11-17T...'
}));
```

---

### Search

**Model: `search.models.SearchQuery`**
```python
{
    'id': int,
    'query_text': str,
    'results_count': int,
    'created_at': datetime
}
```

**Search History: Session**
```python
request.session['search_history'] = [
   {
      'query': 'jeans',
      'results_count': 4,
      'timestamp': '...'
   }
]
```

---

## 🔄 Data Flow Examples

### Example 1: Adding Product to Cart

```
1. Frontend: Click "Thêm vào giỏ" button
   └─ Collect product_id, quantity
   └─ POST to /api/cart/add/

2. Backend: cart.views.add_to_cart()
   └─ Parse JSON body
   └─ Get product from DB: Product.objects.get(id=product_id)
   └─ Update request.session['cart']
   └─ Return { status: 'success' }

3. Frontend: Update UI
   └─ Show toast "✓ Đã thêm vào giỏ"
   └─ Auto-redirect to cart page
```

### Example 2: Viewing Product Details

```
1. Frontend: Click product link
   └─ Navigate to /product/1/

2. Backend: shop.views.product_detail_page(request, 1)
   └─ Query DB: `Product.objects.get(id=1)`
   └─ Render template with product data

3. Frontend: Display product.html
   └─ Show: title, description, price, image
   └─ Category from product.category_name
   └─ Add to cart button (API call)
```

### Example 3: Checkout & Order Creation

```
1. Frontend: User fills checkout form
   └─ POST /api/orders/create/

2. Backend: orders.views.create_order_from_cart()
   └─ Get cart from session
   └─ Build Order and OrderItem records from DB product data
   └─ Calculate total_price
   └─ Persist order and order items in the database
   └─ Clear session['cart']
   └─ Return order data

3. Frontend: Save to localStorage
   └─ localStorage.setItem('lastOrder', ...)
   └─ Navigate to /order-history/
   └─ Display order confirmation
```

---

## 📊 Data Sources

| Data | Source | Storage | Lifetime |
|------|--------|---------|----------|
| Products | `products.Product` (DB) | Database | Persistent (DB) |
| Categories | `products.Category` (DB) | Database | Persistent (DB) |
| Cart Items | Form input | Session | User session (expires) |
| Orders | `orders.Order` (DB) | Database | Persistent (DB) |
| Search History | Text query | Session | User session (expires) |
| User Info | Form input | localStorage | Browser storage |

---

## 🛠️ Testing Data

### Sample Products for Testing
```python
# Category: Áo (T-shirts)
Product #1: Áo Thun Mẫu - ₫199,000

# Category: Quần (Pants)  
Product #2: Quần Jeans - ₫399,000

# Category: Đầm (Dresses)
Product #3: Đầm Nữ - ₫299,000

# Add to cart: 2x #1 + 1x #2
# Total: (199,000 × 2) + (399,000 × 1) = ₫797,000
```

### API Testing with cURL

```bash
# Get all products
curl http://localhost:8000/api/products/

# Get products in Áo category
curl http://localhost:8000/api/products/category/1/

# Add to cart
curl -X POST http://localhost:8000/api/cart/add/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}' \
  -b "sessionid=..."

# Get cart
curl http://localhost:8000/api/cart/ \
  -b "sessionid=..."
```

---

## ✅ Implementation Checklist

-- [x] Product models & seed data
-- [x] Category models & seed data
-- [x] Shop views (all pages)
-- [x] Products API views & endpoints (ORM)
-- [x] Cart views & session management
-- [x] Orders views & DB persistence
-- [x] Search views & session history
- [x] Templates with Django tags
- [x] CSRF token handling
- [x] AJAX API calls in templates
- [x] Admin interface setup
- [x] Static files & Tailwind CSS

---

## 📝 Next Steps (If Continuing Development)

1. **Database Integration**
   - Replace mock data with database queries
   - Create real Order records instead of in-memory storage
   - Implement user authentication & permissions

2. **Frontend Enhancements**
   - Add loading states & spinners
   - Form validation & error handling
   - Responsive mobile UI improvements

3. **Search & Recommendations**
   - Implement real image search (ML model)
   - Add AI-powered product recommendations
   - Search analytics & trending products

4. **Payment Gateway**
   - Integrate Stripe/PayPal/VNPay
   - Handle payment callbacks
   - Invoice generation

5. **Admin Features**
   - Order management dashboard
   - Product inventory tracking
   - User management
   - Sales analytics
