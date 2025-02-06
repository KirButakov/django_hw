from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import Product, Category
from .forms import ProductForm
from .services import get_products_by_category

class HomeView(TemplateView):
    template_name = 'catalog/home.html'

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        cache_key = "product_list"
        products = cache.get(cache_key)
        if not products:
            products = Product.objects.all()
            cache.set(cache_key, products, timeout=60 * 5)  # Кеш на 5 минут
        return products

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        product_id = self.kwargs.get("pk")
        cache_key = f"product_{product_id}"
        product = cache.get(cache_key)

        if not product:
            product = super().get_object(queryset)
            cache.set(cache_key, product, timeout=60 * 5)  # Кеш на 5 минут

        return product

def category_products_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = get_products_by_category(category_id)
    return render(request, "catalog/category_products.html", {"category": category, "products": products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            cache.delete("product_list")  # Очистка кеша списка
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user != product.owner and not request.user.groups.filter(name='Модераторы').exists():
        return HttpResponseForbidden('У вас нет прав для редактирования этого продукта.')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            cache.delete(f"product_{pk}")  # Очистка кеша при обновлении
            cache.delete("product_list")  # Очистка кеша списка
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user != product.owner and not request.user.groups.filter(name='Модераторы').exists():
        return HttpResponseForbidden('У вас нет прав для удаления этого продукта.')

    if request.method == 'POST':
        product.delete()
        cache.delete(f"product_{pk}")  # Очистка кеша при удалении
        cache.delete("product_list")  # Очистка кеша списка
        return redirect('product_list')
    return render(request, 'catalog/product_confirm_delete.html', {'product': product})
