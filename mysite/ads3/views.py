
from django.shortcuts import render,redirect ,get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q # Q() object that take key word args (lookup field ) that represent a condition used in a query to sql 
from django.views import View
from .models import Ad3 , Coment , Favourite, Ad_Tage,Tage, Cart, CartItem, Order, OrderItem,Driver ,DriverOrder,MyUser,ProductVaraint,Color,Size
from .forms import AdForm , CommentForm, CustomUserCreationForm

from django.views.generic import ListView
from article.owner import OwnerListView, OwnerDetailView,OwnerCreateView, OwnerUpdateView,OwnerDeleteView
from django.db import transaction

from geopy.distance import geodesic
import json
# Create your views here.
from django.contrib.auth import authenticate, login

# yourapp/views.py
from django.contrib.auth.views import LoginView
from urllib.parse import urlencode
from django.utils.http import url_has_allowed_host_and_scheme

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
class SignIn(View):

    def get(self,request):

        form = CustomUserCreationForm()
        print(f"form is {form}")
        return render(request,"ads3/signin.html",{"form":form})

    def post(self,request):

        form = CustomUserCreationForm(request.POST)

        if not form.is_valid():
            return render(request,"ads3/signin.html",{"form":form})

        
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        mail_subject = "activate Your saboudy account."
        message = render_to_string("ads3/acc_active_email.html",
                                   {"user":user,
                                    "domain":current_site.domain,
                                    "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                                    'token':account_activation_token.make_token(user),})
        

        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject,message,to=[to_email])
        email.send()

        return HttpResponse('Please confirm your email address to complete the registration')
    
    #    username = form.cleaned_data.get('username')
     #   password = form.cleaned_data.get('password1')
      #  user = authenticate(username=username,password=password)
       # login(request,user)
        #return redirect(reverse("redirection"))



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


    




class IsSuperUser(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser
    def handle_no_permission(self):
        return redirect(reverse("all"))
        


class IsCustomer(UserPassesTestMixin):
    
    
    def test_func(self):
        #check if the requested user 
        return not isinstance(self.request.user,Driver)
    
    def handle_no_permission(self):

        return redirect(reverse("all_order"))




def redirection(request):

    user  = request.user
    print(f"user is {user}")
    if isinstance(user,Driver):
        return redirect(reverse("all_order"))
    else:
        return redirect(reverse("all"))
        

class CustomLoginView(LoginView):
    print("iam in custom login view")
    
    def get_redirect_url(self):
    
        print("i am in get_")
        
        """Return the user-originating redirect URL if it's safe."""
        # Get the next parameter from POST or GET request
        redirect_to = self.request.POST.get(
            self.redirect_field_name, self.request.GET.get(self.redirect_field_name)
        )
        
        # Check if the next parameter is a safe URL
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )

        # Return the next URL if it's safe; otherwise, handle based on user type
        if url_is_safe:
            return redirect_to
        else:
            # Custom redirection logic based on user type
            user = self.request.user
            if user.is_superuser:
                return reverse_lazy('admin:index')  # Redirect superusers to admin
            elif hasattr(user, 'driver'):  # Assuming Driver is a related model
                return reverse_lazy('all_order')  # Driver view redirection
            else:
                return reverse_lazy('all')  # Customer view redirection

        #super().get_redirect_url(self)



def main(request):
    template_name = "ads3/main.html"
    return render(request,template_name)

"""
class AdListView(OwnerListView,View):
    model = Ad3
    template_name = "ads3/list.html"

    def get(self,request):

        ads = Ad3.objects.all()
        fav_ads = []

        if request.user.is_authenticated:
            
            favourites = Favourite.objects.all()
            
            for favourite in favourites:
                if favourite.owner == request.user:
                    fav_ads.append(favourite.ad)
                    
                    
        ctx = {"adlist":ads,"fav_ads":fav_ads}
        
        return render(request,self.template_name,ctx)
"""

class AdListView(OwnerListView,View):
    model = Ad3
    template_name = "ads3/list.html"

    def get(self,request):

        #divide the get in to 2 part one with search value and other not 
        if request.GET.get("q"):

            # get this GET parameter from the GET dictionary
            search_value = request.GET.get("q")
            # key word arg in filter or other lookup method are and ed together so to use or we need to encapsulate the condition in Q() object
            """
            ad_id_list = []
            at = Ad_Tage.objects.all()
            for obj in at:
                if any(letter in obj.tage.name for letter in list(search_value)):
                    ad_id_list.append(obj.ad.id)
     """               
                
            search_result = Ad3.objects.filter(
                Q(title__contains=search_value)| Q(text__contains=search_value)|Q(tag__name__icontains=search_value)).distinct().order_by("-updated_at")
            ads = search_result

            """
            fav_ads = []
            if request.user.is_authenticated:
                
                favourites = Favourite.objects.all()
            
                for favourite in favourites:
                    if favourite.owner == request.user:
                        
                        fav_ads.append(favourite.ad)
                        ctx = {"adlist":search_result,"fav_ads":fav_ads}
        
        """
            
        
        else:
            #if there is not search value then retrive all the ads 
            ads = Ad3.objects.all()


            
        fav_ads = []
        #make list Favourite ads for the requested user
        if request.user.is_authenticated:
                
            favourites = Favourite.objects.all()
                
            for favourite in favourites:
                if favourite.owner == request.user:
                        
                    fav_ads.append(favourite.ad)

                    
        ctx = {"adlist":ads,"fav_ads":fav_ads}
        return render(request,self.template_name,ctx)


 
class AdDetailView(IsCustomer,View):
    template_name = "ads3/detial.html"

    def get(self,request,pk):
        ad_object = get_object_or_404(Ad3,id=pk)
        colors = ProductVaraint.objects.filter(product=ad_object).values("color__id","color__title","color__color_code").distinct()
        sizes = ProductVaraint.objects.filter(product=ad_object).values("size__id","size__title","price","color__id").distinct()

        #send the all varaint of this product
        product_variant = ProductVaraint.objects.filter(product=ad_object).values("id","image","color__id","size__id","price")

        product_variant = [
            {
                **variant,
                'price': float(variant['price'])  # Convert price to float
            }
            for variant in product_variant
        ]
        
        print(colors)
        ad_comments = Coment.objects.filter(ad = ad_object).order_by("-updated_at")
        
        tags = Ad_Tage.objects.filter(ad=ad_object)

        print(tags)
        comment_form = CommentForm()

        ctx = {
            "ad3":ad_object,
            "comments":ad_comments,
            "tags":tags,
            "comment_form":comment_form,
            "colors":colors,
            "sizes":sizes,
            "product_variant":list(product_variant)}

        return render(request,self.template_name,ctx)

    


class AdCreateView(LoginRequiredMixin,View):

    template_name = "ads3/ad_form.html"
    def get(self ,request):

        form = AdForm()
        ctx = {"form":form}
        return render(request,self.template_name,ctx)

    def post(self,request):

        form = AdForm(request.POST,request.FILES or None)

        if not form.is_valid():
            ctx = {"form":form}
            return render(request,self.template_name,ctx)
        
        ad3 = form.save(commit=False)
        ad3.owner = self.request.user
        
        ad3.save()
        #form.save_m2m()


        tag_list = request.POST.get("tag", "").split(",")

        for tag_name in tag_list:
            tag_name = tag_name.strip()
            if tag_name:  # Avoid empty tags
                tag, created = Tage.objects.get_or_create(name=tag_name)
                print(type(tag))
               # ad3.tage_set.add(tag)  # Add the tag to the ad's many-to-many relationship

                at = Ad_Tage.objects.get_or_create(ad=ad3,tage=tag)
                print(at)
                #at.save()
        
        return redirect(reverse_lazy("all"))



class AdUpdateView(LoginRequiredMixin,View):

    template_name = "ads3/ad_form.html"
    def get(self,request,pk):

        ad_object = get_object_or_404(Ad3,id=pk)
        form = AdForm(instance=ad_object)
        ctx = {"form":form}

        return render(request,self.template_name,ctx)

    def post(self,request,pk):
        ad_object = get_object_or_404(Ad3,id=pk,owner=self.request.user)
        form = AdForm(request.POST,request.FILES or None,instance=ad_object)
        ctx = {"form":form}

        if not form.is_valid():
            return render(request,self.template_name)

        form.save()
        #form.save_m2m()
        return redirect(reverse_lazy("all"))



class AdDeleteView(OwnerDeleteView,LoginRequiredMixin):
    model = Ad3
    template_name = "ads3/delete.html"
    success_url = reverse_lazy("all")




def stream_file(request,pk):

    ad3  = get_object_or_404(Ad3,id=pk)
    response = HttpResponse()
    response["content-type"] = ad3.content_type
    response["content-length"] = len(ad3.picture)
    response.write(ad3.picture)
    return response




class CommentCreateView(IsCustomer,LoginRequiredMixin,View):

    def post(self,request,pk):

        ad_object = get_object_or_404(Ad3,id=pk)

        comments = Coment(text=request.POST['text'],owner=request.user,ad=ad_object)
        comments.save()
        
        return redirect(reverse("ad_detail",args=[pk]))


class CommentDeleteView(IsCustomer,OwnerDeleteView):
    model = Coment
    template_name = "ads3/comment_delete.html"

    def get_success_url(self):

        ad = self.object.ad

        return reverse("ad_detail",args=[ad.id])
    


@method_decorator(csrf_exempt, name='dispatch')
class AddFavouriteView(IsCustomer,LoginRequiredMixin,View):

    def post(self,request,pk):

        ad_fav = get_object_or_404(Ad3,id=pk)
        favourite = Favourite(ad=ad_fav,owner=request.user)

        try:
            favourite.save()
        except IntegrityError:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavouriteView(IsCustomer,LoginRequiredMixin,View):

    def post(self,request,pk):

        ad_fav = get_object_or_404(Ad3,id=pk)
        

        try:
            
            Favourite.objects.get(ad=ad_fav,owner=request.user).delete()        
        except Fav.DoesNotExist:
            pass

        return HttpResponse()


# Cart stuff--------------------------------------------------------------------------


class CartListView(IsCustomer,LoginRequiredMixin,View):

    template_name = "ads3/cart_items_list.html"

    def get(self,request):
        

        #check if there is cart data in session otherwise return emty dictionary
        cart_data = request.session.get('cartdata',{})

        print(cart_data)
        # list to store cart items
        cart_items = []

        # loop through all varaition where etch on is a dictionary and add it as list item
        for variation_key ,item in cart_data.items():
            cart_items.append({
                
                'variation_key':variation_key,
                'id':item['id'],
                'title':item['title'],
                'color':item['color'],
                'size':item['size'],
                'quantity':item['quantity'],
                'image_url':item['image_url'],
                'price':item['price'],
                'total_price':float(item['price']*int(item['quantity']))
            })

        total_cart_price = sum([item['total_price'] for item in cart_items])
        ctx = {"items":cart_items,"total_cart_price":total_cart_price}
        return render(request,self.template_name,ctx)    

    """
    def get(self,request):
        #try to get the cart if 404 return we send empty dict indicat the cart is empty
        try:            
            cart = get_object_or_404(Cart,user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            ctx = {"items":cart_items,"cart":cart,"total_price":cart.total_price()}
        except:
            ctx = {}

        return render(request,self.template_name,ctx)
"""


class AddToCartView(LoginRequiredMixin,IsCustomer, View):
    
    def post(self, request):

        #del request.session['cartdata']
        
        data = json.loads(request.body)
        
        # Generate a unique key for each product variation using product_id, color, and size
        variation_key = f"{data['id']}_{data['color']}_{data['size']}_{data['price']}"
        print(f" the key is {variation_key}")

        # Create a dictionary to hold the new item data
        new_cart_item = {
            'id':data['id'],
            'title': data['title'],
            'color': data['color'],
            'size': data['size'],
            'quantity': int(data['quantity']),
            'price': float(data['price']),
            'image_url':data['image_url'],
        }

        # Check if the session already has a 'cartdata' key
        if "cartdata" in request.session:
            cart_data = request.session['cartdata']

            # Check if the variation already exists in the cart
            if variation_key in cart_data:
                # If it does, update the quantity by adding the new quantity
                cart_data[variation_key]['quantity'] += new_cart_item['quantity']
            else:
                # If the variation doesn't exist, add it as a new item to the cart
                cart_data[variation_key] = new_cart_item

            # Save the updated cart back to the session
            request.session['cartdata'] = cart_data
        else:
            # If no cart exists in the session, create one and add the first variation
            request.session['cartdata'] = {variation_key: new_cart_item}

        # Print the session cart for debugging purposes
        print(f"cartdata is {request.session['cartdata']}")

        # Return the updated cart data as JSON
        return JsonResponse({'data': request.session['cartdata']})

"""
    def post(self,request):

        data = json.loads(request.body)
        
        #del request.session['cartdate']
        cart = {}
        cart[str(data['id'])]={

            #'id':request.GET['id'],
            'title':data['title'],
            'color':data['color'],
            'size':data['size'],
            'quantity':data['quantity'],
            'price':data['price'],
        }

        print(cart)
        
        if "cartdata" in request.session:
            if str(data['id']) in request.session['cartdata']:
                cart_data = request.session['cartdata']
                cart_data[str(data['id'])]['quantity'] = int(cart[str(data['id'])]['quantity'])
                cart_data.update(cart_data)
                request.session['cartdata'] = cart_data
            else:
                #cart_data = request.session['cartdata']
                #cart_data.update(cart_data)
                request.session['cartdata'] = cart
        else:
            request.session['cartdata'] = cart

            

        print(f"cartdata is {request.session['cartdata']}")
        return JsonResponse({'data':request.session['cartdata']})

        


    def post(self, request, pk):
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        ad_product = get_object_or_404(Ad3, id=pk)
        ad_price = ad_product.price

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=ad_product, price=ad_price)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        total_price = cart_item.quantity*cart_item.price
        total_amount = cart.total_price()
        return JsonResponse({'success': True, 'quantity': cart_item.quantity,'price':total_price,"total":total_amount})
    """
            

class UpdateCartView(IsCustomer, LoginRequiredMixin, View):
    
    def post(self, request):
        remove = False
        try:
            # Attempt to parse the JSON data from the request body
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})

        # Ensure the 'key' is provided in the data
        variation_key = data.get('key')
        if not variation_key:
            return JsonResponse({'success': False, 'message': 'Variation key missing'})

        # Retrieve the cart data from the session
        cart_data = request.session.get('cartdata', {})

        # Check if the item exists in the cart
        if variation_key in cart_data:
            #get the total
            total_cart_price = data.get('total_cart_price')
            # Check if an 'action' (increment, decrement, remove) is specified
            action = data.get('action', 'add')  # Default action is 'increment'

            if action == 'add':
                # Increase the quantity of the item
                cart_data[variation_key]['quantity'] += 1
                
                #updataign the total 
                total_cart_price = float(total_cart_price) + cart_data[variation_key]['price']    

            elif action == 'delete':
                # Decrease the quantity but ensure it doesn't drop below 1
                if cart_data[variation_key]['quantity'] > 1:
                    cart_data[variation_key]['quantity'] -= 1

                    
                    total_cart_price = float(total_cart_price) - cart_data[variation_key]['price']    
                elif cart_data[variation_key]['quantity'] == 1:
                    # Remove the item from the cart entirely
                    #total_cart_price = float(total_cart_price) + cart_data[variation_key]['price']    
                    cart_data.pop(variation_key)
                    remove = True
                    
                    #return JsonResponse({'success': False, 'message': 'Quantity cannot be less than 1'})

           
            else:
                return JsonResponse({'success': False, 'message': f'Invalid action: {action}'})

            # Update the session with the modified cart data
            request.session['cartdata'] = cart_data
            if remove:
                return JsonResponse({'success':True,'remove':True})
                
            return JsonResponse(
                {'success': True,
                 'quantity': cart_data[variation_key]['quantity'],
                 'price':float(int(cart_data[variation_key]['quantity'])*cart_data[variation_key]['price']),
                 'total_cart_price':total_cart_price})
        
        # If the item is not in the cart
        return JsonResponse({'success': False, 'message': 'Item not found in cart'})


