from django.urls import path
from .views import search_view, book_view, home_view, category_view

urlpatterns = [
    path('', home_view, name='home'),
    path('books/', book_view, name='books'),
    path('books/search/', search_view, name='search'),
    path('books/<str:category>/', category_view, name='by-category'),
]
