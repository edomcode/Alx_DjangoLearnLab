#!/usr/bin/env python
"""
Comprehensive test script for Django REST Framework views.

This script tests all the custom views and generic views implemented
in the advanced_api_project, including CRUD operations and permissions.
"""

import os
import sys
import django
import json
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from api.models import Author, Book


class ViewTester:
    """
    Test class for comprehensive view testing.
    """
    
    def __init__(self):
        self.client = APIClient()
        self.base_url = 'http://127.0.0.1:8000/api'
        self.setup_test_data()
    
    def setup_test_data(self):
        """
        Set up test data including users, authors, and books.
        """
        print("Setting up test data...")
        
        # Clear existing data
        Book.objects.all().delete()
        Author.objects.all().delete()
        User.objects.all().delete()
        
        # Create test user
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author2
        )
        
        print("✓ Test data created successfully")
    
    def test_unauthenticated_access(self):
        """
        Test access to endpoints without authentication.
        """
        print("\n" + "="*60)
        print("TESTING UNAUTHENTICATED ACCESS")
        print("="*60)
        
        # Test API overview (should work)
        response = self.client.get('/api/')
        print(f"API Overview: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
        
        # Test book list (should work)
        response = self.client.get('/api/books/')
        print(f"Book List: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
        
        # Test book detail (should work)
        response = self.client.get(f'/api/books/{self.book1.id}/')
        print(f"Book Detail: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
        
        # Test book create (should fail - 401)
        book_data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', book_data)
        print(f"Book Create (no auth): {response.status_code} - {'✓' if response.status_code == 401 else '✗'}")
        
        # Test book update (should fail - 401)
        response = self.client.put(f'/api/books/{self.book1.id}/update/', book_data)
        print(f"Book Update (no auth): {response.status_code} - {'✓' if response.status_code == 401 else '✗'}")
        
        # Test book delete (should fail - 401)
        response = self.client.delete(f'/api/books/{self.book1.id}/delete/')
        print(f"Book Delete (no auth): {response.status_code} - {'✓' if response.status_code == 401 else '✗'}")
    
    def test_authenticated_access(self):
        """
        Test access to endpoints with authentication.
        """
        print("\n" + "="*60)
        print("TESTING AUTHENTICATED ACCESS")
        print("="*60)
        
        # Authenticate the client
        self.client.force_authenticate(user=self.test_user)
        
        # Test book create (should work)
        book_data = {
            'title': 'Authenticated Test Book',
            'publication_year': 2021,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', book_data)
        print(f"Book Create (authenticated): {response.status_code} - {'✓' if response.status_code == 201 else '✗'}")
        
        if response.status_code == 201:
            created_book_id = response.data['book']['id']
            
            # Test book update (should work)
            update_data = {
                'title': 'Updated Test Book',
                'publication_year': 2022,
                'author': self.author2.id
            }
            response = self.client.put(f'/api/books/{created_book_id}/update/', update_data)
            print(f"Book Update (authenticated): {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
            
            # Test book delete (should work)
            response = self.client.delete(f'/api/books/{created_book_id}/delete/')
            print(f"Book Delete (authenticated): {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
    
    def test_validation(self):
        """
        Test custom validation in serializers.
        """
        print("\n" + "="*60)
        print("TESTING VALIDATION")
        print("="*60)
        
        # Authenticate the client
        self.client.force_authenticate(user=self.test_user)
        
        # Test future year validation (should fail)
        future_year = datetime.now().year + 1
        invalid_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', invalid_data)
        print(f"Future year validation: {response.status_code} - {'✓' if response.status_code == 400 else '✗'}")
        
        if response.status_code == 400:
            print(f"  Error message: {response.data}")
    
    def test_filtering_and_search(self):
        """
        Test filtering and search functionality.
        """
        print("\n" + "="*60)
        print("TESTING FILTERING AND SEARCH")
        print("="*60)
        
        # Test filtering by author
        response = self.client.get(f'/api/books/?author={self.author1.id}')
        print(f"Filter by author: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
        if response.status_code == 200:
            print(f"  Found {len(response.data)} books by {self.author1.name}")
        
        # Test filtering by publication year
        response = self.client.get('/api/books/?publication_year=1997')
        print(f"Filter by year: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
        if response.status_code == 200:
            print(f"  Found {len(response.data)} books from 1997")
        
        # Test search by title
        response = self.client.get('/api/books/?search=Harry')
        print(f"Search by title: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
        if response.status_code == 200:
            print(f"  Found {len(response.data)} books matching 'Harry'")
        
        # Test year range filtering
        response = self.client.get('/api/books/?year_from=1990&year_to=2000')
        print(f"Year range filter: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
        if response.status_code == 200:
            print(f"  Found {len(response.data)} books from 1990-2000")
    
    def test_author_endpoints(self):
        """
        Test author-related endpoints.
        """
        print("\n" + "="*60)
        print("TESTING AUTHOR ENDPOINTS")
        print("="*60)
        
        # Test author list
        response = self.client.get('/api/authors/')
        print(f"Author List: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
        if response.status_code == 200:
            print(f"  Found {len(response.data)} authors")
        
        # Test author detail with nested books
        response = self.client.get(f'/api/authors/{self.author1.id}/')
        print(f"Author Detail: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
        if response.status_code == 200:
            print(f"  Author: {response.data['name']}")
            print(f"  Books count: {response.data['books_count']}")
        
        # Test author filtering by name
        response = self.client.get('/api/authors/?name=Rowling')
        print(f"Author name filter: {response.status_code} - {'✓' if response.status_code == 200 else '✗'}")
        if response.status_code == 200:
            print(f"  Found {len(response.data)} authors matching 'Rowling'")
    
    def run_all_tests(self):
        """
        Run all test methods.
        """
        print("STARTING COMPREHENSIVE VIEW TESTING")
        print("="*60)
        
        self.test_unauthenticated_access()
        self.test_authenticated_access()
        self.test_validation()
        self.test_filtering_and_search()
        self.test_author_endpoints()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED!")
        print("="*60)


if __name__ == "__main__":
    tester = ViewTester()
    tester.run_all_tests()
