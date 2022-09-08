from django.urls import path
from products.views import create_product, list, search_products, delete_product, update_product, DetailProduct


urlpatterns = [
    path("list/", list, name= "list"),
    path('create_product/', create_product, name= 'create_product'),
    path('search_products/', search_products, name='search_products'), 
    path('delete_product/<int:id>/', delete_product, name='delete_product'),
    path('update_product/<int:id>/', update_product, name='update_product'),
    path('detail_product/<int:pk>/', DetailProduct.as_view(), name='DetailProduct')]
