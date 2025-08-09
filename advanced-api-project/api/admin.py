from django.contrib import admin
from .models import Author, Book

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Author model.

    Provides a clean interface for managing authors in the Django admin.
    """
    list_display = ['name', 'books_count']
    search_fields = ['name']
    ordering = ['name']

    def books_count(self, obj):
        """Display the number of books by this author"""
        return obj.books.count()
    books_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.

    Provides a comprehensive interface for managing books in the Django admin.
    """
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    ordering = ['-publication_year', 'title']

    # Group fields in the form
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'publication_year')
        }),
        ('Author Information', {
            'fields': ('author',)
        }),
    )
