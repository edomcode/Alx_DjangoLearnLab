#!/usr/bin/env python
"""
Verification script to check if all requirements are met.

This script verifies:
1. URL patterns contain required strings
2. Permission classes are properly applied
3. URLs are included in the main project
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

def check_url_patterns():
    """Check if URL patterns contain required strings."""
    print("Checking URL patterns...")
    
    # Read api/urls.py
    with open('api/urls.py', 'r') as f:
        urls_content = f.read()
    
    # Check for required patterns
    required_patterns = ['books/update', 'books/delete']
    
    for pattern in required_patterns:
        if pattern in urls_content:
            print(f"✓ Found URL pattern: {pattern}")
        else:
            print(f"✗ Missing URL pattern: {pattern}")
    
    # Show actual patterns found
    print("\nActual URL patterns found:")
    lines = urls_content.split('\n')
    for line in lines:
        if 'path(' in line and ('books/' in line or 'authors/' in line):
            print(f"  {line.strip()}")

def check_permission_classes():
    """Check if permission classes are properly applied."""
    print("\nChecking permission classes...")
    
    # Read api/views.py
    with open('api/views.py', 'r') as f:
        views_content = f.read()
    
    # Check for permission class usage
    permission_patterns = [
        'IsAuthenticated',
        'IsAuthenticatedOrReadOnly',
        'permission_classes'
    ]
    
    for pattern in permission_patterns:
        count = views_content.count(pattern)
        print(f"✓ Found '{pattern}': {count} times")
    
    # Check specific views have permissions
    view_classes = [
        'BookCreateView',
        'BookUpdateView', 
        'BookDeleteView',
        'AuthorListCreateView',
        'AuthorDetailView'
    ]
    
    print("\nPermission classes by view:")
    for view_class in view_classes:
        if view_class in views_content:
            # Find the permission_classes line for this view
            view_start = views_content.find(f'class {view_class}')
            if view_start != -1:
                # Find the next class or end of file
                next_class = views_content.find('class ', view_start + 1)
                if next_class == -1:
                    view_section = views_content[view_start:]
                else:
                    view_section = views_content[view_start:next_class]
                
                if 'permission_classes' in view_section:
                    # Extract the permission classes line
                    lines = view_section.split('\n')
                    for line in lines:
                        if 'permission_classes' in line:
                            print(f"  {view_class}: {line.strip()}")
                            break
                else:
                    print(f"  {view_class}: No permission_classes found")

def check_main_urls():
    """Check if URLs are included in main project."""
    print("\nChecking main project URLs...")
    
    # Read advanced_api_project/urls.py
    with open('advanced_api_project/urls.py', 'r') as f:
        main_urls_content = f.read()
    
    if "include('api.urls')" in main_urls_content:
        print("✓ API URLs are included in main project")
    else:
        print("✗ API URLs are NOT included in main project")
    
    if "path('api/', include('api.urls'))" in main_urls_content:
        print("✓ API URLs are mapped to 'api/' path")
    else:
        print("✗ API URLs are NOT mapped to 'api/' path")

def test_endpoints():
    """Test that endpoints are accessible."""
    print("\nTesting endpoint accessibility...")
    
    from django.test import Client
    from django.contrib.auth.models import User
    from api.models import Author, Book
    
    # Clear and create test data
    Book.objects.all().delete()
    Author.objects.all().delete()
    User.objects.all().delete()
    
    author = Author.objects.create(name="Test Author")
    book = Book.objects.create(title="Test Book", publication_year=2020, author=author)
    user = User.objects.create_user(username='testuser', password='testpass')
    
    client = Client()
    
    # Test public endpoints
    endpoints_to_test = [
        ('/api/', 'GET', False),  # API overview
        ('/api/books/', 'GET', False),  # Book list
        (f'/api/books/{book.id}/', 'GET', False),  # Book detail
        ('/api/authors/', 'GET', False),  # Author list
        (f'/api/authors/{author.id}/', 'GET', False),  # Author detail
        ('/api/books/create/', 'POST', True),  # Book create (requires auth)
        (f'/api/books/{book.id}/update/', 'PUT', True),  # Book update (requires auth)
        (f'/api/books/{book.id}/delete/', 'DELETE', True),  # Book delete (requires auth)
    ]
    
    for endpoint, method, requires_auth in endpoints_to_test:
        try:
            if method == 'GET':
                response = client.get(endpoint)
            elif method == 'POST':
                response = client.post(endpoint, {'title': 'Test', 'publication_year': 2023, 'author': author.id})
            elif method == 'PUT':
                response = client.put(endpoint, {'title': 'Test', 'publication_year': 2023, 'author': author.id})
            elif method == 'DELETE':
                response = client.delete(endpoint)
            
            if requires_auth:
                expected_status = 403  # Forbidden without auth
                status_ok = response.status_code == expected_status
            else:
                expected_status = 200  # OK for public endpoints
                status_ok = response.status_code == expected_status
            
            status_symbol = "✓" if status_ok else "✗"
            print(f"  {status_symbol} {method} {endpoint}: {response.status_code} (expected: {expected_status})")
            
        except Exception as e:
            print(f"  ✗ {method} {endpoint}: Error - {e}")

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("REQUIREMENTS VERIFICATION")
    print("=" * 60)
    
    check_url_patterns()
    check_permission_classes()
    check_main_urls()
    test_endpoints()
    
    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()
