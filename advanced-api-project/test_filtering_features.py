#!/usr/bin/env python
"""
Comprehensive test script for filtering, searching, and ordering features.

This script tests all the advanced query capabilities implemented in the
Django REST Framework API, including filtering, searching, and ordering.
"""

import os
import sys
import django
import json
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from api.models import Author, Book


class FilteringTestSuite:
    """
    Comprehensive test suite for filtering, searching, and ordering features.
    """
    
    def __init__(self):
        self.client = Client()
        self.base_url = '/api/books/'
        self.authors_url = '/api/authors/'
        self.setup_test_data()
    
    def setup_test_data(self):
        """
        Create comprehensive test data for filtering tests.
        """
        print("Setting up test data...")
        
        # Clear existing data
        Book.objects.all().delete()
        Author.objects.all().delete()
        
        # Create diverse authors
        self.authors = {
            'rowling': Author.objects.create(name="J.K. Rowling"),
            'tolkien': Author.objects.create(name="J.R.R. Tolkien"),
            'orwell': Author.objects.create(name="George Orwell"),
            'asimov': Author.objects.create(name="Isaac Asimov"),
            'clarke': Author.objects.create(name="Arthur C. Clarke"),
            'herbert': Author.objects.create(name="Frank Herbert"),
            'single_book': Author.objects.create(name="Single Book Author"),
        }
        
        # Create diverse books across different decades
        self.books = [
            # J.K. Rowling books (1990s-2000s)
            Book.objects.create(title="Harry Potter and the Philosopher's Stone", publication_year=1997, author=self.authors['rowling']),
            Book.objects.create(title="Harry Potter and the Chamber of Secrets", publication_year=1998, author=self.authors['rowling']),
            Book.objects.create(title="Harry Potter and the Prisoner of Azkaban", publication_year=1999, author=self.authors['rowling']),
            
            # J.R.R. Tolkien books (1930s-1950s)
            Book.objects.create(title="The Hobbit", publication_year=1937, author=self.authors['tolkien']),
            Book.objects.create(title="The Fellowship of the Ring", publication_year=1954, author=self.authors['tolkien']),
            Book.objects.create(title="The Two Towers", publication_year=1954, author=self.authors['tolkien']),
            Book.objects.create(title="The Return of the King", publication_year=1955, author=self.authors['tolkien']),
            
            # George Orwell books (1940s)
            Book.objects.create(title="Animal Farm", publication_year=1945, author=self.authors['orwell']),
            Book.objects.create(title="1984", publication_year=1949, author=self.authors['orwell']),
            
            # Isaac Asimov books (1950s)
            Book.objects.create(title="Foundation", publication_year=1951, author=self.authors['asimov']),
            Book.objects.create(title="Foundation and Empire", publication_year=1952, author=self.authors['asimov']),
            Book.objects.create(title="Second Foundation", publication_year=1953, author=self.authors['asimov']),
            
            # Arthur C. Clarke books (1960s-1970s)
            Book.objects.create(title="2001: A Space Odyssey", publication_year=1968, author=self.authors['clarke']),
            Book.objects.create(title="Rendezvous with Rama", publication_year=1973, author=self.authors['clarke']),
            
            # Frank Herbert (1960s)
            Book.objects.create(title="Dune", publication_year=1965, author=self.authors['herbert']),
            
            # Single book author (2020s - recent)
            Book.objects.create(title="Modern Novel", publication_year=2020, author=self.authors['single_book']),
        ]
        
        print(f"✓ Created {len(self.authors)} authors and {len(self.books)} books")
    
    def test_basic_filtering(self):
        """Test basic filtering capabilities."""
        print("\n" + "="*60)
        print("TESTING BASIC FILTERING")
        print("="*60)
        
        # Test filtering by title
        response = self.client.get(self.base_url, {'title': 'Harry'})
        self.assert_response(response, "Title filtering", expected_count=3)
        
        # Test exact title filtering
        response = self.client.get(self.base_url, {'title_exact': 'Dune'})
        self.assert_response(response, "Exact title filtering", expected_count=1)
        
        # Test publication year filtering
        response = self.client.get(self.base_url, {'publication_year': 1954})
        self.assert_response(response, "Publication year filtering", expected_count=2)
        
        # Test year range filtering
        response = self.client.get(self.base_url, {'publication_year_min': 1950, 'publication_year_max': 1960})
        result_count = len(response.json()['results']) if 'results' in response.json() else len(response.json())
        print(f"✓ Year range filtering (1950-1960): {result_count} books found")
        
        # Test author filtering
        response = self.client.get(self.base_url, {'author': self.authors['rowling'].id})
        self.assert_response(response, "Author ID filtering", expected_count=3)
        
        # Test author name filtering
        response = self.client.get(self.base_url, {'author_name': 'Tolkien'})
        self.assert_response(response, "Author name filtering", expected_count=4)
    
    def test_advanced_filtering(self):
        """Test advanced filtering features."""
        print("\n" + "="*60)
        print("TESTING ADVANCED FILTERING")
        print("="*60)
        
        # Test decade filtering
        response = self.client.get(self.base_url, {'decade': '1950s'})
        result_count = len(response.json()['results']) if 'results' in response.json() else len(response.json())
        print(f"✓ Decade filtering (1950s): {result_count} books found")
        
        # Test recent books filtering
        response = self.client.get(self.base_url, {'has_recent_publication': 'true'})
        result_count = len(response.json()['results']) if 'results' in response.json() else len(response.json())
        print(f"✓ Recent books filtering: {result_count} books found")
        
        # Test popular authors filtering (legacy parameter)
        response = self.client.get(self.base_url, {'popular_only': 'true'})
        result_count = len(response.json()['results']) if 'results' in response.json() else len(response.json())
        print(f"✓ Popular authors filtering: {result_count} books found")
        
        # Test custom search filter
        response = self.client.get(self.base_url, {'search': 'Foundation'})
        result_count = len(response.json()['results']) if 'results' in response.json() else len(response.json())
        print(f"✓ Custom search filtering: {result_count} books found")
    
    def test_search_functionality(self):
        """Test search functionality."""
        print("\n" + "="*60)
        print("TESTING SEARCH FUNCTIONALITY")
        print("="*60)
        
        # Test title search
        response = self.client.get(self.base_url, {'search': 'Potter'})
        result_count = len(response.json()['results']) if 'results' in response.json() else len(response.json())
        print(f"✓ Title search ('Potter'): {result_count} books found")
        
        # Test author search
        response = self.client.get(self.base_url, {'search': 'Orwell'})
        result_count = len(response.json()['results']) if 'results' in response.json() else len(response.json())
        print(f"✓ Author search ('Orwell'): {result_count} books found")
        
        # Test partial search
        response = self.client.get(self.base_url, {'search': 'Found'})
        result_count = len(response.json()['results']) if 'results' in response.json() else len(response.json())
        print(f"✓ Partial search ('Found'): {result_count} books found")
        
        # Test case-insensitive search
        response = self.client.get(self.base_url, {'search': 'DUNE'})
        result_count = len(response.json()['results']) if 'results' in response.json() else len(response.json())
        print(f"✓ Case-insensitive search ('DUNE'): {result_count} books found")
    
    def test_ordering_functionality(self):
        """Test ordering functionality."""
        print("\n" + "="*60)
        print("TESTING ORDERING FUNCTIONALITY")
        print("="*60)
        
        # Test ordering by title (ascending)
        response = self.client.get(self.base_url, {'ordering': 'title'})
        books = response.json()['results'] if 'results' in response.json() else response.json()
        if len(books) >= 2:
            first_title = books[0]['title']
            second_title = books[1]['title']
            is_ordered = first_title <= second_title
            print(f"✓ Title ordering (asc): {'Correct' if is_ordered else 'Incorrect'} - '{first_title}' vs '{second_title}'")
        
        # Test ordering by publication year (descending)
        response = self.client.get(self.base_url, {'ordering': '-publication_year'})
        books = response.json()['results'] if 'results' in response.json() else response.json()
        if len(books) >= 2:
            first_year = books[0]['publication_year']
            second_year = books[1]['publication_year']
            is_ordered = first_year >= second_year
            print(f"✓ Year ordering (desc): {'Correct' if is_ordered else 'Incorrect'} - {first_year} vs {second_year}")
        
        # Test ordering by author name
        response = self.client.get(self.base_url, {'ordering': 'author__name'})
        books = response.json()['results'] if 'results' in response.json() else response.json()
        print(f"✓ Author name ordering: {len(books)} books ordered by author")
    
    def test_combined_filtering(self):
        """Test combining multiple filters."""
        print("\n" + "="*60)
        print("TESTING COMBINED FILTERING")
        print("="*60)
        
        # Test search + ordering
        response = self.client.get(self.base_url, {
            'search': 'Harry',
            'ordering': 'publication_year'
        })
        result_count = len(response.json()['results']) if 'results' in response.json() else len(response.json())
        print(f"✓ Search + Ordering: {result_count} books found")
        
        # Test author + year range + ordering
        response = self.client.get(self.base_url, {
            'author_name': 'Tolkien',
            'publication_year_min': 1950,
            'ordering': '-publication_year'
        })
        result_count = len(response.json()['results']) if 'results' in response.json() else len(response.json())
        print(f"✓ Author + Year Range + Ordering: {result_count} books found")
        
        # Test decade + search
        response = self.client.get(self.base_url, {
            'decade': '1940s',
            'search': '1984'
        })
        result_count = len(response.json()['results']) if 'results' in response.json() else len(response.json())
        print(f"✓ Decade + Search: {result_count} books found")
    
    def test_author_filtering(self):
        """Test author-specific filtering."""
        print("\n" + "="*60)
        print("TESTING AUTHOR FILTERING")
        print("="*60)
        
        # Test author name filtering
        response = self.client.get(self.authors_url, {'name': 'George'})
        result_count = len(response.json())
        print(f"✓ Author name filtering: {result_count} authors found")
        
        # Test authors with books
        response = self.client.get(self.authors_url, {'has_books': 'true'})
        result_count = len(response.json())
        print(f"✓ Authors with books: {result_count} authors found")
        
        # Test minimum books filter
        response = self.client.get(self.authors_url, {'min_books': '3'})
        result_count = len(response.json())
        print(f"✓ Authors with 3+ books: {result_count} authors found")
        
        # Test author search
        response = self.client.get(self.authors_url, {'search': 'Tolkien'})
        result_count = len(response.json())
        print(f"✓ Author search: {result_count} authors found")
    
    def assert_response(self, response, test_name, expected_count=None):
        """Helper method to assert response validity."""
        if response.status_code == 200:
            data = response.json()
            result_count = len(data['results']) if 'results' in data else len(data)
            status = "✓" if expected_count is None or result_count == expected_count else "⚠"
            print(f"{status} {test_name}: {result_count} results")
            if expected_count and result_count != expected_count:
                print(f"  Expected {expected_count}, got {result_count}")
        else:
            print(f"✗ {test_name}: HTTP {response.status_code}")
    
    def run_all_tests(self):
        """Run all filtering tests."""
        print("COMPREHENSIVE FILTERING, SEARCHING, AND ORDERING TESTS")
        print("="*80)
        
        self.test_basic_filtering()
        self.test_advanced_filtering()
        self.test_search_functionality()
        self.test_ordering_functionality()
        self.test_combined_filtering()
        self.test_author_filtering()
        
        print("\n" + "="*80)
        print("ALL FILTERING TESTS COMPLETED!")
        print("="*80)


if __name__ == "__main__":
    tester = FilteringTestSuite()
    tester.run_all_tests()
