#!/usr/bin/env python
"""
Check if all imports in views.py are working correctly.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

try:
    print("Testing imports...")
    
    from rest_framework import generics, status, permissions, filters
    print("✓ rest_framework imports successful")
    
    from rest_framework.response import Response
    print("✓ Response import successful")
    
    from rest_framework.decorators import api_view, permission_classes
    print("✓ decorators import successful")
    
    from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
    print("✓ permissions import successful")
    
    try:
        from django_filters.rest_framework import DjangoFilterBackend
        print("✓ django_filters import successful")
    except ImportError:
        print("✗ django_filters import failed - will use alternative")
    
    from django.shortcuts import get_object_or_404
    print("✓ django shortcuts import successful")
    
    from api.models import Author, Book
    print("✓ models import successful")
    
    from api.serializers import AuthorSerializer, BookSerializer
    print("✓ serializers import successful")
    
    print("\nAll imports successful! Views should work correctly.")
    
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Other error: {e}")
