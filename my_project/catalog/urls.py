from django.urls import path, include
from .views import HomeView, ContactsView, ProductListView, ProductDetailView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Главная страница
    path('contacts/', ContactsView.as_view(), name='contacts'),  # Страница контактов
    path('products/', ProductListView.as_view(), name='product_list'),  # Страница со всеми продуктами
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Страница с деталями конкретного продукта
    path('product/create/', views.product_create, name='product_create'),  # Создание продукта
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),  # Редактирование продукта
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),  # Удаление продукта
    path('blogs/', include('blog.urls')),  # Подключение маршрутов блога
]