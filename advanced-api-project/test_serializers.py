#!/usr/bin/env python
"""
Test script for the custom serializers.

This script demonstrates the functionality of the AuthorSerializer and BookSerializer,
including the custom validation and nested serialization features.
"""

import os
import sys
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer


def test_serializers():
    """
    Test the custom serializers with sample data.
    """
    print("=" * 60)
    print("TESTING CUSTOM SERIALIZERS")
    print("=" * 60)
    
    # Clear existing data for clean testing
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # Create test authors
    print("\n1. Creating test authors...")
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    print(f"Created: {author1}")
    print(f"Created: {author2}")
    
    # Create test books
    print("\n2. Creating test books...")
    book1 = Book.objects.create(
        title="Harry Potter and the Philosopher's Stone",
        publication_year=1997,
        author=author1
    )
    book2 = Book.objects.create(
        title="Harry Potter and the Chamber of Secrets",
        publication_year=1998,
        author=author1
    )
    book3 = Book.objects.create(
        title="1984",
        publication_year=1949,
        author=author2
    )
    book4 = Book.objects.create(
        title="Animal Farm",
        publication_year=1945,
        author=author2
    )
    
    print(f"Created: {book1}")
    print(f"Created: {book2}")
    print(f"Created: {book3}")
    print(f"Created: {book4}")
    
    # Test BookSerializer
    print("\n3. Testing BookSerializer...")
    book_serializer = BookSerializer(book1)
    print("Serialized book data:")
    print(book_serializer.data)
    
    # Test BookSerializer validation (valid year)
    print("\n4. Testing BookSerializer validation (valid year)...")
    valid_book_data = {
        'title': 'Test Book',
        'publication_year': 2020,
        'author': author1.id
    }
    book_serializer = BookSerializer(data=valid_book_data)
    if book_serializer.is_valid():
        print("✓ Valid book data passed validation")
        print(f"Validated data: {book_serializer.validated_data}")
    else:
        print("✗ Valid book data failed validation")
        print(f"Errors: {book_serializer.errors}")
    
    # Test BookSerializer validation (future year - should fail)
    print("\n5. Testing BookSerializer validation (future year)...")
    future_year = datetime.now().year + 1
    invalid_book_data = {
        'title': 'Future Book',
        'publication_year': future_year,
        'author': author1.id
    }
    book_serializer = BookSerializer(data=invalid_book_data)
    if book_serializer.is_valid():
        print("✗ Future year data incorrectly passed validation")
    else:
        print("✓ Future year data correctly failed validation")
        print(f"Validation errors: {book_serializer.errors}")
    
    # Test AuthorSerializer with nested books
    print("\n6. Testing AuthorSerializer with nested books...")
    author_serializer = AuthorSerializer(author1)
    print("Serialized author data with nested books:")
    print(author_serializer.data)
    
    # Test AuthorSerializer for author with no books
    print("\n7. Testing AuthorSerializer for author with no books...")
    author3 = Author.objects.create(name="New Author")
    author_serializer = AuthorSerializer(author3)
    print("Serialized author data (no books):")
    print(author_serializer.data)
    
    # Test multiple authors serialization
    print("\n8. Testing multiple authors serialization...")
    authors = Author.objects.all()
    authors_serializer = AuthorSerializer(authors, many=True)
    print("All authors with their books:")
    for author_data in authors_serializer.data:
        print(f"Author: {author_data['name']}")
        print(f"Books count: {author_data['books_count']}")
        print(f"Books: {[book['title'] for book in author_data['books']]}")
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("SERIALIZER TESTING COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    test_serializers()
