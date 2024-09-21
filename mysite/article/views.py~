from django.shortcuts import render
from django.urls import reverse_lazy
from article.models import Article
from article.owner import OwnerListView, OwnerDetailView,OwnerCreateView, OwnerUpdateView,OwnerDeleteView

# Create your views here.

class ArticleList(OwnerListView):
    model = Article
    



class ArticleDetail(OwnerDetailView):
    model = Article
    success_url=reverse_lazy("all")


class ArticleCreate(OwnerCreateView):
    model = Article
    fields = ["title","text"]
    success_url = reverse_lazy("all")



class ArticleUpdate(OwnerUpdateView):
    model = Article
    fields = ["title","text"]
    success_url = reverse_lazy("all")

class ArticleDelete(OwnerDeleteView):
    model = Article
    success_url = reverse_lazy("all")
