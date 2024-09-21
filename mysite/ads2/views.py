from django.shortcuts import render,redirect ,get_object_or_404, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from .models import Ad2 , Comment
from .forms import AdForm , CommentForm

from article.owner import OwnerListView, OwnerDetailView,OwnerCreateView, OwnerUpdateView,OwnerDeleteView
# Create your views here.


def main(request):
    template_name = "ads2/main.html"
    return render(request,template_name)


class AdListView(OwnerListView,View):
    model = Ad2
    template_name = "ads2/list.html"


class AdDetailView(View):
    template_name = "ads2/detial.html"

    def get(self,request,pk):
        ad_object = get_object_or_404(Ad2,id=pk)
        ad_comments = Comment.objects.filter(ad = ad_object).order_by("-updated_at")

        comment_form = CommentForm()

        ctx = {"ad2":ad_object,"comments":ad_comments,"comment_form":comment_form}

        return render(request,self.template_name,ctx)

    


class AdCreateView(LoginRequiredMixin,View):

    template_name = "ads2/ad_form.html"
    def get(self ,request):

        form = AdForm()
        ctx = {"form":form}
        return render(request,self.template_name,ctx)

    def post(self,request):

        form = AdForm(request.POST,request.FILES or None)

        if not form.is_valid():
            return render(request,self.template_name,form)
        ad2 = form.save(commit=False)
        ad2.owner = self.request.user
        ad2.save()
        return redirect(reverse_lazy("all"))



class AdUpdateView(LoginRequiredMixin,View):

    template_name = "ads2/ad_form.html"
    def get(self,request,pk):

        ad_object = get_object_or_404(Ad2,id=pk)
        form = AdForm(instance=ad_object)
        ctx = {"form":form}

        return render(request,self.template_name,ctx)

    def post(self,request,pk):
        ad_object = get_object_or_404(Ad2,id=pk,owner=self.request.user)
        form = AdForm(request.POST,request.FILES or None,instance=ad_object)
        ctx = {"form":form}

        if not form.is_valid():
            return render(request,self.template_name)

        form.save()
        return redirect(reverse_lazy("all"))



class AdDeleteView(OwnerDeleteView,LoginRequiredMixin):
    model = Ad2
    template_name = "ads2/delete.html"
    success_url = reverse_lazy("all")




def stream_file(request,pk):

    ad2  = get_object_or_404(Ad2,id=pk)
    response = HttpResponse()
    response["content-type"] = ad2.content_type
    response["content-length"] = len(ad2.picture)
    response.write(ad2.picture)
    return response



class CommentCreateView(LoginRequiredMixin,View):

    def post(self,request,pk):

        ad_object = get_object_or_404(Ad2,id=pk)

        comments = Comment(text=request.POST['text'],owner=request.user,ad=ad_object)
        comments.save()
        
        return redirect(reverse("ad_detail",args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads2/comment_delete.html"

    def get_success_url(self):

        ad = self.object.ad

        return reverse("ad_detail",args=[ad.id])
    
