
from django.urls import path

from . import views
'''path function match the requested url to a view function or class '''
urlpatterns = [
    path("", views.index, name="index"),
    path("index2",views.index2, name="index2"),
    path("index3",views.index3),
    path("index4/<int:m>",views.index4),
    path("books_list",views.books_list,name="books"),
    path("book_detail/<int:pk>",views.books_detail.as_view(),name="book"),
    path("form",views.form,name="form"),
    path("postform",views.postform , name="postform"),
    path("getpostform",views.getpostform.as_view(),name="getpostform"),
    path("addbook",views.add_book.as_view(),name="addbook"),
    path("cookies",views.cookies,name="cookies"),
    path("getcookies",views.get_cookies,name="get_cookies"),
    path("session",views.session,name="session"),
    path("yourdata",views.yourdata.as_view(),name="yourdata"),
    path("yourlogout",views.yourlogout,name="yourlogout"),
    path("dumpform",views.dumpform,name="dumpform"),
    path("createbook",views.CreateBook.as_view(),name="createbook"),
    path("crispyforms",views.crispyforms.as_view(template="test/crispy.html"),name="crispy"),
    path("success",views.success,name="success"),
    path("fetch",views.fetch,name="fetch"),
    path("json",views.json,name="json"),
]
