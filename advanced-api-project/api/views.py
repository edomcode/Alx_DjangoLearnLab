from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorListCreateView(generics.ListCreateAPIView):
    """
    API view for listing all authors and creating new authors.

    GET: Returns a list of all authors with their nested books
    POST: Creates a new author
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific author.

    GET: Returns a specific author with their nested books
    PUT/PATCH: Updates an author
    DELETE: Deletes an author
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """
    API view for listing all books and creating new books.

    GET: Returns a list of all books
    POST: Creates a new book (with validation)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific book.

    GET: Returns a specific book
    PUT/PATCH: Updates a book (with validation)
    DELETE: Deletes a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


@api_view(['GET'])
def api_overview(request):
    """
    API overview endpoint that lists all available endpoints.
    """
    api_urls = {
        'API Overview': '/api/',
        'Authors List': '/api/authors/',
        'Author Detail': '/api/authors/<int:pk>/',
        'Books List': '/api/books/',
        'Book Detail': '/api/books/<int:pk>/',
    }
    return Response(api_urls)
