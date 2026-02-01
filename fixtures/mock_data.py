# Mock categories and ~30 mock products for load_mock_data command

MOCK_CATEGORIES = [
    {'id': 1, 'name': 'Tops'},
    {'id': 2, 'name': 'Bottoms'},
    {'id': 3, 'name': 'Dresses'},
    {'id': 4, 'name': 'Outerwear'},
    {'id': 5, 'name': 'Accessories'},
    {'id': 6, 'name': 'Shoes'},
]

MOCK_PRODUCTS = [
    {'id': 1, 'sku': 'TOP-001', 'title': 'Basic White Tee', 'description': 'Lightweight cotton tee', 'price': 199, 'image': '', 'category_id': 1, 'season': 'all', 'seasonal_discount_percent': 10},
    {'id': 2, 'sku': 'TOP-002', 'title': 'Striped Long Sleeve', 'description': 'Classic striped long sleeve top', 'price': 249, 'image': '', 'category_id': 1, 'season': 'spring', 'seasonal_discount_percent': 20},
    {'id': 3, 'sku': 'TOP-003', 'title': 'Linen Shirt', 'description': 'Breathable linen shirt', 'price': 399, 'image': '', 'category_id': 1, 'season': 'summer'},
    {'id': 4, 'sku': 'TOP-004', 'title': 'Knit Sweater', 'description': 'Cozy knit sweater', 'price': 499, 'image': '', 'category_id': 1, 'season': 'autumn'},
    {'id': 5, 'sku': 'TOP-005', 'title': 'Turtleneck', 'description': 'Warm turtleneck jumper', 'price': 559, 'image': '', 'category_id': 1, 'season': 'winter'},

    {'id': 6, 'sku': 'BOT-001', 'title': 'Slim Jeans', 'description': 'Comfort stretch denim', 'price': 599, 'image': '', 'category_id': 2, 'season': 'all'},
    {'id': 7, 'sku': 'BOT-002', 'title': 'Chino Pants', 'description': 'Smart casual chinos', 'price': 449, 'image': '', 'category_id': 2, 'season': 'spring', 'seasonal_discount_percent': 15},
    {'id': 8, 'sku': 'BOT-003', 'title': 'Shorts', 'description': 'Summer cotton shorts', 'price': 299, 'image': '', 'category_id': 2, 'season': 'summer'},
    {'id': 9, 'sku': 'BOT-004', 'title': 'Corduroy Trousers', 'description': 'Soft corduroy trousers', 'price': 499, 'image': '', 'category_id': 2, 'season': 'autumn'},
    {'id': 10, 'sku': 'BOT-005', 'title': 'Wool Trousers', 'description': 'Warm wool trousers', 'price': 649, 'image': '', 'category_id': 2, 'season': 'winter'},

    {'id': 11, 'sku': 'DRS-001', 'title': 'Floral Midi Dress', 'description': 'Light floral pattern dress', 'price': 699, 'image': '', 'category_id': 3, 'season': 'spring', 'seasonal_discount_percent': 15},
    {'id': 12, 'sku': 'DRS-002', 'title': 'Sundress', 'description': 'Casual summer sundress', 'price': 599, 'image': '', 'category_id': 3, 'season': 'summer'},
    {'id': 13, 'sku': 'DRS-003', 'title': 'Wrap Dress', 'description': 'Versatile wrap dress', 'price': 799, 'image': '', 'category_id': 3, 'season': 'all'},
    {'id': 14, 'sku': 'DRS-004', 'title': 'Velvet Dress', 'description': 'Elegant velvet dress', 'price': 899, 'image': '', 'category_id': 3, 'season': 'winter'},
    {'id': 15, 'sku': 'DRS-005', 'title': 'Knit Dress', 'description': 'Warm knit dress for cooler days', 'price': 749, 'image': '', 'category_id': 3, 'season': 'autumn'},

    {'id': 16, 'sku': 'OUT-001', 'title': 'Denim Jacket', 'description': 'Classic denim jacket', 'price': 699, 'image': '', 'category_id': 4, 'season': 'spring', 'seasonal_discount_percent': 20},
    {'id': 17, 'sku': 'OUT-002', 'title': 'Trench Coat', 'description': 'Timeless trench coat', 'price': 1299, 'image': '', 'category_id': 4, 'season': 'autumn'},
    {'id': 18, 'sku': 'OUT-003', 'title': 'Puffer Jacket', 'description': 'Insulated puffer for cold weather', 'price': 1499, 'image': '', 'category_id': 4, 'season': 'winter'},
    {'id': 19, 'sku': 'OUT-004', 'title': 'Light Windbreaker', 'description': 'Windproof light jacket', 'price': 499, 'image': '', 'category_id': 4, 'season': 'summer'},
    {'id': 20, 'sku': 'OUT-005', 'title': 'Cardigan', 'description': 'Soft cardigan for layering', 'price': 399, 'image': '', 'category_id': 4, 'season': 'all'},

    {'id': 21, 'sku': 'ACC-001', 'title': 'Canvas Tote', 'description': 'Everyday canvas tote bag', 'price': 199, 'image': '', 'category_id': 5, 'season': 'all'},
    {'id': 22, 'sku': 'ACC-002', 'title': 'Straw Hat', 'description': 'Perfect for beach days', 'price': 149, 'image': '', 'category_id': 5, 'season': 'summer'},
    {'id': 23, 'sku': 'ACC-003', 'title': 'Wool Scarf', 'description': 'Cozy scarf for winter', 'price': 249, 'image': '', 'category_id': 5, 'season': 'winter'},
    {'id': 24, 'sku': 'ACC-004', 'title': 'Silk Bandana', 'description': 'Stylish accessory', 'price': 99, 'image': '', 'category_id': 5, 'season': 'spring', 'seasonal_discount_percent': 10},
    {'id': 25, 'sku': 'ACC-005', 'title': 'Sunglasses', 'description': 'UV protection sunglasses', 'price': 299, 'image': '', 'category_id': 5, 'season': 'summer'},

    {'id': 26, 'sku': 'SHO-001', 'title': 'White Sneakers', 'description': 'Everyday casual sneakers', 'price': 799, 'image': '', 'category_id': 6, 'season': 'all'},
    {'id': 27, 'sku': 'SHO-002', 'title': 'Loafers', 'description': 'Smart leather loafers', 'price': 999, 'image': '', 'category_id': 6, 'season': 'autumn'},
    {'id': 28, 'sku': 'SHO-003', 'title': 'Sandals', 'description': 'Comfortable summer sandals', 'price': 349, 'image': '', 'category_id': 6, 'season': 'summer'},
    {'id': 29, 'sku': 'SHO-004', 'title': 'Ankle Boots', 'description': 'Stylish boots for fall', 'price': 1199, 'image': '', 'category_id': 6, 'season': 'autumn'},
    {'id': 30, 'sku': 'SHO-005', 'title': 'Snow Boots', 'description': 'Durable winter boots', 'price': 1399, 'image': '', 'category_id': 6, 'season': 'winter'},
]