class DeleteFromCart(IsCustomer,LoginRequiredMixin,View):

    def post(self,request,item_pk):

        remove = False
        cart = get_object_or_404(Cart,user=request.user)

       # product_ad = get_object_or_404(Ad3,id=item_pk)

       
        cart_item = CartItem.objects.get(id=item_pk)

        if cart_item.quantity==1:
            remove=True
            cart_item.delete()

        else:
            cart_item.quantity -=1
            cart_item.save()

        total_price = cart_item.quantity*cart_item.price
        total_amount = cart.total_price()
        return JsonResponse({'success': True, 'quantity': cart_item.quantity,'price':total_price,"remove":remove,"total":total_amount})




class DeliveryCost(IsCustomer,LoginRequiredMixin,View):

    def post(self,request):

        try:
            data = json.loads(request.body)
            longitude = data['longitude']
            latitude = data['latitude']
            request.session["lat"] =latitude
            request.session["lng"] = longitude

        

        
            order_location = (latitude,longitude)
            shope_location = (32.218900, 20.065400)
        

            distance = geodesic(shope_location, order_location).km 
            
            delivery_cost = int(distance)

            request.session["delivery_cost"] = delivery_cost
            print(f"Delivey Cost {delivery_cost}")
        except JSONDecodeError:
            return JsonResponse({'success':False,"message":"bad json"})

        return JsonResponse({'success':True,'redirect_url':reverse("order_confirmation")})
    
    


