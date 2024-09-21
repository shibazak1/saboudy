from django.urls import path ,include
from django.contrib import admin
from . import views


urlpatterns = [

    path("",views.main,name="main"),
    path("ads2/list",views.AdListView.as_view(),name="all"),
    path("ads2/detail/<int:pk>",views.AdDetailView.as_view(),name="ad_detail"),
    path ("ads2/create",views.AdCreateView.as_view(),name="ad_create"),
    path("ads2/update/<int:pk>",views.AdUpdateView.as_view(),name="ad_update"),
    path("ads2/delete<int:pk>",views.AdDeleteView.as_view(),name="ad_delete"),
    path("ads2/pic/<int:pk>",views.stream_file,name="ad_pic"),
    #comment stuff
    path("ads2/comment/create/<int:pk>",views.CommentCreateView.as_view(),name="comment_create"),
    path("ads2/delete/<int:pk>",views.CommentDeleteView.as_view(),name="comment_delete"),
    
]
