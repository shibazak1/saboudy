from django.urls import path ,include
from django.contrib import admin
from . import views


urlpatterns = [

    # urls.py

    #path('accounts/login/', views.custom_login_view, name='login'),
    #path('accounts/login/',views.CustomLoginView.as_view(template_name='registration/login_social.html'),name="login"),

    path("ads3/signin",views.SignIn.as_view(),name="signin"),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path("",views.main,name="main"),
    path("ads3/list",views.AdListView.as_view(),name="all"),
    path("ads3/detail/<int:pk>",views.AdDetailView.as_view(),name="ad_detail"),
    path ("ads3/create",views.AdCreateView.as_view(),name="ad_create"),
    path("ads3/update/<int:pk>",views.AdUpdateView.as_view(),name="ad_update"),
    path("ads3/delete<int:pk>",views.AdDeleteView.as_view(),name="ad_delete"),
    path("ads3/pic/<int:pk>",views.stream_file,name="ad_pic"),
    #comment stuff
    path("ads3/comment/create/<int:pk>",views.CommentCreateView.as_view(),name="comment_create"),
    path("ads3/delete/<int:pk>",views.CommentDeleteView.as_view(),name="comment_delete"),

    #favourite urls
    path("ads3/add/<int:pk>/favourite",views.AddFavouriteView.as_view(),name="favourite"),
    path("ads3/delete/<int:pk>/favourite",views.DeleteFavouriteView.as_view(),name="unfavourite"),

    #Cart urls
    path("ads3/cart/list",views.CartListView.as_view(),name="cart_list"),
    #path("ads3/add/<int:pk>/cart",views.AddToCartView.as_view(),name="add_to_cart"),
    path("ads3/add/cart",views.AddToCartView.as_view(),name="add_to_cart"),
    path("ads3/update/cart",views.UpdateCartView.as_view(),name="update_cart"),
    path("ads3/delete/<int:item_pk>/cart",views.DeleteFromCart.as_view(),name="delete_from_cart"),

    #order stuff
    #path("ads3/<int:cart_id>/order",views.AddOrderView.as_view(),name="order"),
   # path("ads3/order/<int:order_id>/confirmation",views.order_confirmation,name="order_confirmation"),
    path("ads3/order",views.AddOrderView.as_view(),name="order"),
    path("ads3/order/confirmation",views.order_confirmation,name="order_confirmation"),
    path("ads3/order/list",views.OrderListView.as_view(),name="order_list"),
    path("ads3/order/<int:pk>/detail",views.OrderDetailView.as_view(),name="order_detail"),
    path("ads3/all/order/list",views.AllOrderListView.as_view(),name="all_order"),
    #driver stuff
    path("ads3/order/pick",views.PickOrder.as_view(),name="pick_order"),
    path("ads3/driver/order/list",views.DriverOrderListView.as_view(),name="driver_order_list"),
    path("ads3/order/<int:order_id>/delivered",views.DeliveredOrderView.as_view(),name="delivered_order"),
    path("ads3/order/delivered",views.DeliveredOrderListView.as_view(),name="delivered_order_list"),
    path("ads3/compute/distance",views.compute_distance,name="compute_distance"),
    #track order stuff
  #  path("ads3/map/<int:order_id>",views.view_map,name="view_map"),
    #path("ads3/track/<int:order_id>/driver",views.track_driver,name="track_driver"),
    path("ads3/customer/<int:order_id>/map",views.CustomerMapView.as_view(),name="customer_map"),
    path("ads3/driver/<int:order_id>/map",views.DriverMapView.as_view(),name="driver_map"),

    #delivery cost
    path("ads3/delivery/cost",views.DeliveryCost.as_view(),name="delivery_cost"),


    #----
    path("ads3/redirect",views.redirection,name="redirection"),

    #moneter url
    path("ads3/moneter",views.Moneter.as_view(),name="moneter"),

    #pushnotification stuff
    path("ads3/subscribe",views.subscribe,name="subscribe"),

    #caches stuff an offline page to return when the netowrk is off
    path("ads3/offline",views.offLine,name="offline"),
    
    
]
