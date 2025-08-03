def run_queries():
    author_name = "J.K. Rowling"
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        print(f"\nBooks by {author_name}: {[book.title for book in books]}")
    except Author.DoesNotExist:
        print(f"\nAuthor '{author_name}' not found.")

    library_name = "Central Library"
    library = None  # Initialize first
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"\nBooks in {library_name}: {[book.title for book in books_in_library]}")
    except Library.DoesNotExist:
        print(f"\nLibrary '{library_name}' not found.")

    if library:
        try:
            librarian = library.librarian
            print(f"\nLibrarian at {library.name}: {librarian.name}")
        except Librarian.DoesNotExist:
            print(f"\nNo librarian assigned to {library.name}.")
import os
import sys
import django

# Add the base directory to Python's path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    author_name = "J.K. Rowling"
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        print(f"\nBooks by {author_name}: {[book.title for book in books]}")
    except Author.DoesNotExist:
        print(f"\nAuthor '{author_name}' not found.")

    library_name = "Central Library"
    library = None
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"\nBooks in {library_name}: {[book.title for book in books_in_library]}")
    except Library.DoesNotExist:
        print(f"\nLibrary '{library_name}' not found.")

    if library:
        try:
            librarian = library.librarian
            print(f"\nLibrarian at {library.name}: {librarian.name}")
        except Librarian.DoesNotExist:
            print(f"\nNo librarian assigned to {library.name}.")

if __name__ == "__main__":
    run_queries()
