from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    return render(request, 'catalog/home.html')

def contacts(request):
    return render(request, 'catalog/contacts.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})
