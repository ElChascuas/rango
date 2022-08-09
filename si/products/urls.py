from django.urls import path
from products.views import create_product, list


urlpatterns = [
    path("list/", list, name= "list"),
    path('create_product/', create_product, name= 'create_product')
]
