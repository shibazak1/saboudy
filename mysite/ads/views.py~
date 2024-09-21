from django.shortcuts import render , redirect , get_object_or_404, HttpResponse
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from article.models import Article
from ads.models import Ad
from ads.forms import AdForm
from article.owner import OwnerListView, OwnerDetailView,OwnerCreateView, OwnerUpdateView,OwnerDeleteView

# Create your views here.


class AdListView(OwnerListView):
    model = Ad
    template_name = "ads/list.html"



class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ads/detial.html"


class AdCreateView(LoginRequiredMixin, View):

    template_name = "ads/ad_form.html"
    def get(self, request):
        
        form = AdForm()
        ctx = {"form":form}

        return render(request,self.template_name,ctx)

    def post(self,request):

        form = AdForm(request.POST,request.FILES or None)

        if not form.is_valid():

            ctx = {"form":form}
            return render(request,self.template_name,ctx)
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        return redirect(reverse_lazy("all"))


class AdUpdateView(LoginRequiredMixin,View):

    def get(self ,request,pk):
        ad = get_object_or_404(Ad,id=pk)
        form = AdForm(instance=ad)

        ctx = {"form":form}

        return render(request,"ads/ad_form.html",ctx)

    def post(self,request,pk):
        ad = get_object_or_404(Ad,id=pk,owner=self.request.user)
        
        form = AdForm(request.POST,request.FILES or None,instance=ad)
        ctx = {"form":form}
        if not form.is_valid():
            return render(request,"ads/ad_form.html",ctx)
        ad_object = form.save(commit=False)
        ad_object.save()

        return redirect(reverse_lazy("all"))


class AdDeleteView(LoginRequiredMixin,View):

    def get(self,request,pk):

        ad = get_object_or_404(Ad,owner=self.request.user,id=pk)
        return render(request,"ads/delete.html")
    
    def post(self, request,pk):
        Ad.objects.filter(pk=pk).delete()
        return redirect(reverse_lazy("all"))
        
        
        
        

    
        
        

def stream_file(request,pk):
    ad = get_object_or_404(Ad,id=pk)
    response = HttpResponse()
    response["content-type"] = ad.content_type
    response["content-length"] = len(ad.picture)
    response.write(ad.picture)
    return response

