from django.shortcuts import render
from django.http import HttpResponse

from . import models


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.

def products(request):

    ctx = {'prd': models.Product.objects.all()}

    return render(request,'polls/products.html',ctx)

    
