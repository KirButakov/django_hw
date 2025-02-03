from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Product
from .forms import ProductForm

class HomeView(TemplateView):
    template_name = 'catalog/home.html'

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

# Декорируем функцию product_create для проверки авторизации
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Перенаправление на страницу со списком продуктов
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})

# Декорируем функцию product_update для проверки авторизации
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})

# Декорируем функцию product_delete для проверки авторизации
@login_required
def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404("Продукт не найден")

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')  # Перенаправление на страницу со списком продуктов
    return render(request, 'catalog/product_confirm_delete.html', {'product': product})
