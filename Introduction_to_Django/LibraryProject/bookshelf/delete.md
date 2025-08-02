
---

## 📄 `delete.md`

```markdown
# Delete a Book instance

```python
from bookshelf.models import Book
book = Book.objects.get(title="Things Fall Apart (Updated)")
book.delete()
