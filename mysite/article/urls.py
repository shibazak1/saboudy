from django.contrib import admin
from django.urls import include, path, reverse_lazy
from . import views


urlpatterns = [

    path("", views.ArticleList.as_view(),name="all"),
    path("article_detail/<int:pk>",views.ArticleDetail.as_view(),name="article_detail"),
    path("article_update/<int:pk>",views.ArticleUpdate.as_view(),name="article_update"),
    path("article_delete/<int:pk>",views.ArticleDelete.as_view(),name="article_delete"),
    path("article_create",views.ArticleCreate.as_view(),name="article_create"),



    

]
