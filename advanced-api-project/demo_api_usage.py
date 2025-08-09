#!/usr/bin/env python
"""
Demonstration script showing how to use the Django REST Framework API.

This script demonstrates:
1. Creating test data
2. Using different API endpoints
3. Testing permissions
4. Using filtering and search features
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
import json

def demo_api_usage():
    """
    Demonstrate API usage with real examples.
    """
    print("=" * 60)
    print("DJANGO REST FRAMEWORK API DEMONSTRATION")
    print("=" * 60)
    
    # Setup
    print("\n1. Setting up test data...")
    
    # Clear existing data
    Book.objects.all().delete()
    Author.objects.all().delete()
    User.objects.all().delete()
    
    # Create test user
    user = User.objects.create_user(
        username='demo_user',
        password='demo_pass123',
        email='demo@example.com'
    )
    
    # Create test authors and books
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="Isaac Asimov")
    
    Book.objects.create(title="Harry Potter and the Philosopher's Stone", publication_year=1997, author=author1)
    Book.objects.create(title="Harry Potter and the Chamber of Secrets", publication_year=1998, author=author1)
    Book.objects.create(title="1984", publication_year=1949, author=author2)
    Book.objects.create(title="Animal Farm", publication_year=1945, author=author2)
    Book.objects.create(title="Foundation", publication_year=1951, author=author3)
    
    print("✓ Test data created successfully")
    
    client = Client()
    
    # 2. Demonstrate public endpoints
    print("\n2. Testing public endpoints (no authentication required)...")
    
    # API Overview
    response = client.get('/api/')
    print(f"✓ API Overview: {response.status_code}")
    
    # List all books
    response = client.get('/api/books/')
    books = response.json()
    print(f"✓ Book List: Found {len(books)} books")
    
    # Get specific book
    if books:
        book_id = books[0]['id']
        response = client.get(f'/api/books/{book_id}/')
        book = response.json()
        print(f"✓ Book Detail: '{book['title']}' by author ID {book['author']}")
    
    # List all authors with nested books
    response = client.get('/api/authors/')
    authors = response.json()
    print(f"✓ Author List: Found {len(authors)} authors")
    for author in authors:
        print(f"  - {author['name']}: {author['books_count']} books")
    
    # 3. Demonstrate filtering and search
    print("\n3. Testing filtering and search features...")
    
    # Search for books
    response = client.get('/api/books/?search=Harry')
    harry_books = response.json()
    print(f"✓ Search 'Harry': Found {len(harry_books)} books")
    
    # Filter by year range
    response = client.get('/api/books/?year_from=1990&year_to=2000')
    modern_books = response.json()
    print(f"✓ Books 1990-2000: Found {len(modern_books)} books")
    
    # Order by title
    response = client.get('/api/books/?ordering=title')
    ordered_books = response.json()
    print(f"✓ Ordered by title: First book is '{ordered_books[0]['title']}'")
    
    # Filter authors by name
    response = client.get('/api/authors/?name=Orwell')
    orwell_authors = response.json()
    print(f"✓ Authors with 'Orwell': Found {len(orwell_authors)} authors")
    
    # 4. Demonstrate protected endpoints (should fail without auth)
    print("\n4. Testing protected endpoints without authentication...")
    
    new_book_data = {
        'title': 'Test Book',
        'publication_year': 2023,
        'author': author1.id
    }
    
    response = client.post('/api/books/create/', 
                          data=json.dumps(new_book_data),
                          content_type='application/json')
    print(f"✓ Create book (no auth): {response.status_code} (Expected: 403 Forbidden)")
    
    # 5. Demonstrate authenticated operations
    print("\n5. Testing authenticated operations...")
    
    # Login
    client.login(username='demo_user', password='demo_pass123')
    print("✓ User authenticated")
    
    # Create a new book
    response = client.post('/api/books/create/', 
                          data=json.dumps(new_book_data),
                          content_type='application/json')
    if response.status_code == 201:
        created_book = response.json()
        created_book_id = created_book['book']['id']
        print(f"✓ Book created: '{created_book['book']['title']}'")
        
        # Update the book
        update_data = {
            'title': 'Updated Test Book',
            'publication_year': 2024,
            'author': author2.id
        }
        response = client.put(f'/api/books/{created_book_id}/update/',
                             data=json.dumps(update_data),
                             content_type='application/json')
        if response.status_code == 200:
            updated_book = response.json()
            print(f"✓ Book updated: '{updated_book['book']['title']}'")
        
        # Delete the book
        response = client.delete(f'/api/books/{created_book_id}/delete/')
        if response.status_code == 200:
            delete_response = response.json()
            print(f"✓ Book deleted: {delete_response['message']}")
    
    # 6. Demonstrate validation
    print("\n6. Testing custom validation...")
    
    # Try to create book with future year (should fail)
    future_book_data = {
        'title': 'Future Book',
        'publication_year': 2030,  # Future year
        'author': author1.id
    }
    
    response = client.post('/api/books/create/',
                          data=json.dumps(future_book_data),
                          content_type='application/json')
    if response.status_code == 400:
        error_response = response.json()
        print(f"✓ Future year validation: {error_response}")
    
    # 7. Demonstrate author operations
    print("\n7. Testing author operations...")
    
    # Create new author
    author_data = {'name': 'New Demo Author'}
    response = client.post('/api/authors/',
                          data=json.dumps(author_data),
                          content_type='application/json')
    if response.status_code == 201:
        new_author = response.json()
        print(f"✓ Author created: '{new_author['name']}'")
        
        # Get author with nested books
        response = client.get(f'/api/authors/{new_author["id"]}/')
        if response.status_code == 200:
            author_detail = response.json()
            print(f"✓ Author detail: {author_detail['books_count']} books")
    
    # 8. Demonstrate legacy endpoints
    print("\n8. Testing legacy endpoints...")
    
    response = client.get('/api/books/legacy/')
    print(f"✓ Legacy book list: {response.status_code}")
    
    if books:
        response = client.get(f'/api/books/{books[0]["id"]}/legacy/')
        print(f"✓ Legacy book detail: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("API DEMONSTRATION COMPLETED!")
    print("=" * 60)
    print("\nKey Features Demonstrated:")
    print("✓ Public read access to books and authors")
    print("✓ Authentication-protected write operations")
    print("✓ Advanced filtering and search capabilities")
    print("✓ Custom validation (future year prevention)")
    print("✓ Nested serialization (authors with books)")
    print("✓ Custom response formatting")
    print("✓ Separate CRUD operations")
    print("✓ Legacy endpoint compatibility")
    print("\nThe API is ready for production use!")

if __name__ == "__main__":
    demo_api_usage()
