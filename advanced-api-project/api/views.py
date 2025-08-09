from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# Try to import django_filters, use fallback if not available
try:
    from django_filters.rest_framework import DjangoFilterBackend
    DJANGO_FILTERS_AVAILABLE = True
except ImportError:
    DJANGO_FILTERS_AVAILABLE = False


# =============================================================================
# AUTHOR VIEWS
# =============================================================================

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    Combined API view for listing all authors and creating new authors.

    This view combines list and create functionality for efficiency.

    GET: Returns a list of all authors with their nested books
    POST: Creates a new author (requires authentication)

    Permissions:
    - GET: Available to all users (authenticated and unauthenticated)
    - POST: Requires authentication
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Optionally filter authors by name using query parameters.
        Example: /api/authors/?name=Rowling
        """
        queryset = Author.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific author.

    GET: Returns a specific author with their nested books
    PUT/PATCH: Updates an author (requires authentication)
    DELETE: Deletes an author (requires authentication)

    Permissions:
    - GET: Available to all users
    - PUT/PATCH/DELETE: Requires authentication
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# =============================================================================
# BOOK VIEWS - SEPARATE CRUD OPERATIONS
# =============================================================================

class BookListView(generics.ListAPIView):
    """
    Generic ListView for retrieving all books.

    This view handles GET requests to retrieve a list of all books.
    Supports filtering and searching capabilities.

    Features:
    - Filtering by publication year and author
    - Search by title and author name
    - Ordering by publication year and title

    Permissions: Open to all users (no authentication required)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []  # No authentication required for reading

    # Configure filter backends based on availability
    if DJANGO_FILTERS_AVAILABLE:
        filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
        filterset_fields = ['publication_year', 'author']
    else:
        filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['title', 'author__name']
    ordering_fields = ['publication_year', 'title']
    ordering = ['-publication_year']  # Default ordering: newest first

    def get_queryset(self):
        """
        Custom queryset with additional filtering options.

        Query parameters:
        - year_from: Filter books published from this year onwards
        - year_to: Filter books published up to this year
        """
        queryset = Book.objects.select_related('author')

        year_from = self.request.query_params.get('year_from', None)
        year_to = self.request.query_params.get('year_to', None)

        if year_from is not None:
            queryset = queryset.filter(publication_year__gte=year_from)
        if year_to is not None:
            queryset = queryset.filter(publication_year__lte=year_to)

        return queryset


class BookDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for retrieving a single book by ID.

    This view handles GET requests to retrieve a specific book.

    Permissions: Open to all users (no authentication required)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []  # No authentication required for reading


class BookCreateView(generics.CreateAPIView):
    """
    Generic CreateView for adding a new book.

    This view handles POST requests to create new books.
    Includes custom validation and proper error handling.

    Features:
    - Custom validation through BookSerializer
    - Automatic author relationship handling
    - Detailed error responses

    Permissions: Requires authentication
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom create method to add additional logic during book creation.

        This method is called when a valid serializer is ready to save.
        Can be used to set additional fields or perform custom actions.
        """
        # You can add custom logic here, such as:
        # - Setting the created_by field to the current user
        # - Logging the creation event
        # - Sending notifications

        book = serializer.save()

        # Example: Log the creation (in a real app, use proper logging)
        print(f"New book created: {book.title} by {book.author.name}")

        return book

    def create(self, request, *args, **kwargs):
        """
        Override create method to provide custom response formatting.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = self.perform_create(serializer)

        # Return custom success response
        return Response({
            'message': 'Book created successfully',
            'book': BookSerializer(book).data
        }, status=status.HTTP_201_CREATED)


class BookUpdateView(generics.UpdateAPIView):
    """
    Generic UpdateView for modifying an existing book.

    This view handles PUT and PATCH requests to update books.
    Supports both full updates (PUT) and partial updates (PATCH).

    Features:
    - Partial update support
    - Custom validation
    - Detailed error handling

    Permissions: Requires authentication
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom update method to add additional logic during book updates.
        """
        # Store the old instance for comparison
        old_instance = self.get_object()
        old_title = old_instance.title

        # Save the updated instance
        book = serializer.save()

        # Example: Log the update if title changed
        if old_title != book.title:
            print(f"Book title updated: '{old_title}' -> '{book.title}'")

        return book

    def update(self, request, *args, **kwargs):
        """
        Override update method to provide custom response formatting.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        book = self.perform_update(serializer)

        return Response({
            'message': 'Book updated successfully',
            'book': BookSerializer(book).data
        })


