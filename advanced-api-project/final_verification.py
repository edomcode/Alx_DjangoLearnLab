#!/usr/bin/env python
"""
Final verification that all requirements are met.
"""

def check_requirements():
    print("FINAL REQUIREMENTS VERIFICATION")
    print("=" * 50)
    
    # 1. Check URL patterns
    print("\n1. Checking URL patterns in api/urls.py:")
    try:
        with open('api/urls.py', 'r') as f:
            content = f.read()
        
        # Check for required patterns
        if 'books/update' in content:
            print("   ✅ 'books/update' pattern found")
        else:
            print("   ❌ 'books/update' pattern NOT found")
            
        if 'books/delete' in content:
            print("   ✅ 'books/delete' pattern found")
        else:
            print("   ❌ 'books/delete' pattern NOT found")
            
        # Show the actual lines
        lines = content.split('\n')
        print("\n   Relevant URL patterns:")
        for i, line in enumerate(lines, 1):
            if 'books/' in line and 'path(' in line:
                print(f"   Line {i}: {line.strip()}")
                
    except Exception as e:
        print(f"   ❌ Error reading api/urls.py: {e}")
    
    # 2. Check permission classes
    print("\n2. Checking permission classes in api/views.py:")
    try:
        with open('api/views.py', 'r') as f:
            content = f.read()
        
        permission_checks = [
            ('IsAuthenticated', 'IsAuthenticated'),
            ('IsAuthenticatedOrReadOnly', 'IsAuthenticatedOrReadOnly'),
            ('permission_classes', 'permission_classes attribute')
        ]
        
        for pattern, description in permission_checks:
            count = content.count(pattern)
            if count > 0:
                print(f"   ✅ {description}: found {count} times")
            else:
                print(f"   ❌ {description}: NOT found")
                
    except Exception as e:
        print(f"   ❌ Error reading api/views.py: {e}")
    
    # 3. Check main project URLs
    print("\n3. Checking main project URLs:")
    try:
        with open('advanced_api_project/urls.py', 'r') as f:
            content = f.read()
        
        if "include('api.urls')" in content:
            print("   ✅ API URLs included in main project")
        else:
            print("   ❌ API URLs NOT included in main project")
            
        if "path('api/'," in content:
            print("   ✅ API URLs mapped to 'api/' path")
        else:
            print("   ❌ API URLs NOT mapped to 'api/' path")
            
    except Exception as e:
        print(f"   ❌ Error reading main urls.py: {e}")
    
    # 4. Check generic views implementation
    print("\n4. Checking generic views implementation:")
    try:
        with open('api/views.py', 'r') as f:
            content = f.read()
        
        view_checks = [
            ('BookListView', 'ListView for books'),
            ('BookDetailView', 'DetailView for books'),
            ('BookCreateView', 'CreateView for books'),
            ('BookUpdateView', 'UpdateView for books'),
            ('BookDeleteView', 'DeleteView for books')
        ]
        
        for view_class, description in view_checks:
            if f'class {view_class}' in content:
                print(f"   ✅ {description}: implemented")
            else:
                print(f"   ❌ {description}: NOT implemented")
                
    except Exception as e:
        print(f"   ❌ Error checking views: {e}")
    
    print("\n" + "=" * 50)
    print("VERIFICATION COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    check_requirements()
