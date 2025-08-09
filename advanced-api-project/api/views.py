from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter, AuthorFilter


# =============================================================================
# AUTHOR VIEWS
# =============================================================================

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    Enhanced API view for listing and creating authors with advanced filtering.

    This view provides comprehensive filtering and search capabilities for authors.

    GET: Returns a list of all authors with their nested books
    POST: Creates a new author (requires authentication)

    Supported Query Parameters:

    FILTERING:
    - name: Filter by author name (partial match, case-insensitive)
    - name_exact: Filter by exact author name
    - has_books: Filter authors who have published books (true/false)
    - min_books: Filter authors with at least this many books

    SEARCHING:
    - search: Search in author names

    ORDERING:
    - ordering: Sort by name, book count, etc.

    Examples:
    - /api/authors/?name=tolkien&has_books=true
    - /api/authors/?min_books=2&ordering=name
    - /api/authors/?search=george&ordering=-name

    Permissions:
    - GET: Available to all users (authenticated and unauthenticated)
    - POST: Requires authentication
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Configure filter backends
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # Use custom filter class
    filterset_class = AuthorFilter

    # Search configuration
    search_fields = ['name', '^name']  # Search by name, with starts-with option

    # Ordering configuration
    ordering_fields = ['name', 'id']
    ordering = ['name']  # Default: alphabetical by name

    def get_queryset(self):
        """
        Enhanced queryset with optimizations and legacy parameter support.

        Provides:
        - Query optimization with prefetch_related for books
        - Legacy parameter support for backward compatibility
        - Additional filtering options
        """
        # Base queryset with optimization
        queryset = Author.objects.prefetch_related('books').all()

        # Legacy parameter support (maintained for backward compatibility)
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
    Enhanced ListView for retrieving all books with comprehensive filtering.

    This view provides advanced query capabilities including:
    - Comprehensive filtering by multiple fields
    - Full-text search across title and author
    - Flexible ordering options
    - Custom filtering methods

    Supported Query Parameters:

    FILTERING:
    - title: Filter by title (partial match, case-insensitive)
    - title_exact: Filter by exact title
    - publication_year: Filter by exact year
    - publication_year_min: Books published from this year onwards
    - publication_year_max: Books published up to this year
    - author: Filter by author ID
    - author_name: Filter by author name (partial match)
    - author_name_exact: Filter by exact author name
    - decade: Filter by decade (1940s, 1950s, etc.)
    - has_recent_publication: Recent books (last 10 years)

    SEARCHING:
    - search: Full-text search across title and author name

    ORDERING:
    - ordering: Sort by any field (title, publication_year, author__name)
    - Use '-' prefix for descending order (e.g., -publication_year)

    Examples:
    - /api/books/?title=harry&ordering=-publication_year
    - /api/books/?author_name=rowling&publication_year_min=1990
    - /api/books/?search=fantasy&decade=1990s
    - /api/books/?has_recent_publication=true&ordering=title

    Permissions: Open to all users (no authentication required)
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = []  # No authentication required for reading

    # Configure filter backends
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # Use custom filter class for advanced filtering
    filterset_class = BookFilter

    # Basic filterset fields for simple filtering
    filterset_fields = ['title', 'author', 'publication_year']

    # Search configuration - Enable search functionality on Book model fields (title and author)
    search_fields = [
        'title',           # Search in book title field
        'author__name',    # Search in author name field
        '=title',          # Exact match option for title
        '^title',          # Starts with option for title
    ]

    # Ordering configuration
    ordering_fields = [
        'title',
        'publication_year',
        'author__name',
        'id'
    ]
    ordering = ['-publication_year', 'title']  # Default: newest first, then alphabetical

    def get_queryset(self):
        """
        Enhanced queryset with optimizations and additional filtering.

        Provides:
        - Query optimization with select_related
        - Legacy parameter support for backward compatibility
        - Additional custom filtering options

        Legacy Query Parameters (maintained for backward compatibility):
        - year_from: Filter books published from this year onwards
        - year_to: Filter books published up to this year
        """
        # Base queryset with optimization
        queryset = Book.objects.select_related('author').all()

        # Legacy parameter support for backward compatibility
        year_from = self.request.query_params.get('year_from', None)
        year_to = self.request.query_params.get('year_to', None)

        if year_from is not None:
            try:
                year_from = int(year_from)
                queryset = queryset.filter(publication_year__gte=year_from)
            except (ValueError, TypeError):
                pass  # Ignore invalid year values

        if year_to is not None:
            try:
                year_to = int(year_to)
                queryset = queryset.filter(publication_year__lte=year_to)
            except (ValueError, TypeError):
                pass  # Ignore invalid year values

        # Additional custom filtering
        popular_only = self.request.query_params.get('popular_only', None)
        if popular_only and popular_only.lower() == 'true':
            # Filter books by authors who have written multiple books
            queryset = queryset.filter(
                author__in=Author.objects.annotate(
                    book_count=Count('books')
                ).filter(book_count__gt=1)
            )

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Enhanced list method with additional metadata.

        Returns the standard paginated response with additional
        metadata about filtering and search results.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Get pagination info
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            # Add metadata
            response.data['meta'] = {
                'total_count': queryset.count(),
                'filters_applied': bool(request.query_params),
                'available_filters': self.get_available_filters(),
            }
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'meta': {
                'total_count': queryset.count(),
                'filters_applied': bool(request.query_params),
                'available_filters': self.get_available_filters(),
            }
        })

    def get_available_filters(self):
        """
        Return information about available filters for API documentation.
        """
        return {
            'filtering': {
                'title': 'Filter by title (partial match)',
                'title_exact': 'Filter by exact title',
                'publication_year': 'Filter by exact year',
                'publication_year_min': 'Books from this year onwards',
                'publication_year_max': 'Books up to this year',
                'author': 'Filter by author ID',
                'author_name': 'Filter by author name (partial)',
                'decade': 'Filter by decade (1940s, 1950s, etc.)',
                'has_recent_publication': 'Recent books (true/false)',
            },
            'searching': {
                'search': 'Search across title and author name',
            },
            'ordering': {
                'ordering': 'Sort by: title, publication_year, author__name (use - for desc)',
            },
            'legacy': {
                'year_from': 'Legacy: Books from this year onwards',
                'year_to': 'Legacy: Books up to this year',
                'popular_only': 'Books by authors with multiple publications',
            }
        }


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
