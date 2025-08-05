book = Book.objects.get(id=1)
book.title = "Advanced Django"
book.save()