def order_confirmation(request):

    cart_data = request.session.get('cartdata',{})
    
    #get how many item in the cart
    number_item = len(cart_data)

    total_cart_price = sum([float(int(item['price'])*item['quantity']) for variation_key,item in cart_data.items()])

    total_cost = request.session['delivery_cost'] + total_cart_price
    
    ctx = {"items":cart_data,"item_count":number_item,"cart_total":total_cart_price,"total":total_cost}

    return render(request,"ads3/order_confirmation.html",ctx)

    
    """
    cart = get_object_or_404(Cart,id=cart_id)
    cart_items = CartItem.objects.filter(cart=cart)

    
    delivery_cost = request.session["delivery_cost"]
    total = delivery_cost + cart.total_price()
    
    return render(request,"ads3/order_confirmation.html",
                  {"cart":cart,"items":cart_items,"total":total,"cart_total":cart.total_price(),"delivery_cost":delivery_cost})
    """



    
        

    

class AddOrderView(IsCustomer,LoginRequiredMixin,View):

    def get(self,request):        

        #get the cart data from the session if exist
        cart_data = request.session.get('cartdata',{})
        # calculate the total price of the cart loop through all the item and sum the price *quantity
        total_cart_price = sum([float(int(item['price'])*item['quantity']) for variation_key,item in cart_data.items()])
        #get delivery cost form session
        delivery_cost = request.session['delivery_cost']

        #calculate the total cost of cart with delivey
        total = total_cart_price + delivery_cost
        
        #create order object
        order = Order(owner=request.user,total_amount=total_cart_price,delivery_cost=delivery_cost,total=total)

        # store location of the order from session
        order.longitude = request.session["lng"]
        order.latitude = request.session["lat"]
        
        print(f"order longitude {order.longitude} , order latitude {order.latitude}")
        order.save()

        # here we create  order item by looping though all the item in the cart_date dictionary of the session
        for key, item in cart_data.items():
            #eatch key is unique varaition of product and his value is {} contain the variation data
            #get the product and other varaion data
            ad = get_object_or_404(Ad3,id=item['id'])
            color = get_object_or_404(Color,id=item['color'])
            size = get_object_or_404(Size,title=item['size'])
            price = item['price']
            quantity = item['quantity']

            # get the varaion object with this data 
            product_variant = get_object_or_404(
                ProductVaraint,product=ad,color=color,size=size,price=price)

            # use the varaion object and other data to create order item 
            OrderItem.objects.create(
                order=order,product_variant=product_variant,quantity=quantity,price=float(price*quantity)).save()

        # delete the data form the session
        del request.session['cartdata']
        return redirect(reverse("all"))

        
        """
        cart = get_object_or_404(Cart,id=cart_id,user=request.user)
        order = Order(owner=request.user,total_amount=cart.total_price())

        order.longitude = request.session["lng"]
        order.latitude = request.session["lat"]

        #del request.session["key"] for dealeting from session

        order.delivery_cost = request.session["delivery_cost"]
        order.total = order.total_amount + order.delivery_cost
        
        
        #order.longitude = data['longitude']
        #order.latitude =  data['latitude']

        print(f"order longitude {order.longitude} , order latitude {order.latitude}")
        order.save()

        cart_items = CartItem.objects.filter(cart=cart)
        print(cart_items)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,product=item.product,quantity=item.quantity,price=item.price*item.quantity).save()
            
        cart.delete()

        return redirect(reverse("all"))

        # order_items = OrderItem.objects.filter(order=order)

       
        #return JsonResponse({'success':True,'redirect_url':reverse("order_confirmation",args=[order.id])})
        # return render(request,"ads3/order_confirmation.html",{"order":order,"items":order_items})
"""
       



