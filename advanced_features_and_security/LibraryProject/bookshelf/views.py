from django.shortcuts import render
from django.http import HttpResponse
def index(request):
	return HttpResponse("Welcome to my book store.")

from django.shortcuts import render, get_object_or_404
from .models import Book
from .forms import BookForm
from django.db.models import Q

def book_list(request):
    query = request.GET.get('q')
    books = Book.objects.all()
    if query:
        # Safe query using ORM (no raw SQL or string interpolation)
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'bookshelf/book_list.html', {'books': books})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():  # Ensures data is validated and sanitized
            form.save()
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})
