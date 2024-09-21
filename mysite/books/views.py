from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book ,Author
from .forms import AuthorForm
# Create your views here.

def books_list(request):
    books = Book.objects.all()
    ctx = {"books":books}

    return render(request,"books/books.html",ctx)

class AuthorView(View):
    
    def get(self ,request):
        authors = Author.objects.all()
        ctx = {"authors":authors}

        return render(request,"books/authors_list.html",ctx)
        



class AddAuthor(View):
    
    def get(self,request):

        form = AuthorForm()
        ctx  = {"form":form}
        return render(request,"books/addauthor.html",ctx)

    def post(self,request):

        form = AuthorForm(request.POST)
        if not form.is_valid():
            ctx = {"form":form}
            return render(request,"books/addauthor.html",ctx)
        
        form.save()
        return redirect(reverse_lazy("books_list"))


class AuthorUpdate(View):

    def get(self,request,pk):

        author_data = get_object_or_404(Author ,pk=pk)
        form = AuthorForm(instance = author_data)

        ctx = {"form":form}
        return render(request,"books/addauthor.html",ctx)

    def post(self,request,pk):

        author_data = get_object_or_404(Author,pk=pk)
        form = AuthorForm(request.POST,instance =author_data)

        if not form.is_valid():
            ctx = {"form":form}
            return render(request,"books/addauthor.html",ctx)
        form.save()
        return redirect(reverse_lazy("books_list"))



class AuthorDelete(View):

    def get(self,request,pk):

        author_data = get_object_or_404(Author,pk=pk)
        form = AuthorForm(instance=author_data)
        ctx = {"form":form}

        return render(request,"books/delete.html",ctx)

    def post(self,request,pk):

        Author.objects.filter(pk=pk).delete()
        return redirect(reverse_lazy("books_list"))
        

        
class BookAdd(CreateView):
    model = Book
    fields  = '__all__'
    success_url = reverse_lazy('books_list')


class BookUpdate(UpdateView):

    model = Book
    fields = "__all__"
    success_url = reverse_lazy('books_list')
        
        

class BookDelelte(DeleteView):

    model = Book
    fields = "__all__"
    success_url = reverse_lazy('books_list')
