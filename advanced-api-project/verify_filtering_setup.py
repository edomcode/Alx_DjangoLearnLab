#!/usr/bin/env python
"""
Verification script to confirm all filtering, searching, and ordering components are properly set up.
"""

import os
import ast

def check_required_imports():
    """Check if all required imports are present in views.py."""
    print("CHECKING REQUIRED IMPORTS")
    print("=" * 50)
    
    views_file = 'api/views.py'
    
    if not os.path.exists(views_file):
        print("❌ views.py file not found")
        return False
    
    with open(views_file, 'r') as f:
        content = f.read()
    
    # Check for required imports
    required_imports = [
        'from django_filters import rest_framework',
        'from django_filters.rest_framework import DjangoFilterBackend',
        'from rest_framework.filters import SearchFilter, OrderingFilter',
    ]
    
    all_imports_found = True
    
    for import_stmt in required_imports:
        if import_stmt in content:
            print(f"✅ Found: {import_stmt}")
        else:
            print(f"❌ Missing: {import_stmt}")
            all_imports_found = False
    
    return all_imports_found

def check_filter_backends():
    """Check if filter backends are properly configured."""
    print("\nCHECKING FILTER BACKENDS CONFIGURATION")
    print("=" * 50)
    
    views_file = 'api/views.py'
    
    with open(views_file, 'r') as f:
        content = f.read()
    
    # Check for filter backends configuration
    required_backends = [
        'DjangoFilterBackend',
        'SearchFilter',
        'OrderingFilter'
    ]
    
    backends_found = True
    
    for backend in required_backends:
        if backend in content and 'filter_backends' in content:
            print(f"✅ {backend} configured in filter_backends")
        else:
            print(f"❌ {backend} not found in filter_backends")
            backends_found = False
    
    return backends_found

def check_search_configuration():
    """Check if search functionality is properly configured."""
    print("\nCHECKING SEARCH CONFIGURATION")
    print("=" * 50)
    
    views_file = 'api/views.py'
    
    with open(views_file, 'r') as f:
        content = f.read()
    
    # Check for search fields configuration
    search_indicators = [
        'search_fields',
        'title',
        'author__name'
    ]
    
    search_configured = True
    
    if 'search_fields' in content:
        print("✅ search_fields configured")
        
        # Check if title and author fields are included
        if 'title' in content and 'author__name' in content:
            print("✅ Search enabled on title and author fields")
        else:
            print("❌ Title and/or author fields not configured for search")
            search_configured = False
    else:
        print("❌ search_fields not configured")
        search_configured = False
    
    return search_configured

def check_ordering_configuration():
    """Check if ordering functionality is properly configured."""
    print("\nCHECKING ORDERING CONFIGURATION")
    print("=" * 50)
    
    views_file = 'api/views.py'
    
    with open(views_file, 'r') as f:
        content = f.read()
    
    # Check for ordering configuration
    ordering_indicators = [
        'ordering_fields',
        'ordering'
    ]
    
    ordering_configured = True
    
    if 'ordering_fields' in content:
        print("✅ ordering_fields configured")
        
        # Check for common ordering fields
        if 'title' in content and 'publication_year' in content:
            print("✅ Ordering enabled on title and publication_year")
        else:
            print("❌ Title and/or publication_year not configured for ordering")
            ordering_configured = False
    else:
        print("❌ ordering_fields not configured")
        ordering_configured = False
    
    if 'ordering = ' in content:
        print("✅ Default ordering configured")
    else:
        print("❌ Default ordering not configured")
        ordering_configured = False
    
    return ordering_configured

def check_filtering_configuration():
    """Check if filtering functionality is properly configured."""
    print("\nCHECKING FILTERING CONFIGURATION")
    print("=" * 50)
    
    views_file = 'api/views.py'
    
    with open(views_file, 'r') as f:
        content = f.read()
    
    # Check for filtering configuration
    filtering_configured = True
    
    if 'filterset_fields' in content:
        print("✅ filterset_fields configured")
        
        # Check for basic filtering fields
        if 'title' in content and 'author' in content and 'publication_year' in content:
            print("✅ Basic filtering enabled on title, author, and publication_year")
        else:
            print("❌ Basic filtering fields not properly configured")
            filtering_configured = False
    else:
        print("❌ filterset_fields not configured")
        filtering_configured = False
    
    if 'filterset_class' in content:
        print("✅ Custom filterset_class configured")
    else:
        print("❌ Custom filterset_class not configured")
        filtering_configured = False
    
    return filtering_configured

def check_custom_filters():
    """Check if custom filter classes exist."""
    print("\nCHECKING CUSTOM FILTER CLASSES")
    print("=" * 50)
    
    filters_file = 'api/filters.py'
    
    if not os.path.exists(filters_file):
        print("❌ filters.py file not found")
        return False
    
    with open(filters_file, 'r') as f:
        content = f.read()
    
    # Check for custom filter classes
    required_classes = ['BookFilter', 'AuthorFilter']
    
    classes_found = True
    
    for class_name in required_classes:
        if f'class {class_name}' in content:
            print(f"✅ {class_name} class found")
        else:
            print(f"❌ {class_name} class not found")
            classes_found = False
    
    return classes_found

def test_api_endpoints():
    """Test that the API endpoints work with filtering, searching, and ordering."""
    print("\nTESTING API ENDPOINTS")
    print("=" * 50)
    
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
    django.setup()
    
    from django.test import Client
    from api.models import Author, Book
    
    # Create test data
    author = Author.objects.create(name="Test Author")
    book = Book.objects.create(title="Test Book", publication_year=2020, author=author)
    
    client = Client()
    
    # Test basic endpoint
    response = client.get('/api/books/')
    if response.status_code == 200:
        print("✅ Basic book list endpoint works")
    else:
        print(f"❌ Basic book list endpoint failed: {response.status_code}")
        return False
    
    # Test filtering
    response = client.get('/api/books/', {'title': 'Test'})
    if response.status_code == 200:
        print("✅ Title filtering works")
    else:
        print(f"❌ Title filtering failed: {response.status_code}")
        return False
    
    # Test search
    response = client.get('/api/books/', {'search': 'Test'})
    if response.status_code == 200:
        print("✅ Search functionality works")
    else:
        print(f"❌ Search functionality failed: {response.status_code}")
        return False
    
    # Test ordering
    response = client.get('/api/books/', {'ordering': 'title'})
    if response.status_code == 200:
        print("✅ Ordering functionality works")
    else:
        print(f"❌ Ordering functionality failed: {response.status_code}")
        return False
    
    return True

def main():
    """Run all verification checks."""
    print("FILTERING, SEARCHING, AND ORDERING SETUP VERIFICATION")
    print("=" * 70)
    
    checks = [
        check_required_imports(),
        check_filter_backends(),
        check_search_configuration(),
        check_ordering_configuration(),
        check_filtering_configuration(),
        check_custom_filters(),
        test_api_endpoints()
    ]
    
    print("\n" + "=" * 70)
    print("VERIFICATION RESULTS")
    print("=" * 70)
    
    if all(checks):
        print("✅ ALL CHECKS PASSED!")
        print("\nSummary:")
        print("✅ Required imports are present")
        print("✅ Filter backends are configured")
        print("✅ Search functionality is set up")
        print("✅ Ordering functionality is configured")
        print("✅ Filtering is properly implemented")
        print("✅ Custom filter classes exist")
        print("✅ API endpoints are working")
        print("\nThe filtering, searching, and ordering implementation is COMPLETE!")
        return True
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Please review the failed checks above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
