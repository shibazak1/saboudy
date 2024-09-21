
from django.contrib import admin
from django.urls import include, path
from books import views

urlpatterns = [
    path('books_list', views.books_list,name="books_list"),
    path('book_add', views.BookAdd.as_view(),name="addbook"),
    path('book_update/<int:pk>', views.BookUpdate.as_view(),name="bookupdate"),
    path('book_delet/<int:pk>', views.BookDelelte.as_view(),name="bookdelete"),
    path('addauthor', views.AddAuthor.as_view(),name="addauthor"),
    path('authors_list', views.AuthorView.as_view(),name="authorview"),
    path('authors_update/<int:pk>', views.AuthorUpdate.as_view(),name="authorupdate"),
    path('authors_delete/<int:pk>', views.AuthorDelete.as_view(),name="authordelete"),
    
    
       
]




