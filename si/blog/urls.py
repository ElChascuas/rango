from django.urls import path
from blog.views import create_article, articles, delete_article, update_article, search_articles, DetailArticle


urlpatterns = [
    path("articles/", articles, name= "articles"),
    path('create_article/', create_article, name= 'create_article'),
    path('search_articles/', search_articles, name='search_articles'),
    path('delete_article/<int:id>/', delete_article, name='delete_article'),
    path('update_article/<int:id>/', update_article, name='update_article'),
    path('detail_article/<int:pk>/', DetailArticle.as_view(), name='DetailArticle')]
