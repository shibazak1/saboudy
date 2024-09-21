from django.shortcuts import render, redirect
from django.http import HttpResponse ,JsonResponse
from django.utils.html import escape , urlencode
from django.views import View
from .models import Book
from django.middleware.csrf import get_token
from django.urls import reverse
from test.forms import BookForm ,crispy
# Create your views here.

def index(request):

    return render(request,'test/index.html')
    
def index2(request):
    return HttpResponse("this is index2")

def index3(request):
    quess  = request.GET['quess']
    message  = """<h1>you guess is """+escape(quess)+"""</h1>"""
    return HttpResponse(message)

def index4(request,m):
    return HttpResponse(f"""<p>your m is {m}</p>""")

def books_list(request):

    books = Book.objects.all()
    ctx = {"books":books}
    return render(request,"test/books.html",ctx)

class books_detail(View):
    def get(self,request,pk):
        book = Book.objects.get(pk=pk)
        ctx = {"book":book}
        return render(request,"test/book_detail.html",ctx)


def dump_data(method,data):

    result = """<p>Incomping data</p><br/>"""
    for key,value in data.items():
        result +=key+"="+value+"<br/>"
    return result

    
def form(request):
    response = """<form method="Get"><label for="number">Number<label/>
    <input type="text" name="guess" id="number"><br/>
     <input type="submit" value="submit">
    </form>"""

    response += dump_data("get",request.GET)
    return HttpResponse(response)


def postform(request):

    response = """<form method="Post"><label for="number">Number<label/>
    <input type="text" name="guess" id="number"><br/>
    <input type="hidden" name="csrfmiddlewaretoken" value="__token__">
     <input type="submit" value="submit">
    </form>"""

    token = get_token(request)
    response = response.replace("__token__",token)
    response += dump_data("POST",request.POST)

    return HttpResponse(response)

class getpostform(View):

    def get(self ,request):

        return render(request,"test/form.html")

    def post(self,request):

        guess = request.POST.get("guess")
        ctx = {"guess":guess}

        return render(request,"test/form.html",ctx)
    

class add_book(View):

    def get(self ,request):

        return render(request,"test/addbook.html")

    def post(self,request):

        name = request.POST.get("name")
        author = request.POST.get("auther")
        publisher = request.POST.get("puplisher")
        genre = request.POST.get("type")

        b = Book(name=name, auther=author, puplisher=publisher, genre=genre)
        b.save()


        
        return redirect(request.path)
        
#---------------------------------------------------------------
# test about cookies

def cookies(request):
    print(request.COOKIES)
    ctx = {"cookies":request.COOKIES}
    
    return render(request,"test/cookies.html",ctx)

def get_cookies(request):
    print(request.COOKIES)

    oldval = request.COOKIES.get("vii",None)

    resp = HttpResponse("<p>your cookies is : </p>"+str(oldval))

    if oldval:
        resp.set_cookie("vii",int(oldval)+1)
        
    else:
        resp.set_cookie("vii",24)
        

    return resp

def session(request):

    x = request.session.get("x",0)+1
    request.session["x"] = x
    if x>4:
        del(request.session["x"])
    return HttpResponse("view count = "+str(x))
#----------------------------------------------------------------------------------------------------

# test login logout functions

class yourdata(View):

    def get(self,request):
        if request.user.is_authenticated:
            name = request.user.username
            email= request.user.email
            #logouturl = reverse("logout")+"?"+urlencode({"next":"test/yourlogout.html"})
            ctx = {"name":name,"email":email}
            return render(request,"test/yourdata.html",ctx)
        loginurl= reverse("login")+"?"+urlencode({"next":request.path})
        return redirect(loginurl)


def yourlogout(request):
    return render(request,"test/yourlogout.html",{})


#------------------------------------------------------------------------------------------------
#test forms

def dumpform(request):
    form = BookForm()
    return HttpResponse(form.as_table())


class CreateBook(View):
    def get(self ,request):
        form = BookForm()
        ctx = {"form":form}
        return render(request,"test/createbook.html",ctx)



#-------------------------------------------------------------------------------------------
#testing crispy forms

class crispyforms(View):

    template = None
    def get(self,request):
        form = crispy()
        ctx = {"form":form}
        return render(request,self.template,ctx)

    def post(self,request):
        form = crispy(request.POST)
        if not form.is_valid():
            ctx = {"form":form}
            return render(request,self.template,ctx)
        #save the form
        return redirect(reverse("success"))
        
        
def success(request):

    return HttpResponse("YOUR CAR HASE BEEN REGESTERED")


#-----------------------------------------------------------------------------------

def fetch(request):
    return render(request,"test/promis.html")


def json(request):

    person = {

        "name":"ahmed",
        "age":"24",
        "skills":["c","python","javascript"],

    }


    return JsonResponse(person)

