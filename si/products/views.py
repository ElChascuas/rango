from django.shortcuts import render, redirect
from products.models import Product
from products.forms import FormularioProducts
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def create_product(request):
    """Esta vista retorna el personaje creado, 
    ademas requiere estar logueado para acceder, de lo contrario te envia al registro."""
    if request.method == 'POST':
        form= FormularioProducts(request.POST, request.FILES)

        if form.is_valid():
            Product.objects.create(
                name = form.cleaned_data['name'],
                category = form.cleaned_data['category'],
                description = form.cleaned_data['description'],
                price = form.cleaned_data['price'],
                stock = form.cleaned_data['stock'],
                image= form.cleaned_data["image"])     
            return redirect(list)

    elif request.method == 'GET':
        form = FormularioProducts
        context = {'form':form}
        return render(request, "products/create_product.html", context=context)
   

@login_required
def list(request):
    """Esta vista retorna todos los personajes de la base de datos y los muestra, 
    ademas requiere estar logueado, sino te manda al registro"""
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "products/list.html", context=context)


@login_required
def search_products(request):
   search = request.GET['search']
   products = Product.objects.filter(name__icontains=search)
   context={'products':products}
   return render(request, 'products/search_products.html', context=context)


class DetailProduct(DetailView):
    model = Product
    template_name = 'products/detail_product.html'


@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, id):
    """Esta vista retorna un delete del producto que seleccionaste, 
    ademas requiere estar logueado y ser admin para acceder, sino te manda al registro"""
    if request.method == 'GET':
        products = Product.objects.get(id=id)
        context = {'products':products}
        return render(request, 'products/delete_product.html',context=context)
    elif request.method == 'POST':
        products = Product.objects.get(id=id)
        products.delete()
        return redirect(list)


@user_passes_test(lambda u: u.is_superuser)
def update_product(request, id):
    """Esta vista retorna un update del personaje que seleccionaste, 
    ademas requiere estar logueado y ser admin para acceder, sino te manda al registro"""
    if request.method == 'POST':
        form = FormularioProducts(request.POST)
        if form.is_valid():
            products = Product.objects.get(id=id)
            products.name = form.cleaned_data['name']
            products.category = form.cleaned_data['category']
            products.description = form.cleaned_data['description']
            products.price = form.cleaned_data['price']
            products.stock = form.cleaned_data['stock']
            products.save()
            return redirect(list)


    elif request.method == 'GET':
        products = Product.objects.get(id=id)
        form = FormularioProducts(initial={
                                    'name':products.name,
                                    'category':products.category,
                                    'price':products.price, 
                                    'description':products.description,
                                    'stock':products.stock})
        context = {'form':form}
        return render(request, 'products/update_product.html', context=context)