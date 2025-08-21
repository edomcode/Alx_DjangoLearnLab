#!/usr/bin/env python
"""
Practical demonstration of filtering, searching, and ordering features.

This script provides real-world examples of how to use the advanced
query capabilities in the Django REST Framework API.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.test import Client
from api.models import Author, Book


def setup_demo_data():
    """Create realistic demo data for filtering demonstration."""
    print("Setting up demo data...")
    
    # Clear existing data
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # Create authors
    authors = {
        'rowling': Author.objects.create(name="J.K. Rowling"),
        'tolkien': Author.objects.create(name="J.R.R. Tolkien"),
        'martin': Author.objects.create(name="George R.R. Martin"),
        'sanderson': Author.objects.create(name="Brandon Sanderson"),
        'pratchett': Author.objects.create(name="Terry Pratchett"),
        'gaiman': Author.objects.create(name="Neil Gaiman"),
    }
    
    # Create books
    books = [
        # J.K. Rowling - Harry Potter series
        Book.objects.create(title="Harry Potter and the Philosopher's Stone", publication_year=1997, author=authors['rowling']),
        Book.objects.create(title="Harry Potter and the Chamber of Secrets", publication_year=1998, author=authors['rowling']),
        Book.objects.create(title="Harry Potter and the Prisoner of Azkaban", publication_year=1999, author=authors['rowling']),
        Book.objects.create(title="Harry Potter and the Goblet of Fire", publication_year=2000, author=authors['rowling']),
        
        # J.R.R. Tolkien - Middle-earth
        Book.objects.create(title="The Hobbit", publication_year=1937, author=authors['tolkien']),
        Book.objects.create(title="The Fellowship of the Ring", publication_year=1954, author=authors['tolkien']),
        Book.objects.create(title="The Two Towers", publication_year=1954, author=authors['tolkien']),
        Book.objects.create(title="The Return of the King", publication_year=1955, author=authors['tolkien']),
        
        # George R.R. Martin - A Song of Ice and Fire
        Book.objects.create(title="A Game of Thrones", publication_year=1996, author=authors['martin']),
        Book.objects.create(title="A Clash of Kings", publication_year=1998, author=authors['martin']),
        Book.objects.create(title="A Storm of Swords", publication_year=2000, author=authors['martin']),
        
        # Brandon Sanderson - Cosmere
        Book.objects.create(title="The Way of Kings", publication_year=2010, author=authors['sanderson']),
        Book.objects.create(title="Words of Radiance", publication_year=2014, author=authors['sanderson']),
        Book.objects.create(title="Oathbringer", publication_year=2017, author=authors['sanderson']),
        
        # Terry Pratchett - Discworld
        Book.objects.create(title="The Colour of Magic", publication_year=1983, author=authors['pratchett']),
        Book.objects.create(title="The Light Fantastic", publication_year=1986, author=authors['pratchett']),
        
        # Neil Gaiman
        Book.objects.create(title="Good Omens", publication_year=1990, author=authors['gaiman']),
        Book.objects.create(title="American Gods", publication_year=2001, author=authors['gaiman']),
    ]
    
    print(f"✓ Created {len(authors)} authors and {len(books)} books")
    return authors, books


def demonstrate_filtering():
    """Demonstrate various filtering capabilities."""
    client = Client()
    
    print("\n" + "="*80)
    print("FILTERING DEMONSTRATION")
    print("="*80)
    
    # Example 1: Find all Harry Potter books
    print("\n1. Finding all Harry Potter books:")
    print("   Query: /api/books/?title=Harry")
    response = client.get('/api/books/', {'title': 'Harry'})
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   Found {len(books)} books:")
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']})")
    
    # Example 2: Find books published in the 1990s
    print("\n2. Finding books from the 1990s:")
    print("   Query: /api/books/?decade=1990s")
    response = client.get('/api/books/', {'decade': '1990s'})
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   Found {len(books)} books:")
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']})")
    
    # Example 3: Find recent books (last 10 years)
    print("\n3. Finding recent books (last 10 years):")
    print("   Query: /api/books/?has_recent_publication=true")
    response = client.get('/api/books/', {'has_recent_publication': 'true'})
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   Found {len(books)} books:")
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']})")
    
    # Example 4: Find books by Tolkien published after 1950
    print("\n4. Finding Tolkien books published after 1950:")
    print("   Query: /api/books/?author_name=Tolkien&publication_year_min=1950")
    response = client.get('/api/books/', {
        'author_name': 'Tolkien',
        'publication_year_min': 1950
    })
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   Found {len(books)} books:")
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']})")


def demonstrate_searching():
    """Demonstrate search capabilities."""
    client = Client()
    
    print("\n" + "="*80)
    print("SEARCH DEMONSTRATION")
    print("="*80)
    
    # Example 1: Search for "King" in titles and author names
    print("\n1. Searching for 'King' across titles and authors:")
    print("   Query: /api/books/?search=King")
    response = client.get('/api/books/', {'search': 'King'})
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   Found {len(books)} books:")
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']})")
    
    # Example 2: Search for "Magic"
    print("\n2. Searching for 'Magic':")
    print("   Query: /api/books/?search=Magic")
    response = client.get('/api/books/', {'search': 'Magic'})
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   Found {len(books)} books:")
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']})")
    
    # Example 3: Case-insensitive search
    print("\n3. Case-insensitive search for 'GAME':")
    print("   Query: /api/books/?search=GAME")
    response = client.get('/api/books/', {'search': 'GAME'})
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   Found {len(books)} books:")
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']})")


def demonstrate_ordering():
    """Demonstrate ordering capabilities."""
    client = Client()
    
    print("\n" + "="*80)
    print("ORDERING DEMONSTRATION")
    print("="*80)
    
    # Example 1: Order by title (alphabetical)
    print("\n1. Books ordered alphabetically by title:")
    print("   Query: /api/books/?ordering=title")
    response = client.get('/api/books/', {'ordering': 'title'})
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   First 5 books:")
    for book in books[:5]:
        print(f"   - {book['title']}")
    
    # Example 2: Order by publication year (newest first)
    print("\n2. Books ordered by publication year (newest first):")
    print("   Query: /api/books/?ordering=-publication_year")
    response = client.get('/api/books/', {'ordering': '-publication_year'})
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   First 5 books:")
    for book in books[:5]:
        print(f"   - {book['title']} ({book['publication_year']})")
    
    # Example 3: Order by author name
    print("\n3. Books ordered by author name:")
    print("   Query: /api/books/?ordering=author__name")
    response = client.get('/api/books/', {'ordering': 'author__name'})
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   First 5 books:")
    for book in books[:5]:
        print(f"   - {book['title']} (by author ID: {book['author']})")


def demonstrate_combined_queries():
    """Demonstrate combining filters, search, and ordering."""
    client = Client()
    
    print("\n" + "="*80)
    print("COMBINED QUERIES DEMONSTRATION")
    print("="*80)
    
    # Example 1: Search + Filter + Order
    print("\n1. Fantasy books from 1990s, ordered by year:")
    print("   Query: /api/books/?search=fantasy&decade=1990s&ordering=publication_year")
    response = client.get('/api/books/', {
        'search': 'fantasy',
        'decade': '1990s',
        'ordering': 'publication_year'
    })
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   Found {len(books)} books:")
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']})")
    
    # Example 2: Author + Year Range + Order
    print("\n2. Rowling books from 1995-2005, ordered by title:")
    print("   Query: /api/books/?author_name=Rowling&publication_year_min=1995&publication_year_max=2005&ordering=title")
    response = client.get('/api/books/', {
        'author_name': 'Rowling',
        'publication_year_min': 1995,
        'publication_year_max': 2005,
        'ordering': 'title'
    })
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   Found {len(books)} books:")
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']})")
    
    # Example 3: Complex query with multiple filters
    print("\n3. Books with 'The' in title, published after 1980, ordered by year:")
    print("   Query: /api/books/?title=The&publication_year_min=1980&ordering=-publication_year")
    response = client.get('/api/books/', {
        'title': 'The',
        'publication_year_min': 1980,
        'ordering': '-publication_year'
    })
    books = response.json()['results'] if 'results' in response.json() else response.json()
    print(f"   Found {len(books)} books:")
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']})")


def demonstrate_author_filtering():
    """Demonstrate author-specific filtering."""
    client = Client()
    
    print("\n" + "="*80)
    print("AUTHOR FILTERING DEMONSTRATION")
    print("="*80)
    
    # Example 1: Authors with books
    print("\n1. Authors who have published books:")
    print("   Query: /api/authors/?has_books=true")
    response = client.get('/api/authors/', {'has_books': 'true'})
    authors = response.json()
    print(f"   Found {len(authors)} authors:")
    for author in authors:
        print(f"   - {author['name']} ({author['books_count']} books)")
    
    # Example 2: Prolific authors (3+ books)
    print("\n2. Authors with 3 or more books:")
    print("   Query: /api/authors/?min_books=3")
    response = client.get('/api/authors/', {'min_books': '3'})
    authors = response.json()
    print(f"   Found {len(authors)} authors:")
    for author in authors:
        print(f"   - {author['name']} ({author['books_count']} books)")
    
    # Example 3: Search authors by name
    print("\n3. Search for authors with 'George' in name:")
    print("   Query: /api/authors/?search=George")
    response = client.get('/api/authors/', {'search': 'George'})
    authors = response.json()
    print(f"   Found {len(authors)} authors:")
    for author in authors:
        print(f"   - {author['name']} ({author['books_count']} books)")


def main():
    """Run the complete filtering demonstration."""
    print("DJANGO REST FRAMEWORK FILTERING DEMONSTRATION")
    print("="*80)
    
    # Setup demo data
    setup_demo_data()
    
    # Run demonstrations
    demonstrate_filtering()
    demonstrate_searching()
    demonstrate_ordering()
    demonstrate_combined_queries()
    demonstrate_author_filtering()
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETED!")
    print("="*80)
    print("\nKey Features Demonstrated:")
    print("✓ Advanced filtering by multiple fields")
    print("✓ Full-text search across title and author")
    print("✓ Flexible ordering options")
    print("✓ Combined query capabilities")
    print("✓ Author-specific filtering")
    print("✓ Legacy parameter support")
    print("\nThe API now provides powerful tools for data access and manipulation!")


if __name__ == "__main__":
    main()
