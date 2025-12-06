from django.shortcuts import render
from .models import BookModel
from django.db.models import Q
from django.conf import settings
import google.generativeai as genai
import os


def search_view(request):
    query = request.GET.get('q', '')
    results = BookModel.objects.none()
    if query:
        results = BookModel.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)).distinct()
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


# AI Functionality
genai.configure(api_key=settings.GEMINI_API_KEY)


def ai_assistant(request):
    result = None

    if request.method == "POST":

        user_description = request.POST.get("description")
        books = BookModel.objects.all()
        books_list_text = "\n".join([
            f"- Title: {b.title}\n  Summary: {b.summary[:300]}" for b in books
        ])

        prompt = f"""
        The user described a book. Your task is to find the closest matching book ONLY from this list.

        User description:
        \"\"\"{user_description}\"\"\"
        
        Book list:
        {books_list_text}

        Return ONLY the exact title of the closest matching book.
        If none are similar, return "NO_MATCH".
        """

        model = genai.GenerativeModel("gemini-2.5-flash")

        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)

        response = model.generate_content(
            prompt, request_options={"timeout": 15})
        result = response.text.strip()

    return render(request, "books/find_book.html", {
        "result": result
    })
