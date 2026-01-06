from django.contrib import admin


from .models import Review

# Cách 1: Đăng ký cơ bản (Nhanh nhất)
# admin.site.register(Review)

# Cách 2: Đăng ký xịn xò (Hiện nhiều cột để dễ xem lỗi)
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Những cột sẽ hiện ra trong danh sách
    list_display = ('id', 'user', 'product', 'rating', 'created_at')
    
    # Bộ lọc bên tay phải (lọc theo số sao, ngày tạo)
    list_filter = ('rating', 'created_at')
    
    # Thanh tìm kiếm (tìm theo tên user, tên sản phẩm)
    search_fields = ('user__username', 'product__title', 'comment')
