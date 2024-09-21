from django.urls import path,include , reverse_lazy
from django.contrib import admin
from . import views



urlpatterns = [

    path("ads_list",views.AdListView.as_view(),name="all"),
    path("ad/<int:pk>",views.AdDetailView.as_view(),name="ad_detail"),
    path("ad/create",views.AdCreateView.as_view(),name="ad_create"),
    path("ad/updata/<int:pk>",views.AdUpdateView.as_view(),name="ad_update"),
    path("ad/delete/<int:pk>",views.AdDeleteView.as_view(),name="ad_delete"),
    path("ad_pic/<int:pk>",views.stream_file,name="ad_pic"),



]

