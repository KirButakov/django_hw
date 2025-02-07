from django.core.management.base import BaseCommand

from catalog.models.product import Product

from catalog.models.category import Category

class Command(BaseCommand):
    help = 'Add test products to the database'

    def handle(self, *args, **kwargs):
        # Удаление всех существующих продуктов и категорий
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создание категорий
        electronics = Category.objects.create(name='Electronics', description='Electronic devices')
        clothing = Category.objects.create(name='Clothing', description='Apparel and accessories')

        # Создание продуктов
        Product.objects.create(name='Smartphone', description='Latest model smartphone', price=699.99, category=electronics)
        Product.objects.create(name='T-Shirt', description='Cotton t-shirt', price=19.99, category=clothing)

        self.stdout.write(self.style.SUCCESS('Successfully added test products!'))
