# Giảm giá theo mùa (Seasonal Discounts) ✅

Tài liệu ngắn hướng dẫn cách tính và cấu hình **giảm giá theo mùa** đã triển khai trong dự án.

---

## 🔧 Tổng quan
- Mục tiêu: áp dụng **giảm giá %** cho sản phẩm theo mùa (spring, summer, autumn, winter, all).
- `Product` có hai trường liên quan: `season` và `seasonal_discount_percent`.
- Mùa hiện tại được đọc từ setting: `CURRENT_SEASON = 'spring'` (file: `fashion_backend/settings.py`).

---

## 📁 Các tệp đã thay đổi / thêm
- `products/models.py` — thêm trường `seasonal_discount_percent`, property `is_on_seasonal_sale` và `discounted_price`.
- `products/migrations/0003_add_seasonal_discount_percent.py` — migration thêm trường.
- `products/management/commands/load_mock_data.py` & `fixtures/mock_data.py` — nạp dữ liệu mẫu có giá trị giảm giá.
- `shop/views.py` — hiển thị 4 sản phẩm giảm giá trên trang chủ và trang toàn bộ giảm giá (`seasonal_sales_page`).
- `templates/index.html` và `templates/seasonal-sales.html` — hiển thị UI giảm giá.
- `products/admin.py` — hiển thị `season` và `seasonal_discount_percent` trong admin.

---

## ▶️ Cách bật & kiểm tra (quick start)
1. Chạy migration:

   ```bash
   python manage.py migrate
   ```

2. Nạp dữ liệu mẫu (xóa dữ liệu cũ và nạp lại ~30 sản phẩm):

   ```bash
   python manage.py load_mock_data
   ```

3. Chạy dev server và mở:
   - Trang chủ: `/` (hiển thị tối đa 4 sản phẩm đang giảm giá cho mùa hiện tại)
   - Trang giảm giá mùa: `/seasonal-sales/` (liệt kê tất cả sản phẩm có giảm giá áp dụng)

---

## 🛠️ Cách cấu hình mùa hiện tại
- Hiện tại mùa đặt cứng trong: `fashion_backend/settings.py`

  ```py
  CURRENT_SEASON = 'spring'  # 'spring'|'summer'|'autumn'|'winter'|'all'
  ```

- Gợi ý nâng cao: thay bằng biến môi trường hoặc model `SiteSetting` để thay đổi linh hoạt bằng admin hoặc cron.

---

## ✏️ Cách thêm/sửa giảm giá cho 1 sản phẩm
- Qua admin: chỉnh `season` và `seasonal_discount_percent` cho sản phẩm.
- Qua shell/logic:

  ```py
  p = Product.objects.get(id=1)
  p.season = Product.SEASON_SPRING
  p.seasonal_discount_percent = 20
  p.save()
  ```

- Trong code, để kiểm tra:
  - `p.is_on_seasonal_sale` → True nếu mùa khớp (hoặc `all`) và percent > 0
  - `p.discounted_price` → giá đã áp dụng giảm giá (integer)

---

## 🔎 Ví dụ truy vấn (Django ORM)
- Lấy sản phẩm đang giảm giá cho mùa hiện tại:

```py
from django.conf import settings
cur = settings.CURRENT_SEASON
Product.objects.filter(seasonal_discount_percent__gt=0).filter(Q(season=cur) | Q(season=Product.SEASON_ALL))
```

- Lấy top 4 để hiển thị trang chủ (đã thực hiện trong `shop.views.index`): tương tự nhưng thêm `.order_by('-seasonal_discount_percent')[:4]`.

---

## ✅ Kiểm tra giao diện & QA
- Kiểm tra trang chủ có hiện `seasonal_products` (tối đa 4 mục).
- Mở `/seasonal-sales/` để xem danh sách đầy đủ và đảm bảo giá hiển thị `discounted_price` và -X% badge.
- Kiểm tra `product-detail.html` hiển thị giá gốc gạch ngang và giá sau giảm.

---

## 💡 Gợi ý cải tiến (nếu muốn tiếp tục)
- Thay `CURRENT_SEASON` bằng model hoặc biến môi trường để thay đổi mà không deploy.
- Thêm management command để bật/tắt giảm giá theo lịch (cron job).
- Thêm tests đơn vị cho `is_on_seasonal_sale` và tính toán `discounted_price`.

---

Nếu cần, tôi có thể: tạo một `README` chi tiết hơn, thêm unit tests hoặc một management command để thay mùa tự động. ✨