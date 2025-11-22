from django.urls import path
from .views import records_view, borrow_book


urlpatterns = [
    path('', records_view, name='user-records'),
    path('borrow/', borrow_book, name='borrow-book'),
]
