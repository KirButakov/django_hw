from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category_name', 'status', 'owner')
    list_filter = ('category__name', 'status')  # Фильтрация по статусу и категории
    search_fields = ('name', 'description')

    def category_name(self, obj):
        return obj.category.name
    category_name.admin_order_field = 'category'
    category_name.short_description = 'Category'