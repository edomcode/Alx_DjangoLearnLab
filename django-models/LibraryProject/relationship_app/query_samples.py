import django
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_config.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def query_all_books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return None


def list_all_books_in_library(library_name):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return None


def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


# Sample usage (uncomment to test)
if __name__ == "__main__":
    # Example usage:
    # books_by_author = query_all_books_by_author("J.K. Rowling")
    # books_in_library = list_all_books_in_library("Central Library")
    # librarian = retrieve_librarian_for_library("Central Library")
    
    print("Query functions are ready to use!")
    print("Available functions:")
    print("1. query_all_books_by_author(author_name)")
    print("2. list_all_books_in_library(library_name)")
    print("3. retrieve_librarian_for_library(library_name)")
