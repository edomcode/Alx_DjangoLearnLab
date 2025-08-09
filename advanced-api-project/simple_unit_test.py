#!/usr/bin/env python
"""
Simple unit test to verify the test framework is working.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Author, Book
from api.serializers import BookSerializer

class SimpleTestCase(TestCase):
    """Simple test case to verify basic functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
        self.client = APIClient()
    
    def test_author_creation(self):
        """Test that authors can be created."""
        author = Author.objects.create(name="New Author")
        self.assertEqual(author.name, "New Author")
        self.assertTrue(Author.objects.filter(name="New Author").exists())
    
    def test_book_creation(self):
        """Test that books can be created."""
        book = Book.objects.create(
            title="New Book",
            publication_year=2023,
            author=self.author
        )
        self.assertEqual(book.title, "New Book")
        self.assertEqual(book.author, self.author)
    
    def test_book_serializer(self):
        """Test BookSerializer functionality."""
        serializer = BookSerializer(self.book)
        data = serializer.data
        
        self.assertEqual(data['title'], "Test Book")
        self.assertEqual(data['publication_year'], 2020)
        self.assertEqual(data['author'], self.author.id)
    
    def test_api_overview_endpoint(self):
        """Test API overview endpoint."""
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_book_list_endpoint(self):
        """Test book list endpoint."""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

def run_simple_tests():
    """Run the simple tests."""
    import unittest
    
    print("Running simple unit tests...")
    print("=" * 40)
    
    # Create test suite
    suite = unittest.TestSuite()
    suite.addTest(SimpleTestCase('test_author_creation'))
    suite.addTest(SimpleTestCase('test_book_creation'))
    suite.addTest(SimpleTestCase('test_book_serializer'))
    suite.addTest(SimpleTestCase('test_api_overview_endpoint'))
    suite.addTest(SimpleTestCase('test_book_list_endpoint'))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 40)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ All simple tests passed!")
    else:
        print("❌ Some tests failed.")
        if result.failures:
            for test, traceback in result.failures:
                print(f"FAILURE: {test}")
                print(traceback)
        if result.errors:
            for test, traceback in result.errors:
                print(f"ERROR: {test}")
                print(traceback)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_simple_tests()
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")
