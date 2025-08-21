from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from .forms import BookForm
from .forms import ExampleForm

from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def book_list(request):
    return render(request, 'bookshelf/book_list.html')  # looks inside templates/bookshelf/
@csrf_protect
@login_required
@permission_required('book_content.can_view', raise_exception=True)
def view_books(request):
    books = Book.objects.all()
    return render(request, 'book_content/view.books.html', {'books':books})
@login_required
@permission_required('book_content.can_create', raise_exception=True)
@csrf_protect
@login_required
@permission_required('book_content.can_create', raise_exception=True)
def create_book(request):
    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if title and content:
            Book.objects.create(title=title, content=content)
            return redirect('view_books')
        else:
            return render(request, 'book_content/create_book.html', {'error': 'All fields are required.'})
    return render(request, 'book_content/create_book.html')

@csrf_protect
@login_required
@permission_required('book_content.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()  
        if title and content:
            book.title = title
            book.content = content
            book.save()
            return redirect('view_books')
        else:
            return render(request, 'book_content/edit_book.html', {'book': book, 'error': 'All fields are required.'})
    # Show form with current data
    return render(request, 'book_content/edit_book.html', {'book': book})

@login_required
@permission_required('book_content.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('view_books')
    return render(request, 'book_content/delete_book.html', {'book':book})



def search_books(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'books': books})


def add_book_view(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})
def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Normally you might save or process the data here
            return redirect('list_books')  # or wherever you want
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/example_form.html', {'form': form})