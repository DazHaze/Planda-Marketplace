from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<product_id>', views.product_detail, name='product_detail'),
    path('sale/sale_products', views.sale_products, name='sale_products'),
    path('/favourites/<favourite_id>', views.favourite_add, name='favourite_add'),
]