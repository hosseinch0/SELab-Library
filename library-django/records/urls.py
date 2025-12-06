from django.urls import path
from .views import records_view, borrow_book, fine_records


urlpatterns = [
    path('borrowed/', records_view, name='user-records'),
    path('borrow/', borrow_book, name='borrow-book'),
    path('fine/', fine_records, name="fine"),
]
