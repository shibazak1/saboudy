"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

 
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from django.contrib import admin
from django.urls import path, include ,re_path
from django.contrib.auth import views as auth_views
from ads3 import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("ads3.urls")),
   
   
    #path('accounts/login/',views.CustomLoginView.as_view(template_name='registration/login_social.html'),name="login"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login_social.html'),name="login"),
    path("accounts/",include("django.contrib.auth.urls")),
    path('', include('pwa.urls')),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),  # Keep

   # path('service-worker.js', RedirectView.as_view(url='/static/js/service-worker.js', permanent=True)),
    re_path(r'^serviceworker.js$', RedirectView.as_view(url=settings.STATIC_URL + 'js/serviceworker.js', permanent=True)),

    re_path(r'^webpush/', include('webpush.urls'))

]      
                                                                                
                          


# Add static file serving in development (if not already done)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Switch to social login if it is configured - Keep for later

try:
    from . import github_settings
    social_login = 'registration/login_social.html'
    urlpatterns.insert(0,
                       path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
                       )
    print('Using', social_login, 'as the login template')
except:
    print('Using registration/login.html as the login template')

# References

# https://docs.djangoproject.com/en/4.2/ref/urls/#include
