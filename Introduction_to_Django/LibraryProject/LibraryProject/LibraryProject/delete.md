# Import the Book model
from bookshelf.models import Book

# Create a book instance again (if not already existing)
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Delete the book instance
book.delete()

# Output:
# (1, {'bookshelf.Book': 1})  # Indicates 1 object of model 'bookshelf.Book' was deleted

# Confirm deletion by checking all books
print(Book.objects.all())

# Output:
# <QuerySet []>  # Confirms no books exist in the database
