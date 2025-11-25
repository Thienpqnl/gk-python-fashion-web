# Fashion E-commerce API Documentation

## Overview
Mock Fashion E-commerce API built with Django. Includes product catalog, shopping cart, orders, and search functionality.

## Base URL
```
http://localhost:8000/
```

## Endpoints

### Products API (`/api/products/`)

#### List All Products
```http
GET /api/products/
```
**Query Parameters:**
- `category` (int, optional) - Filter by category ID

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "sku": "AO-THUN-001",
      "title": "Áo Thun Mẫu #1",
      "description": "100% cotton, thoáng mát...",
      "price": 199000,
      "image": "/static/images/product-001.svg",
      "category_id": 1,
      "category_name": "Áo"
    }
  ],
  "count": 12
}
```

#### Get Product Detail
```http
GET /api/products/<product_id>/
```

#### Search Products
```http
GET /api/products/search/?q=query
```

#### Filter by Category
```http
GET /api/products/category/<category_id>/
```

### Cart API (`/api/cart/`)

#### Get Cart
```http
GET /api/cart/
```
**Response:**
```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "product_id": 1,
        "product_title": "Áo Thun Mẫu #1",
        "product_price": 199000,
        "product_image": "/static/images/product-001.svg",
        "quantity": 2,
        "item_total": 398000
      }
    ],
    "total_price": 398000,
    "total_quantity": 2,
    "item_count": 1
  }
}
```

#### Add to Cart
```http
POST /api/cart/add/
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```

#### Update Cart Item
```http
POST /api/cart/update/
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 3
}
```

#### Remove from Cart
```http
POST /api/cart/remove/
Content-Type: application/json

{
  "product_id": 1
}
```

#### Clear Cart
```http
POST /api/cart/clear/
```

### Orders API (`/api/orders/`)

#### List User Orders
```http
GET /api/orders/
```

#### Get Order Detail
```http
GET /api/orders/<order_id>/
```

#### Create Order from Cart
```http
POST /api/orders/create/
Content-Type: application/json

{
  "shipping_address": "123 Street, City"
}
```

#### Update Order Status
```http
POST /api/orders/<order_id>/update-status/
Content-Type: application/json

{
  "status": "shipped"
}
```
Valid statuses: `pending`, `processing`, `shipped`, `delivered`, `cancelled`

#### Cancel Order
```http
POST /api/orders/<order_id>/cancel/
```

### Search API (`/api/search/`)

#### Search by Text
```http
GET /api/search/text/?q=query
```

#### Search by Image
```http
POST /api/search/image/
Content-Type: multipart/form-data

image: <file>
```

#### Get Search History
```http
GET /api/search/history/
```

#### Delete Search History
```http
POST /api/search/history/delete/
```

## Web Pages

### Shop Pages
- `/` - Home page with featured products
- `/products/` - All products listing with category filter
- `/product/<id>/` - Product detail page
- `/cart/` - Shopping cart page
- `/checkout/` - Checkout page
- `/ai-search/` - Image-based search page
- `/order-history/` - Order history page

## Mock Data

### Products
12 mock products across 3 categories:
- **Áo** (T-shirts, Shirts, Jackets) - 4 products
- **Quần** (Pants, Shorts, Jeans) - 4 products
- **Đầm** (Dresses) - 4 products

### Features Implemented
✅ Product listing and filtering
✅ Product search (text)
✅ Shopping cart (session-based)
✅ Order management
✅ Image search (mock results)
✅ Search history (session-based)
✅ Admin interface (`/admin/`)

## Authentication
- Admin credentials: `admin` / `admin123`
- Admin URL: `/admin/`

## Notes
- Cart data stored in Django session (server-side)
- Order data stored in memory (mock)
- Search history stored in Django session
- Image search returns mock results (4 random products)
- All prices in Vietnamese Dong (₫)
- CSRF protection enabled for POST requests
