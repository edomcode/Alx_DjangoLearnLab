# relationship_app/views.py
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Book

# 🟢 Function-Based View
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})

# 🔵 Class-Based View
class BookDetailView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'relationship_app/book_detail.html', {'book': book})

