"""
Custom filters for Django REST Framework API endpoints.

This module provides advanced filtering capabilities for the Book and Author models,
including custom filter classes and field-specific filtering options.
"""

import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Book, Author


class BookFilter(filters.FilterSet):
    """
    Advanced filter class for Book model.
    
    Provides comprehensive filtering options including:
    - Exact matches for specific fields
    - Range filtering for publication years
    - Text-based filtering with multiple options
    - Author-related filtering
    """
    
    # Basic field filters
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text='Filter by title (case-insensitive partial match)'
    )
    
    title_exact = filters.CharFilter(
        field_name='title',
        lookup_expr='iexact',
        help_text='Filter by exact title (case-insensitive)'
    )
    
    # Publication year filters
    publication_year = filters.NumberFilter(
        field_name='publication_year',
        help_text='Filter by exact publication year'
    )
    
    publication_year_min = filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text='Filter books published from this year onwards'
    )
    
    publication_year_max = filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        help_text='Filter books published up to this year'
    )
    
    year_range = filters.DateFromToRangeFilter(
        field_name='publication_year',
        help_text='Filter books within a year range (use year_range_after and year_range_before)'
    )
    
    # Author filters
    author = filters.ModelChoiceFilter(
        queryset=Author.objects.all(),
        help_text='Filter by specific author ID'
    )
    
    author_name = filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text='Filter by author name (case-insensitive partial match)'
    )
    
    author_name_exact = filters.CharFilter(
        field_name='author__name',
        lookup_expr='iexact',
        help_text='Filter by exact author name (case-insensitive)'
    )
    
    # Custom filters
    decade = filters.ChoiceFilter(
        method='filter_by_decade',
        choices=[
            ('1940s', '1940s'),
            ('1950s', '1950s'),
            ('1960s', '1960s'),
            ('1970s', '1970s'),
            ('1980s', '1980s'),
            ('1990s', '1990s'),
            ('2000s', '2000s'),
            ('2010s', '2010s'),
            ('2020s', '2020s'),
        ],
        help_text='Filter books by decade of publication'
    )
    
    has_recent_publication = filters.BooleanFilter(
        method='filter_recent_books',
        help_text='Filter books published in the last 10 years (true/false)'
    )
    
    # Multi-field search
    search = filters.CharFilter(
        method='filter_search',
        help_text='Search across title and author name'
    )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'publication_year': ['exact', 'gte', 'lte', 'gt', 'lt'],
            'author': ['exact'],
            'author__name': ['exact', 'icontains', 'istartswith'],
        }
    
    def filter_by_decade(self, queryset, name, value):
        """
        Custom filter method to filter books by decade.
        
        Args:
            queryset: The initial queryset
            name: The filter field name
            value: The decade value (e.g., '1990s')
            
        Returns:
            Filtered queryset containing books from the specified decade
        """
        if not value:
            return queryset
        
        # Extract decade start year
        decade_start = int(value[:4])
        decade_end = decade_start + 9
        
        return queryset.filter(
            publication_year__gte=decade_start,
            publication_year__lte=decade_end
        )
    
    def filter_recent_books(self, queryset, name, value):
        """
        Custom filter method to filter recent books (last 10 years).
        
        Args:
            queryset: The initial queryset
            name: The filter field name
            value: Boolean value (True for recent books)
            
        Returns:
            Filtered queryset containing recent books if value is True
        """
        if value is None:
            return queryset
        
        from datetime import datetime
        current_year = datetime.now().year
        
        if value:
            # Return books from last 10 years
            return queryset.filter(publication_year__gte=current_year - 10)
        else:
            # Return books older than 10 years
            return queryset.filter(publication_year__lt=current_year - 10)
    
    def filter_search(self, queryset, name, value):
        """
        Custom search filter across multiple fields.
        
        Searches in both title and author name fields.
        
        Args:
            queryset: The initial queryset
            name: The filter field name
            value: The search term
            
        Returns:
            Filtered queryset containing books matching the search term
        """
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) | Q(author__name__icontains=value)
        )


class AuthorFilter(filters.FilterSet):
    """
    Filter class for Author model.
    
    Provides filtering options for authors including name-based filtering
    and filtering by number of books.
    """
    
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        help_text='Filter by author name (case-insensitive partial match)'
    )
    
    name_exact = filters.CharFilter(
        field_name='name',
        lookup_expr='iexact',
        help_text='Filter by exact author name (case-insensitive)'
    )
    
    has_books = filters.BooleanFilter(
        method='filter_authors_with_books',
        help_text='Filter authors who have published books (true/false)'
    )
    
    min_books = filters.NumberFilter(
        method='filter_by_book_count',
        help_text='Filter authors with at least this many books'
    )
    
    class Meta:
        model = Author
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
    
    def filter_authors_with_books(self, queryset, name, value):
        """
        Filter authors based on whether they have published books.
        
        Args:
            queryset: The initial queryset
            name: The filter field name
            value: Boolean value
            
        Returns:
            Filtered queryset of authors with or without books
        """
        if value is None:
            return queryset
        
        if value:
            # Return authors who have at least one book
            return queryset.filter(books__isnull=False).distinct()
        else:
            # Return authors who have no books
            return queryset.filter(books__isnull=True)
    
    def filter_by_book_count(self, queryset, name, value):
        """
        Filter authors by minimum number of books.
        
        Args:
            queryset: The initial queryset
            name: The filter field name
            value: Minimum number of books
            
        Returns:
            Filtered queryset of authors with at least the specified number of books
        """
        if value is None:
            return queryset
        
        from django.db.models import Count
        
        return queryset.annotate(
            book_count=Count('books')
        ).filter(book_count__gte=value)
