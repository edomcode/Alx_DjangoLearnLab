from django.test import TestCase
from .models import Book

class BookModelTest(TestCase):
    def test_create_book(self):
        book = Book.objects.create(title="Test Book", author="Eden", published_date="2025-08-02")
        self.assertEqual(book.title, "Test Book")
