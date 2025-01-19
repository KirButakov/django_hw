from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category_name')
    list_filter = ('category__name',)  # Фильтрация по имени категории
    search_fields = ('name', 'description')

    # Метод для отображения имени категории
    def category_name(self, obj):
        return obj.category.name
    category_name.admin_order_field = 'category'  # Сортировка по полю категории
    category_name.short_description = 'Category'  # Название колонки в админке
