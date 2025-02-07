from django.test import TestCase
from .models import Product
from .forms import ProductForm

class ProductFormTest(TestCase):
    def test_form_validation_forbidden_words_in_name(self):
        form_data = {'name': 'Криптовалюта', 'description': 'Описание продукта', 'price': 100, 'available': True}
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ['Название не может содержать слово: криптовалюта'])

    def test_form_validation_forbidden_words_in_description(self):
        form_data = {'name': 'Product Name', 'description': 'Описание с криптовалютой', 'price': 100, 'available': True}
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['description'], ['Описание не может содержать слово: криптовалюта'])

    def test_form_validation_negative_price(self):
        form_data = {'name': 'Product Name', 'description': 'Описание продукта', 'price': -100, 'available': True}
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['price'], ['Цена не может быть отрицательной.'])
