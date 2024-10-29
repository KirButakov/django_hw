from django.urls import path, include
from .views import HomeView, ContactsView, ProductListView, ProductDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Главная страница
    path('contacts/', ContactsView.as_view(), name='contacts'),  # Страница контактов
    path('products/', ProductListView.as_view(), name='product_list'),  # Страница со всеми продуктами
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Страница с деталями конкретного продукта
    path('blogs/', include('blog.urls')),  # Подключение маршрутов блога
]
