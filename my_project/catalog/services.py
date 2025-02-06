from django.core.cache import cache
from .models import Product

def get_products_by_category(category_id):
    """
    Получает список продуктов указанной категории.
    Использует кеширование для оптимизации запросов.
    """
    cache_key = f"products_category_{category_id}"
    products = cache.get(cache_key)

    if not products:
        products = list(Product.objects.filter(category_id=category_id, status=Product.PUBLISHED))
        cache.set(cache_key, products, timeout=60 * 10)  # Кеш на 10 минут

    return products
