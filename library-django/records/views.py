from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import RecordsModel, BookModel, FineModel
from .forms import BorrowForm


def records_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == "GET":
            records = RecordsModel.objects.filter(user_id=request.user)
            return render(request, 'users/records.html', {"records": records})


def borrow_book(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to borrow a book.")
        return redirect('login')
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow_record = form.save(commit=False)
            borrow_record.user_id = request.user
            book = borrow_record.book_id

            if book.total_copies <= 0:
                messages.error(
                    request, f'"{book.title}" is currently unavailable.')
                return redirect('borrow_book')

            if borrow_record:
                book.save()
                borrow_record.save()
                messages.success(
                    request, f'You have borrowed "{book.title}" successfully!')
                return redirect('home')
            else:
                messages.error(request, "This boo is currently unavailable.")
                return redirect('borrow_book')
    else:
        form = BorrowForm()

    return render(request, 'users/borrow_book.html', {"form": form})


def fine_records(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            fines = FineModel.objects.filter(record_id__user_id=request.user)
            return render(request, 'users/fines.html', {'fines': fines})
        else:
            return redirect('login')
