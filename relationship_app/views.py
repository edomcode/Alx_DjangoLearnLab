from django.shortcuts import render
from .models import Author

def home(request):
    return render(request, 'relationship_app/home.html')

def authors_list(request):
    authors = Author.objects.all()
    return render(request, 'relationship_app/authors_list.html', {'authors': authors})