class OrderListView(IsCustomer,LoginRequiredMixin,View):

    template_name = "ads3/customer_order.html"
    def get(self,request):

        orders = Order.objects.filter(owner=request.user).order_by("-created_at")
        orders_num = len(orders)


        
        ctx = {"order_list":orders,"number":orders_num}
        return render(request,self.template_name,ctx)
    
        


class OrderDetailView(LoginRequiredMixin,View):
    template_name = "ads3/order_detail.html"

    def get(self,request,pk):

        order = Order.objects.get(id=pk)
        order_items = OrderItem.objects.filter(order=order)

        ctx = {"items":order_items,"order":order}

        return render(request,self.template_name,ctx)


#driver stuff

class IsDriver(UserPassesTestMixin,LoginRequiredMixin):


    def test_func(self):
        #check if the requested user 
        return isinstance(self.request.user,Driver)

    def handle_no_permission(self):

        return redirect(reverse("all"))
    

class AllOrderListView(IsDriver,ListView):

    model = Order
    template_name = "ads3/orders_list.html"


    def get_queryset(self):

        return Order.objects.filter(status="PE")
'''

class BaseOrderAction(IsDriver,View):

    def get_order(self,order_id):
        return get_object_or_404(Order,id=order_id)

    def change_status(self,dic):

        for key in dic:
            key.status = dic[key]
            key.save()
            print(key.status)
        

'''
"""
class BaseOrderAction(IsDriver,View):

    def get_order(self,order_id,driver=None):

        try:
            from django.db import transaction

            with transaction.atomic():

                order = Order.objects.select_for_update().get(id=order_id)

                if  driver:

                    if order.status=="PE":

                        driver_order = DriverOrder(order=order,driver=driver)
                        driver_order.save()

                        order.status = "PR"
                        order.save()
                        print("order  picked  succussfully")
                    else:
                        print("order has been picked by other driver")
                else:

                    driver_order = get_object_or_404(DriverOrder,order=order)

                    driver_order.status = "Delivered"
                    driver_order.save()

                    order.status = "DE"
                    order.save()
        except Order.DoesNotExist:
            print("order does not exist")
                    

"""

