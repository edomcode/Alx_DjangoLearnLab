#!/usr/bin/env python
"""
Test runner script to verify the unit tests work correctly.

This script runs a subset of tests to verify the test framework is working.
"""

import os
import sys
import django
from django.test.utils import get_runner
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

def run_sample_tests():
    """
    Run a sample of tests to verify they work correctly.
    """
    print("Running sample unit tests...")
    print("=" * 50)
    
    try:
        # Import test classes
        from api.test_views import BookAPITestCase, SerializerTestCase
        from django.test import TestCase
        import unittest
        
        # Create test suite
        suite = unittest.TestSuite()
        
        # Add specific test methods
        suite.addTest(BookAPITestCase('test_book_list_unauthenticated'))
        suite.addTest(BookAPITestCase('test_book_create_unauthenticated'))
        suite.addTest(BookAPITestCase('test_book_create_authenticated'))
        suite.addTest(SerializerTestCase('test_book_serializer_valid_data'))
        suite.addTest(SerializerTestCase('test_book_serializer_future_year_validation'))
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Print results
        print("\n" + "=" * 50)
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")
        
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")
        
        if result.wasSuccessful():
            print("\n✅ All sample tests passed!")
        else:
            print("\n❌ Some tests failed.")
        
        return result.wasSuccessful()
        
    except Exception as e:
        print(f"Error running tests: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_test_structure():
    """
    Verify the test file structure and imports.
    """
    print("Verifying test structure...")
    print("-" * 30)
    
    try:
        # Check if test file exists
        import api.test_views
        print("✅ test_views.py file exists and imports successfully")
        
        # Check test classes
        test_classes = [
            'BookAPITestCase',
            'BookFilteringTestCase', 
            'AuthorAPITestCase',
            'APIOverviewTestCase',
            'SerializerTestCase',
            'EdgeCaseTestCase',
            'IntegrationTestCase'
        ]
        
        for class_name in test_classes:
            if hasattr(api.test_views, class_name):
                print(f"✅ {class_name} test class found")
            else:
                print(f"❌ {class_name} test class missing")
        
        # Check imports
        from api.test_views import APITestCase, TestCase
        from api.models import Author, Book
        from api.serializers import BookSerializer, AuthorSerializer
        print("✅ All required imports work correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying test structure: {e}")
        return False

def main():
    """
    Main function to run test verification.
    """
    print("DJANGO REST FRAMEWORK API TESTS VERIFICATION")
    print("=" * 60)
    
    # Step 1: Verify test structure
    structure_ok = verify_test_structure()
    
    if not structure_ok:
        print("\n❌ Test structure verification failed!")
        return False
    
    print("\n")
    
    # Step 2: Run sample tests
    tests_ok = run_sample_tests()
    
    print("\n" + "=" * 60)
    if structure_ok and tests_ok:
        print("✅ TEST VERIFICATION SUCCESSFUL!")
        print("\nTo run all tests, use:")
        print("  python manage.py test api")
        print("  python manage.py test api.test_views")
    else:
        print("❌ TEST VERIFICATION FAILED!")
    
    return structure_ok and tests_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
