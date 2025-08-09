#!/usr/bin/env python
"""
Check if the exact import statements are present as expected by the checker.
"""

def check_exact_imports():
    print("Checking exact import statements...")

    # Read the views.py file
    with open('api/views.py', 'r') as f:
        content = f.read()

    # Check for the exact import statement the checker expects
    expected_import = "from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated"

    if expected_import in content:
        print(f"✅ Found exact import: {expected_import}")
    else:
        print(f"❌ Missing exact import: {expected_import}")

        # Show what imports we do have
        lines = content.split('\n')
        print("\nActual permission imports found:")
        for line in lines:
            if 'from rest_framework.permissions import' in line:
                print(f"  {line.strip()}")

    # Check for permission class usage
    permission_classes = ['IsAuthenticated', 'IsAuthenticatedOrReadOnly']
    for perm_class in permission_classes:
        count = content.count(perm_class)
        print(f"✅ {perm_class} used {count} times")

    # Check main project URLs
    print("\nChecking main project URLs...")
    with open('advanced_api_project/urls.py', 'r') as f:
        main_urls = f.read()

    if "include('api.urls')" in main_urls:
        print("✅ API URLs included in main project")

        # Show all URL patterns
        lines = main_urls.split('\n')
        print("\nURL patterns in main project:")
        for line in lines:
            if 'path(' in line:
                print(f"  {line.strip()}")
    else:
        print("❌ API URLs not included in main project")

if __name__ == "__main__":
    check_exact_imports()