def compute_distance(request):

    if request.method=="POST":
        data = json.loads(request.body)
        
        driver = request.user
        driver.longitude = data['longitude']
        driver.latitude = data['latitude']
        driver.save()

        order = get_object_or_404(Order,id=data['order_id'])

        customer_location = (order.latitude,order.longitude)
        driver_location = (driver.latitude,driver.longitude)

        distance = geodesic(driver_location, customer_location).km

        if distance< 0.1:
            order.status = "DE"
            order.save()

            driver_order = get_object_or_404(DriverOrder,order=order)
            driver_order.status = "Delivered"
            driver_order.save()


        return JsonResponse({'success':True})
    
        

    
    




class BaseOrderAction(IsDriver,View):

    def get_order(self,order_id):

        return Order.objects.select_for_update().get(id=order_id)

    def create_driver_order(self,order,driver):
        return DriverOrder.objects.create(order=order,driver=driver)
        

    def get_driver_order(self,order):
        return get_object_or_404(DriverOrder,order=order)

    def change_status(self,obj,status):

        obj.status = status
        obj.save()
        

    def process_order_action(self,**kwargs):
        pass




              
class PickOrder(BaseOrderAction):
    
    def post(self,request):

        try:
            
            data = json.loads(request.body)
        except json.JSONDecodeError:
            print(" json decode error")
            return JsonResponse({'error':'json error'},status=400)

        
        order_id = data['order_id']
        order = self.get_order(order_id)
        driver = request.user
        driver.latitude = data['latitude']
        driver.longitude = data['longitude']
        driver.save()

         
        self.process_order_action(order=order ,driver=driver)


        print(f" order status  is {order.status}")
        return JsonResponse({'order_status':order.status})
        #return redirect(reverse("all_order"))
        
    def process_order_action(self,**kwargs):

        try:
            
            with transaction.atomic():
                order = kwargs['order']

                
                customer_location = (order.latitude,order.longitude)
                driver_location = (kwargs['driver'].latitude,kwargs['driver'].longitude)
                distance = geodesic(driver_location, customer_location).km


                if order.status=="PE":
                    driver_order = self.create_driver_order(order,kwargs['driver'])
                    print(f"driver order {driver_order}")
                    self.change_status(order,"PR")
                    print(f" order status is {order.status}")
                if distance<0.1:
                    self.change_status(order,"DE")
                    print(f" order status is {order.status}")
                    self.change_status(driver_order,"Delivered")
                    print(f"driver  order status is {driver_order.status}")
        except Order.DoesNotExist:
             print("order does not exist !")

    
        '''
        order = self.get_order(order_id)
        driver_order = DriverOrder(driver = request.user,order=order)
        driver_order.save()

        self.change_status({order:"PR"})
        '''

