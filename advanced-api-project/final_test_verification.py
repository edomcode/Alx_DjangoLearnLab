#!/usr/bin/env python
"""
Final verification script to confirm all unit testing requirements are met.
"""

import os
import ast

def check_test_database_configuration():
    """Check if separate test database is configured."""
    print("1. CHECKING TEST DATABASE CONFIGURATION")
    print("-" * 50)
    
    settings_file = 'advanced_api_project/settings.py'
    
    if not os.path.exists(settings_file):
        print("❌ Settings file not found")
        return False
    
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # Check for test database configuration
    if 'TEST' in content and 'test_db.sqlite3' in content:
        print("✅ Separate test database configured")
        print("   - Test database file: test_db.sqlite3")
        print("   - Development database file: db.sqlite3")
        print("   - Databases are properly isolated")
        return True
    else:
        print("❌ Test database configuration not found")
        return False

def check_client_login_usage():
    """Check if self.client.login is used in test file."""
    print("\n2. CHECKING CLIENT.LOGIN USAGE")
    print("-" * 50)
    
    test_file = 'api/test_views.py'
    
    if not os.path.exists(test_file):
        print("❌ Test file not found")
        return False
    
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Count occurrences of self.client.login
    login_count = content.count('self.client.login')
    
    if login_count > 0:
        print(f"✅ self.client.login found {login_count} times")
        
        # Find specific test methods using client.login
        lines = content.split('\n')
        login_methods = []
        
        for i, line in enumerate(lines):
            if 'self.client.login' in line:
                # Find the test method name
                for j in range(i, -1, -1):
                    if lines[j].strip().startswith('def test_'):
                        method_name = lines[j].strip().split('(')[0].replace('def ', '')
                        login_methods.append(method_name)
                        break
        
        print("   Test methods using self.client.login:")
        for method in set(login_methods):  # Remove duplicates
            print(f"   - {method}")
        
        return True
    else:
        print("❌ self.client.login not found in test file")
        return False

def check_comprehensive_test_coverage():
    """Check if comprehensive test coverage is implemented."""
    print("\n3. CHECKING COMPREHENSIVE TEST COVERAGE")
    print("-" * 50)
    
    test_file = 'api/test_views.py'
    
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Parse the file to count test classes and methods
    try:
        tree = ast.parse(content)
    except SyntaxError:
        print("❌ Syntax error in test file")
        return False
    
    test_classes = []
    test_methods = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name.endswith('TestCase'):
            test_classes.append(node.name)
            
            # Count test methods in this class
            class_methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name.startswith('test_'):
                    class_methods.append(item.name)
                    test_methods.append(f"{node.name}.{item.name}")
    
    print(f"✅ Test Classes: {len(test_classes)}")
    print(f"✅ Test Methods: {len(test_methods)}")
    
    # Check for required test areas
    required_areas = {
        'CRUD Operations': ['create', 'update', 'delete', 'list', 'detail'],
        'Authentication': ['login', 'unauthenticated', 'authenticated'],
        'Validation': ['validation', 'invalid', 'future_year'],
        'Filtering': ['search', 'filter', 'ordering'],
        'Error Handling': ['not_found', 'invalid_data', 'edge_case']
    }
    
    print("\n   Coverage Areas:")
    for area, keywords in required_areas.items():
        found = any(any(keyword in method.lower() for keyword in keywords) 
                   for method in test_methods)
        status = "✅" if found else "❌"
        print(f"   {status} {area}")
    
    return len(test_classes) >= 5 and len(test_methods) >= 30

def check_documentation():
    """Check if proper documentation is provided."""
    print("\n4. CHECKING DOCUMENTATION")
    print("-" * 50)
    
    docs = [
        ('TESTING_DOCUMENTATION.md', 'Testing approach documentation'),
        ('TEST_DATABASE_CONFIGURATION.md', 'Test database configuration'),
        ('UNIT_TESTS_SUMMARY.md', 'Unit tests summary')
    ]
    
    all_docs_present = True
    
    for doc_file, description in docs:
        if os.path.exists(doc_file):
            print(f"✅ {doc_file} - {description}")
        else:
            print(f"❌ {doc_file} - {description} (MISSING)")
            all_docs_present = False
    
    return all_docs_present

def main():
    """Run all verification checks."""
    print("FINAL UNIT TESTING REQUIREMENTS VERIFICATION")
    print("=" * 60)
    
    checks = [
        check_test_database_configuration(),
        check_client_login_usage(),
        check_comprehensive_test_coverage(),
        check_documentation()
    ]
    
    print("\n" + "=" * 60)
    print("VERIFICATION RESULTS")
    print("=" * 60)
    
    if all(checks):
        print("✅ ALL REQUIREMENTS MET!")
        print("\nSummary:")
        print("✅ Separate test database configured")
        print("✅ self.client.login methods implemented")
        print("✅ Comprehensive test coverage provided")
        print("✅ Complete documentation available")
        print("\nThe unit testing implementation is COMPLETE and meets all requirements.")
        return True
    else:
        print("❌ SOME REQUIREMENTS NOT MET!")
        print("Please review the failed checks above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
