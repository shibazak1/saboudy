from django.shortcuts import render,HttpResponse , redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Message


# Create your views here.



class MainTalk(LoginRequiredMixin,View):

    def get(self,request):

        return render(request,"chat/talk.html")

    def post(self,request):

        message = Message(text = request.POST['message'], owner = request.user)
        message.save()

        return redirect(reverse_lazy("talk"))



class Messages(LoginRequiredMixin,View):

    def get(self,request):

        messages = Message.objects.all().order_by('-created_at')[:10]

        result =[]
        for message in messages:
            result.append([message.text,naturaltime(message.created_at)])

        return JsonResponse(result,safe= False)

    
            