#        self.get_order(order_id,request.user)

        
"""          
class PickOrder(BaseOrderAction):

    def post(self,request,order_id):

        self.process_order_action(order_id = order_id,driver=request.user)


        
        return redirect(reverse("all_order"))

    def process_order_action(self,**kwargs):

        try:
            
            with transaction.atomic():
                order = self.get_order(kwargs['order_id'])

                if order.status=="PE":
                    driver_order = self.create_driver_order(order,kwargs['driver'])

                    self.change_status(order,"PR")
                else:
                    print("order has been picked")
                    
                    
                   
        except Order.DoesNotExist:
             print("order does not exist !")

    
        '''
        order = self.get_order(order_id)
        driver_order = DriverOrder(driver = request.user,order=order)
        driver_order.save()

        self.change_status({order:"PR"})
        '''

#        self.get_order(order_id,request.user)

"""
class DeliveredOrderView(BaseOrderAction):

    def post(self,request,order_id):

        self.process_order_action(order_id=order_id)
        
        return redirect(reverse("driver_order_list"))

    


    def process_order_action(self,**kwargs):

        print("i am in delivered function")
        try:
            
            with transaction.atomic():
                
                order = self.get_order(kwargs['order_id'])
                print("done get order")
                
                
                driver_order = self.get_driver_order(order)
                print("done get driver")
                
                self.change_status(order,"DE")
                self.change_status(driver_order,"Delivered")
                print("done delivered")
                
        except Order.DoesNotExist:
            print("order does not exist !")



        '''
        order = self.get_order(order_id)
        driver_order = get_object_or_404(DriverOrder,id=order_id)
        
        self.change_status({order:"DE",driver_order:"Delivered"})
        '''

