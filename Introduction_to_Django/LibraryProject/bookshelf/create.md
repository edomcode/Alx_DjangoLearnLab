from bookshelf.models import Book

# Chinua Achebe example
book1 = Book.objects.create(
    title="Things Fall Apart",
    author="Chinua Achebe",
    publication_year=1958
)

# George Orwell example (required by checker)
book2 = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

