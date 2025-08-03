from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from django.http import HttpResponse

def create_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        isbn = request.POST.get('isbn')
        Book.objects.create(title=title, author=author, published_date=published_date, isbn=isbn)
        return redirect('list_books')
    return render(request, 'bookshelf/create.html')

def list_books(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/list.html', {'books': books})

def retrieve_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/detail.html', {'book': book})

def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.published_date = request.POST.get('published_date')
        book.isbn = request.POST.get('isbn')
        book.save()
        return redirect('list_books')
    return render(request, 'bookshelf/update.html', {'book': book})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'bookshelf/delete.html', {'book': book})