#        self.get_order(order_id,None)
        
   


class DriverOrderListView(IsDriver,ListView):

    model = DriverOrder
    template_name = "ads3/driver_orders.html"

    
    def get_queryset(self):

        querty = DriverOrder.objects.filter(driver=self.request.user,status="Picked")
        print(querty)
        return querty


class DeliveredOrderListView(IsSuperUser,ListView):

    model = DriverOrder
    template_name = "ads3/delivered_order_list.html"

    def get_queryset(self):
        return DriverOrder.objects.filter(driver=self.request.user,status="Delivered")


    def get_context_data(self):

        ctx = super().get_context_data()
        ctx["total"] = DriverOrder.total_money(self,self.request.user)
        return ctx

    
    
        
# track order and map stuff

class BaseMapView(View):

    order = None
    driver_order = None
    driver = None
    
    def get_driver(self,request,order_id):
                
        try:
            self.order = get_object_or_404(Order,id=order_id)
            self.driver_order = get_object_or_404(DriverOrder,order=self.order)
            self.driver = self.driver_order.driver
        except:
            return redirect(reverse_lazy('order_list'))
        
        

        
    def get(self,request,order_id):

        self.get_driver(request,order_id)

        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        
            print(f"request type is => {request.method}")       
            print(self.driver.latitude,self.driver.longitude)
            return JsonResponse({"driver_latitude":self.driver.latitude,"driver_longitude":self.driver.longitude,
                                 "order_latitude":self.order.latitude,"order_longitude":self.order.longitude,
                                 "name":self.driver.username,
                                 "driver":isinstance(request.user,Driver),})
            
            
        print(f"request type is => {request.method}")
        return render(request,"ads3/track_order.html",{'order_id':order_id})
    
         

