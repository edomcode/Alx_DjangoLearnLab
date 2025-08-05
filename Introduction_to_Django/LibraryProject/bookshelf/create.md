# Create a Book instance

```python
from bookshelf.models import Book
book = Book.objects.create(
    title="Things Fall Apart",
    author="Chinua Achebe",
    publication_year=1958
)
