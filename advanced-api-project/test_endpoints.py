#!/usr/bin/env python
"""
Test the API endpoints to ensure they're working correctly.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from api.models import Author, Book

def test_endpoints():
    """Test all API endpoints"""
    print("Testing API endpoints...")
    
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
    
    # Create test user
    user = User.objects.create_user(
        username='testuser',
        password='testpass123'
    )
    
    client = Client()
    
    print("\n=== Testing Public Endpoints (No Authentication) ===")
    
    # Test API overview
    response = client.get('/api/')
    print(f"API Overview: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
    
    # Test book list
    response = client.get('/api/books/')
    print(f"Book List: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
    if response.status_code == 200:
        print(f"  Found {len(response.json())} books")
    
    # Test book detail
    response = client.get(f'/api/books/{book.id}/')
    print(f"Book Detail: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
    
    # Test author list
    response = client.get('/api/authors/')
    print(f"Author List: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
    if response.status_code == 200:
        print(f"  Found {len(response.json())} authors")
    
    # Test author detail
    response = client.get(f'/api/authors/{author.id}/')
    print(f"Author Detail: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
    
    print("\n=== Testing Protected Endpoints (Should Fail Without Auth) ===")
    
    # Test book create (should fail)
    book_data = {
        'title': 'New Book',
        'publication_year': 2023,
        'author': author.id
    }
    response = client.post('/api/books/create/', book_data, content_type='application/json')
    print(f"Book Create (no auth): {response.status_code} {'✓' if response.status_code == 401 else '✗'}")
    
    # Test book update (should fail)
    response = client.put(f'/api/books/{book.id}/update/', book_data, content_type='application/json')
    print(f"Book Update (no auth): {response.status_code} {'✓' if response.status_code == 401 else '✗'}")
    
    # Test book delete (should fail)
    response = client.delete(f'/api/books/{book.id}/delete/')
    print(f"Book Delete (no auth): {response.status_code} {'✓' if response.status_code == 401 else '✗'}")
    
    print("\n=== Testing Protected Endpoints (With Authentication) ===")
    
    # Login the client
    client.login(username='testuser', password='testpass123')
    
    # Test book create (should work)
    response = client.post('/api/books/create/', book_data, content_type='application/json')
    print(f"Book Create (authenticated): {response.status_code} {'✓' if response.status_code == 201 else '✗'}")
    
    if response.status_code == 201:
        created_book_id = response.json()['book']['id']
        
        # Test book update (should work)
        update_data = {
            'title': 'Updated Book',
            'publication_year': 2024,
            'author': author.id
        }
        response = client.put(f'/api/books/{created_book_id}/update/', update_data, content_type='application/json')
        print(f"Book Update (authenticated): {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
        
        # Test book delete (should work)
        response = client.delete(f'/api/books/{created_book_id}/delete/')
        print(f"Book Delete (authenticated): {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
    
    print("\n=== Testing Search and Filtering ===")
    
    # Test search
    response = client.get('/api/books/?search=Test')
    print(f"Search functionality: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
    
    # Test ordering
    response = client.get('/api/books/?ordering=title')
    print(f"Ordering functionality: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
    
    print("\n=== Testing Legacy Endpoints ===")
    
    # Test legacy book list/create
    response = client.get('/api/books/legacy/')
    print(f"Legacy Book List: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
    
    # Test legacy book detail
    response = client.get(f'/api/books/{book.id}/legacy/')
    print(f"Legacy Book Detail: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
    
    print("\n=== All Tests Completed! ===")

if __name__ == "__main__":
    test_endpoints()
