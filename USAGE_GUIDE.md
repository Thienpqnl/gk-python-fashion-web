# 🎯 Fashion E-commerce - Quick Start & Usage Guide

## 🚀 Getting Started

### Current Status
✅ **Server is running on**: `http://localhost:8000/`
✅ **All templates are connected to models**
✅ **Mock data is loaded (12 products)**
✅ **API endpoints are functional**
✅ **Seed data available: 12 products are loaded into the database**
---


### 1️⃣ **Home Page** (`/`)
**What you see:**
- Featured products section (first 4 products)
- Navigation menu with links to:
  - Tìm kiếm (Search)

**What to do:**
- Click "Xem sản phẩm" to go to product listing
- Click product images to view details

**What you see:**
- All 12 products in a grid
- Category filter on the left sidebar (Áo, Quần, Đầm)
**What to do:**
- **Filter products**: Click category name in sidebar to filter
  - Áo → Shows 4 shirt/jacket products
  - Quần → Shows 4 pants/shorts products
  - Đầm → Shows 4 dress products
- **View details**: Click "Chi tiết" button on any product card
- **Back to all**: Click "Tất cả" to remove filter
2. **See results**: sample products appear as placeholders
  ✅ **Server is running on**: `http://localhost:8000/`
  ✅ **Seed data available: 12 products are loaded into the database**
  ✅ **API endpoints are functional**
Đầm Nữ - ₫299,000
```

### 3️⃣ **Product Detail Page** (`/product/<id>/`)
**What you see:**
- Large product image on left
- Product info on right:
  - SKU code
  - Price
  - "Thêm vào giỏ" button (Add to Cart)
  - Additional info (category, availability, shipping)
  ...
  **What to do:**
    - Star rating shown as static placeholder (replace with real ratings later)
4. **Go to cart**: Click "Giỏ hàng" in navigation
---

### 4️⃣ **Shopping Cart** (`/cart/`)
**What you see:**
- List of items in your cart (left side)
- Each item shows:
  - Product image
  - Product name
  **What to do:**
  1. **Upload image**:
    - Click the box to select file, OR
    - Drag & drop an image
    - Supports: JPG, PNG, WebP
  2. **See results**: sample products appear as placeholders
    - (This is a placeholder flow — integrate ML model later for real image search)
  - **Total amount**
**What to do:**
1. **Adjust quantities**: 
   - Click - to decrease (minimum 1)
   - Click + to increase
   - Type directly in field
2. **Remove items**: Click "Xóa" button
  ### Seed / Load Initial Data into Database
  Use the included management command to (re)seed initial products and categories:
  python manage.py load_mock_data
  ```
  This will create categories and products in the project's database. The `fixtures/` folder and top-level scripts are no longer used.
If you add:
- 1x Quần Jeans (₫399,000) = ₫399,000
3. See sample products as results
Total: ₫797,000
```

---

**Order data**: Persisted in the database (orders stored in `orders.Order`)
Make sure views query the `Product` model (e.g. `Product.objects.all()`) instead of relying on in-file mock lists
  2. **shop/views.py** - How views pass data to templates (uses ORM queries)
  3. **products/models.py** - Product and Category models (database schema)
  4. **cart/views.py** - How cart API works (session-backed)
  5. **products/views.py** - Search & filtering logic (Django ORM)
     - Địa chỉ giao hàng (Shipping Address) *required
     - COD (Cash on Delivery) - selected by default
     - Bank transfer
  ### Next Steps
  1. **Database & persistence**
    - The project already uses a database-backed `Product` model. Use ORM queries such as `Product.objects.all()` in views.
    - Orders are already stored in the `orders.Order` model; extend as needed.
1. **Fill in form**:
   ```
   Name: Nguyễn Văn A
   Email: user@example.com
   Address: 123 Đường ABC, Quận 1, TP.HCM
   ```
2. **Choose payment method**: COD (default) or Bank
3. **Click "Đặt hàng"** (Place Order)
   - You'll see: ✓ success message with Order ID (O-[timestamp])
   - Redirects to Order History page

---

### 6️⃣ **Order History** (`/order-history/`)
**What you see:**
- Last order you placed with details:
  - Mã đơn (Order ID): O-1234567890
  - Ngày đặt (Date): 2025-11-17 23:45:30
  - Người nhận (Recipient): Your name
  - Phương thức thanh toán (Payment): COD / Bank
  - Địa chỉ giao hàng (Shipping Address)
  - Tổng cộng (Total): ₫xxx,xxx
  - Status: Đang xử lý (Processing - yellow badge)

**Info:**
- Shows your most recent order only (mock)
- Status is mock: always "Đang xử lý" (Processing)
- Data stored in browser localStorage

---

### 7️⃣ **Image Search** (`/ai-search/`)
**What you see:**
- Upload box with dashed border
- Text: "Kéo & thả ảnh vào đây hoặc click để chọn"
  (Drag & drop image or click to select)
- Preview area (shows uploaded image)
- Mock search results (4 random products)

**What to do:**
1. **Upload image**:
   - Click the box to select file, OR
   - Drag & drop an image
   - Supports: JPG, PNG, WebP
2. **See results**: 4 mock products appear
   - (This is a mock - real app would use ML for image recognition)
3. **View product**: Click "Xem chi tiết" on any result

---

## 🔧 API Endpoints Testing

### Test with Browser Developer Console (F12)

#### 1️⃣ Get All Products
```javascript
fetch('http://localhost:8000/api/products/')
  .then(r => r.json())
  .then(d => console.log(d))