class BookDeleteView(generics.DestroyAPIView):
    """
    Generic DeleteView for removing a book.

    This view handles DELETE requests to remove books from the database.

    Features:
    - Soft delete option (can be implemented)
    - Custom deletion logic
    - Proper error handling

    Permissions: Requires authentication
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        """
        Custom destroy method to add additional logic during book deletion.
        """
        # Store book info before deletion for logging
        book_title = instance.title
        author_name = instance.author.name

        # Perform the actual deletion
        instance.delete()

        # Example: Log the deletion
        print(f"Book deleted: '{book_title}' by {author_name}")

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to provide custom response formatting.
        """
        instance = self.get_object()
        book_title = instance.title

        self.perform_destroy(instance)

        return Response({
            'message': f"Book '{book_title}' deleted successfully"
        }, status=status.HTTP_200_OK)


# =============================================================================
# COMBINED VIEWS (LEGACY SUPPORT)
# =============================================================================

class BookListCreateView(generics.ListCreateAPIView):
    """
    Combined API view for listing all books and creating new books.

    This view is kept for backward compatibility.
    For new implementations, use separate BookListView and BookCreateView.

    GET: Returns a list of all books
    POST: Creates a new book (with validation)

    Permissions: Read-only for unauthenticated, full access for authenticated
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Combined API view for retrieving, updating, and deleting a specific book.

    This view is kept for backward compatibility.
    For new implementations, use separate Detail, Update, and Delete views.

    GET: Returns a specific book
    PUT/PATCH: Updates a book (with validation)
    DELETE: Deletes a book

    Permissions: Read-only for unauthenticated, full access for authenticated
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# =============================================================================
# API OVERVIEW AND UTILITY VIEWS
# =============================================================================

@api_view(['GET'])
@permission_classes([])  # No authentication required
def api_overview(request):
    """
    API overview endpoint that lists all available endpoints.

    This endpoint provides a comprehensive list of all API endpoints
    with their descriptions and supported HTTP methods.
    """
    api_urls = {
        'API Overview': {
            'url': '/api/',
            'methods': ['GET'],
            'description': 'This overview of available endpoints'
        },
        'Authors': {
            'List/Create': {
                'url': '/api/authors/',
                'methods': ['GET', 'POST'],
                'description': 'List all authors or create new author'
            },
            'Detail': {
                'url': '/api/authors/<int:pk>/',
                'methods': ['GET', 'PUT', 'PATCH', 'DELETE'],
                'description': 'Retrieve, update, or delete specific author'
            }
        },
        'Books': {
            'List': {
                'url': '/api/books/',
                'methods': ['GET'],
                'description': 'List all books with filtering and search'
            },
            'Detail': {
                'url': '/api/books/<int:pk>/',
                'methods': ['GET'],
                'description': 'Retrieve specific book details'
            },
            'Create': {
                'url': '/api/books/create/',
                'methods': ['POST'],
                'description': 'Create new book (authentication required)'
            },
            'Update': {
                'url': '/api/books/<int:pk>/update/',
                'methods': ['PUT', 'PATCH'],
                'description': 'Update existing book (authentication required)'
            },
            'Delete': {
                'url': '/api/books/<int:pk>/delete/',
                'methods': ['DELETE'],
                'description': 'Delete book (authentication required)'
            }
        },
        'Legacy Endpoints': {
            'Books List/Create': {
                'url': '/api/books/legacy/',
                'methods': ['GET', 'POST'],
                'description': 'Legacy combined list/create endpoint'
            },
            'Books Detail/Update/Delete': {
                'url': '/api/books/<int:pk>/legacy/',
                'methods': ['GET', 'PUT', 'PATCH', 'DELETE'],
                'description': 'Legacy combined detail/update/delete endpoint'
            }
        }
    }
    return Response(api_urls)
