#!/usr/bin/env python
"""
Test script to verify the custom user model works correctly.
"""
import os
import sys
import django
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_config.settings')
django.setup()

from bookshelf.models import CustomUser

def test_custom_user():
    """Test creating and managing custom users."""
    print("Testing Custom User Model...")
    
    # Test creating a regular user
    print("\n1. Creating a regular user...")
    user = CustomUser.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        date_of_birth=date(1990, 1, 1)
    )
    print(f"Created user: {user}")
    print(f"Date of birth: {user.date_of_birth}")
    print(f"Is staff: {user.is_staff}")
    print(f"Is superuser: {user.is_superuser}")
    
    # Test creating a superuser
    print("\n2. Creating a superuser...")
    admin_user = CustomUser.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        date_of_birth=date(1985, 5, 15)
    )
    print(f"Created admin: {admin_user}")
    print(f"Date of birth: {admin_user.date_of_birth}")
    print(f"Is staff: {admin_user.is_staff}")
    print(f"Is superuser: {admin_user.is_superuser}")
    
    # Test querying users
    print("\n3. Querying all users...")
    all_users = CustomUser.objects.all()
    for user in all_users:
        print(f"User: {user.username}, Email: {user.email}, DOB: {user.date_of_birth}")
    
    print("\n✅ Custom User Model test completed successfully!")

if __name__ == '__main__':
    test_custom_user()
