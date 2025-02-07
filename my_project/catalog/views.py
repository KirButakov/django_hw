from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseForbidden
from django.urls import reverse
from django.core.cache import cache
from django.utils.cache import get_cache_key
from django.views.decorators.cache import cache_page
from .models import Product, Category
from .forms import ProductForm
from .services import get_products_by_category

class HomeView(TemplateView):
    template_name = 'catalog/home.html'

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

def category_products_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = get_products_by_category(category_id)
    return render(request, "catalog/category_products.html", {"category": category, "products": products})

def invalidate_view_cache(path):
    request = HttpRequest()
    request.method = 'GET'
    request.path = path
    key = get_cache_key(request)
    if key:
        cache.delete(key)

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            invalidate_view_cache(reverse('product_list'))
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
            invalidate_view_cache(reverse('product_detail', kwargs={'pk': pk}))
            invalidate_view_cache(reverse('product_list'))
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
        invalidate_view_cache(reverse('product_detail', kwargs={'pk': pk}))
        invalidate_view_cache(reverse('product_list'))
        return redirect('product_list')
    return render(request, 'catalog/product_confirm_delete.html', {'product': product})