```

#### 2️⃣ Filter Products by Category (Áo = 1)
```javascript
fetch('http://localhost:8000/api/products/?category=1')
  .then(r => r.json())
  .then(d => console.log(d))
```

#### 3️⃣ Search Products
```javascript
fetch('http://localhost:8000/api/products/search/?q=jeans')
  .then(r => r.json())
  .then(d => console.log(d))
```

#### 4️⃣ Get Cart
```javascript
fetch('http://localhost:8000/api/cart/')
  .then(r => r.json())
  .then(d => console.log(d))
```

#### 5️⃣ Add to Cart
```javascript
fetch('http://localhost:8000/api/cart/add/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
  },
  body: JSON.stringify({
    product_id: 1,
    quantity: 2
  })
})
  .then(r => r.json())
  .then(d => console.log(d))
```

---

## 📊 Mock Data Details

### Products by Category

#### 1. **Áo** (Shirts & Jackets) - 4 products
| # | Name | Price | SKU |
|---|------|-------|-----|
| 1 | Áo Thun Mẫu #1 | ₫199,000 | AO-THUN-001 |
| 5 | Áo Sơ Mi #5 | ₫349,000 | AO-SO-MI-005 |
| 8 | Áo Hoodie #8 | ₫399,000 | AO-HOODIE-008 |
| 11 | Áo Crop Top #11 | ₫179,000 | AO-CROP-TOP-011 |

#### 2. **Quần** (Pants & Shorts) - 4 products
| # | Name | Price | SKU |
|---|------|-------|-----|
| 2 | Quần Jeans #2 | ₫399,000 | QUAN-JEANS-002 |
| 6 | Quần Short #6 | ₫149,000 | QUAN-SHORT-006 |
| 9 | Quần Jogger #9 | ₫249,000 | QUAN-JOGGER-009 |
| 12 | Quần Kaki #12 | ₫329,000 | QUAN-KAKI-012 |

#### 3. **Đầm** (Dresses) - 4 products
| # | Name | Price | SKU |
|---|------|-------|-----|
| 3 | Đầm Nữ #3 | ₫299,000 | DAM-NU-003 |
| 7 | Váy Dạo Phố #7 | ₫449,000 | VAY-DAO-PHO-007 |
| 10 | Đầm Maxi #10 | ₫599,000 | DAM-MAXI-010 |

---

## 🛠️ Admin Interface

### Access Admin Panel
- **URL**: `http://localhost:8000/admin/`
- **Username**: `admin`
- **Password**: `admin123`

### What You Can Do:
1. **View Products**: All 12 mock products (from database after loading)
2. **View Categories**: All 3 categories
3. **View Orders**: Orders created through checkout
4. **View Cart Items**: CartItem records (if any created)
5. **Manage Users**: Create/edit admin accounts

