from django.shortcuts import render
from .models import BookModel
from django.db.models import Q


def search_view(request):
    query = request.GET.get('q', '')
    results = BookModel.objects.none()
    if query:
        results = BookModel.objects.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(isbn__icontains=query)
        ).distinct()
    return render(request, 'books/search.html', {'results': results, 'query': query})


def book_view(request):
    books = BookModel.objects.all()
    return render(request, 'books/all_books.html', {'books': books})


def home_view(request):
    if request.method == "GET":
        return render(request, 'index.html')


def category_view(request, category):
    if request.method == "GET":
        filtered_books = BookModel.objects.filter(category__name=category)
        return render(request, 'books/by-category.html', {"books": filtered_books})
