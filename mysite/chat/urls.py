
from django.urls import path, include
from  . import views



urlpatterns = [

    path("",views.MainTalk.as_view(),name="talk"),
    path("messages",views.Messages.as_view(),name="messages"),
    
]