### Load Mock Data into Database:
```bash
# Load products.json (if available)
python manage.py loaddata fixtures/products.json
```

---

## 🔄 User Journey Examples

### Journey 1: Browse & Buy
```
1. Start at home (/) → See featured products
2. Click "Xem sản phẩm" → Go to products page
3. Filter by "Áo" category → See 4 shirt products
4. Click "Chi tiết" on one → View product details
5. Select qty 2 → Click "Thêm vào giỏ"
6. See ✓ notification → Cart updated
7. Click "Giỏ hàng" → View cart with 2x item
8. Adjust qty to 1 → Total updates
9. Click "Thanh toán" → Checkout form
10. Fill form → Click "Đặt hàng"
11. See order confirmation → View order history
```

### Journey 2: Search & Add Multiple Items
```
1. Home page (/)
2. Click "Sản phẩm" → Products page
3. Search: Type "jeans" in address bar (API search)
4. See 1 result (Quần Jeans #2)
5. Click "Chi tiết" → Product page
6. Add 3x to cart
7. Back to products (click Danh sách)
8. Try another product
9. Add 2x to cart
10. Go to cart
11. See: 3x Jeans + 2x [other product]
12. Proceed to checkout
```

### Journey 3: Image Search (Mock)
```
1. Click "Tìm kiếm" → AI Search page
2. Upload any image
3. See 4 mock products as results
4. Click "Xem chi tiết"
5. Add product to cart
6. Continue shopping
```

---

## ⚠️ Important Notes

### Session & Data Persistence
- **Cart data**: Stored in Django session (expires after browser closes)
- **Order data**: Stored in memory (lost if server restarts)
- **User orders**: See only last order (localStorage)

### Resetting Data
```bash
# Clear all data (restart with fresh state)
python manage.py flush  # Warning: This deletes database!

# Restart server to clear in-memory orders
# Ctrl+C to stop, then: python manage.py runserver
```

### Testing Tips
- Use **browser DevTools** (F12) to inspect API responses
- Use **Postman** or **curl** for detailed API testing
- Check **browser console** for JavaScript errors
- Use **browser Network tab** to see API calls

---

## 📞 Troubleshooting

### Problem: "Products not showing"
- **Solution**: Check browser console (F12) for errors
- Make sure `MOCK_PRODUCTS` is imported in views.py

### Problem: "Add to cart not working"
- **Solution**: 
  1. Check CSRF token is in form
  2. Verify API endpoint URL
  3. Check Django server logs for errors

### Problem: "Cart appears empty"
- **Solution**: Session may have expired
- Try: Add product again, refresh page

### Problem: "Order not showing in history"
- **Solution**: Data is in localStorage
- Try: Hard refresh (Ctrl+F5)
- Or: Check browser DevTools → Application → localStorage

### Problem: "Server error 500"
- **Solution**: Check Django server terminal for error message
- Restart server: `Ctrl+C` then `python manage.py runserver`

---

## 🎓 Learning Resources

### Files to Study:
1. **templates/index.html** - Homepage with context variables
2. **shop/views.py** - How views pass data to templates
3. **fixtures/mock_data.py** - Where products come from
4. **cart/views.py** - How cart API works
5. **products/views.py** - Search & filtering logic

### Key Concepts:
- Django templates with `{{ variable }}` syntax
- Context dictionaries passed from views
- Session management for cart
- RESTful JSON APIs
- AJAX calls from JavaScript
- URL routing with parameters

---

## ✨ Next Steps

### To Extend This Project:
1. **Connect to real database**
   - Replace MOCK_PRODUCTS with Product.objects.all()
   - Store orders in Order model

2. **Add user authentication**
   - User login/registration
   - Save orders to user profile
   - Persistent cart per user

3. **Implement real features**
   - Payment gateway (Stripe, PayPal)
   - Email confirmations
   - Inventory tracking
   - Product reviews & ratings

4. **Improve search**
   - Elasticsearch for better search
   - Real image recognition AI

5. **Add analytics**
   - Track user behavior
   - Sales reports
   - Popular products

---

**Happy testing! 🎉**

For detailed API documentation, see: `API_DOCUMENTATION.md`
For data flow details, see: `TEMPLATE_MODEL_MAPPING.md`
