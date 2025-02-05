from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
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
            product = form.save(commit=False)
            product.owner = request.user  # Присваиваем владельца
            product.save()
            return redirect('product_list')  # Перенаправление на страницу со списком продуктов
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})

# Декорируем функцию product_update для проверки авторизации и прав владельца
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Проверка на то, что только владелец или модератор может редактировать продукт
    if request.user != product.owner and not request.user.groups.filter(name='Модераторы').exists():
        return HttpResponseForbidden('У вас нет прав для редактирования этого продукта.')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})

# Декорируем функцию product_delete для проверки авторизации и прав владельца
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Проверка на то, что только владелец или модератор может удалить продукт
    if request.user != product.owner and not request.user.groups.filter(name='Модераторы').exists():
        return HttpResponseForbidden('У вас нет прав для удаления этого продукта.')

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')  # Перенаправление на страницу со списком продуктов
    return render(request, 'catalog/product_confirm_delete.html', {'product': product})
