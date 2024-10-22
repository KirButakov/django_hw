from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('contacts/', views.contacts, name='contacts'),  # Страница контактов
    path('products/', views.product_list, name='product_list'), # Страница со всеми продуктами
    path('products/<int:pk>/', views.product_detail, name='product_detail'),  # Страница с деталями конкретного продукта
]
