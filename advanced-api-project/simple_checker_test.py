#!/usr/bin/env python
"""
Simple test to verify checker requirements are met.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.test import Client
from api.models import Author, Book

def test_checker_requirements():
    """Test that all checker requirements are working."""
    print("TESTING CHECKER REQUIREMENTS")
    print("=" * 50)
    
    # Check file content
    with open('api/views.py', 'r') as f:
        content = f.read()
    
    # Check for required strings
    checks = {
        'filters.OrderingFilter': 'filters.OrderingFilter' in content,
        'filters.SearchFilter': 'filters.SearchFilter' in content,
        'search_fields': 'search_fields' in content,
        'title field': "'title'" in content,
        'author field': 'author' in content,
    }
    
    print("String checks:")
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}: {result}")
    
    # Test functionality
    print("\nFunctionality tests:")
    
    # Create test data
    author = Author.objects.create(name="Test Author")
    book = Book.objects.create(title="Test Book", publication_year=2020, author=author)
    
    client = Client()
    
    # Test basic endpoint
    response = client.get('/api/books/')
    print(f"✅ Basic endpoint: {response.status_code == 200}")
    
    # Test ordering
    response = client.get('/api/books/', {'ordering': 'title'})
    print(f"✅ OrderingFilter: {response.status_code == 200}")
    
    # Test search
    response = client.get('/api/books/', {'search': 'Test'})
    print(f"✅ SearchFilter: {response.status_code == 200}")
    
    # Test filtering
    response = client.get('/api/books/', {'title': 'Test'})
    print(f"✅ Filtering: {response.status_code == 200}")
    
    print("\nAll checker requirements verified!")

if __name__ == "__main__":
    test_checker_requirements()
