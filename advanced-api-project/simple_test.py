#!/usr/bin/env python
"""
Simple test script to verify the views are working correctly.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from api.models import Author, Book

def test_basic_functionality():
    """
    Test basic functionality of the views.
    """
    print("Testing basic view functionality...")
    
    # Clear existing data
    Book.objects.all().delete()
    Author.objects.all().delete()
    User.objects.all().delete()
    
    # Create test data
    author = Author.objects.create(name="Test Author")
    book = Book.objects.create(
        title="Test Book",
        publication_year=2020,
        author=author
    )
    
    # Create test client
    client = Client()
    
    # Test API overview
    response = client.get('/api/')
    print(f"API Overview: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
    
    # Test book list
    response = client.get('/api/books/')
    print(f"Book List: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
    
    # Test book detail
    response = client.get(f'/api/books/{book.id}/')
    print(f"Book Detail: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
    
    # Test author list
    response = client.get('/api/authors/')
    print(f"Author List: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
    
    # Test author detail
    response = client.get(f'/api/authors/{author.id}/')
    print(f"Author Detail: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
    
    print("Basic functionality test completed!")

if __name__ == "__main__":
    test_basic_functionality()