class DriverMapView(IsDriver,BaseMapView):

    def get_driver(self,request,order_id):    
        try:
            self.order = get_object_or_404(Order,id=order_id)
            self.driver_order = get_object_or_404(DriverOrder,order=self.order)
            self.driver = self.driver_order.driver
        except:
            self.driver = request.user
            self.driver.latitude = "32.115900"
            self.driver.longitude = "20.065400"


class CustomerMapView(BaseMapView):
    pass

    
        
        


"""
    
def track_driver(request,order_id):
    try:
        
        order = get_object_or_404(Order,id=order_id)
        driver_order = get_object_or_404(DriverOrder,order=order)
        driver = driver_order.driver
        
        if request.method =="GET":
            
            print(f"request type is => {request.method}")
            return render(request,"ads3/track_order.html",{'order_id':order_id})
        else:
            
            print(f"request type is => {request.method}")
            
       
            print(driver.latitude,driver.longitude)
            
            return JsonResponse({"driver_latitude":driver.latitude,"driver_longitude":driver.longitude,
                                 "order_latitude":order.latitude,"order_longitude":order.longitude,
                                 "name":driver.username})
    except:
        if isinstance(request.user,Driver):

            return render(request,"ads3/track_order.html",{'order_id':order_id})
            
        
        return redirect(reverse_lazy('order_list'))
            
   """     
"""
    order = get_object_or_404(Order,id=order_id)
    
    if request.method =="GET":
        if(order.status == 'PE'):
            return redirect(reverse_lazy('order_list'))
        else:
            print(f"request type is => {request.method}")
            return render(request,"ads3/track_order.html",{'order_id':order_id})
    
    else:
        print(f"request type is => {request.method}")
        
       # order = get_object_or_404(Order,id=order_id)
        try:
            
            driver_order = get_object_or_404(DriverOrder,order=order)
            driver = driver_order.driver
            print(driver.latitude,driver.longitude)
            return JsonResponse({"driver_latitude":driver.latitude,"driver_longitude":driver.longitude,
                                 "order_latitude":order.latitude,"order_longitude":order.longitude,
                                 "name":driver.username})

        except:
            return JsonResponse({'exception':'no-orderdriver'})

   """ 

    
    
