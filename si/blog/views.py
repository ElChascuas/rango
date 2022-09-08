from re import A
from django.shortcuts import render, redirect
from blog.models import Article
from blog.forms import FormularioBlog
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import DetailView


@user_passes_test(lambda u: u.is_superuser)
def create_article(request):
    """Esta vista retorna el articulo creado, 
    ademas requiere estar logueado y ser admin para acceder, de lo contrario te envia al registro."""
    if request.method == 'POST':
        form= FormularioBlog(request.POST, request.FILES)

        if form.is_valid():
            Article.objects.create(
                title = form.cleaned_data['title'],
                body = form.cleaned_data['body'],
                date = form.cleaned_data["date"],
                author = form.cleaned_data['author'],
                image= form.cleaned_data["image"])     
            return redirect(articles)
    
    elif request.method == 'GET':
        form = FormularioBlog()
        context = {'form':form}
        return render(request, "articles/create_article.html", context=context)


@login_required
def search_articles(request):
   search = request.GET['search']
   articles = Article.objects.filter(title__icontains=search)
   context={'articles':articles}
   return render(request, 'articles/search_articles.html', context=context)


class DetailArticle(DetailView):
    model = Article
    template_name = 'articles/detail_article.html'


@login_required
def articles(request):
    """Esta vista retorna todos los articulos de la base de datos y los muestra, 
    ademas requiere estar logueado, de lo contrario te manda al registro"""
    articles= Article.objects.all()
    context = {"articles": articles}
    return render(request, "articles/articles.html", context=context)


@user_passes_test(lambda u: u.is_superuser)
def delete_article(request, id):
    """Esta vista retorna un delete del articulo que seleccionaste, 
    ademas requiere estar logueado y ser admin para acceder, sino te manda al registro"""
    if request.method == 'GET':
        article = Article.objects.get(id=id)
        context = {'article':article}
        return render(request, 'articles/delete_article.html',context=context)
    elif request.method == 'POST':
        article = Article.objects.get(id=id)
        article.delete()
        return redirect(articles)


@user_passes_test(lambda u: u.is_superuser)
def update_article(request, id):
    """Esta vista retorna un update del articulo que seleccionaste, 
    ademas requiere estar logueado y ser admin para acceder, sino te manda al registro"""
    if request.method == 'POST':
        form = FormularioBlog(request.POST)
        if form.is_valid():
            article =  Article.objects.get(id=id)
            article.title = form.cleaned_data['title']
            article.body = form.cleaned_data['body']
            article.author = form.cleaned_data['author']
            article.image = form.cleaned_data["image"]
            article.save()
            return redirect(articles)


    elif request.method == 'GET':
        article = Article.objects.get(id=id)
        form = FormularioBlog(initial={
                                    'title':article.title,
                                    'body':article.body,
                                    'author':article.author})
        context = {'form':form}
        return render(request, 'articles/update_article.html', context=context)
