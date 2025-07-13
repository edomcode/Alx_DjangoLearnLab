# Retrieve Operation

```python
books = Book.objects.all()
for b in books:
    print(b.id, b.title, b.author, b.publication_year)

book = Book.objects.get(title="1984")
print(book.id, book.title, book.author, book.publication_year)
