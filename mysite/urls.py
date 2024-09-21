


urlpatterns = [
    path('/test/', include('test.urls')),
    path("books/",include("books.urls")),
    path('admin/', admin.site.urls),
    
    
]
