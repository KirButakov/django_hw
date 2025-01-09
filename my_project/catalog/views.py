from django.views.generic import TemplateView, ListView, DetailView
from .models import Product
from django.shortcuts import render, redirect
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

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Перенаправление на страницу со списком продуктов
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})

def product_update(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})

def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')  # Перенаправление на страницу со списком продуктов
    return render(request, 'catalog/product_confirm_delete.html', {'product': product})
