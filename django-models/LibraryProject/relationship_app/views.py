from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Author, Book

# 🏠 Home View
def home(request):
    return render(request, 'relationship_app/home.html')

# 📚 Author List View
def authors_list(request):
    authors = Author.objects.all()
    return render(request, 'relationship_app/authors_list.html', {'authors': authors})

# 📘 Book List View
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})

# 📖 Book Detail View (Class-Based)
class BookDetailView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'relationship_app/book_detail.html', {'book': book})
