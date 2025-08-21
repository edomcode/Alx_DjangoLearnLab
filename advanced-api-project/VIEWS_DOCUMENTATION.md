# Custom Views and Generic Views Documentation

## Overview

This document provides comprehensive documentation for the custom views and generic views implemented in the Django REST Framework API. The implementation demonstrates advanced API development patterns including CRUD operations, permissions, filtering, and custom view behavior.

## Architecture

### View Organization

The API is organized into three main categories:

1. **Author Views** - Combined CRUD operations using generic views
2. **Book Views** - Separate CRUD operations for fine-grained control
3. **Legacy Views** - Backward compatibility endpoints

### Generic Views Used

| View Type | Purpose | HTTP Methods | Authentication Required |
|-----------|---------|--------------|------------------------|
| `ListAPIView` | Retrieve multiple resources | GET | No |
| `RetrieveAPIView` | Retrieve single resource | GET | No |
| `CreateAPIView` | Create new resource | POST | Yes |
| `UpdateAPIView` | Update existing resource | PUT, PATCH | Yes |
| `DestroyAPIView` | Delete resource | DELETE | Yes |
| `ListCreateAPIView` | Combined list/create | GET, POST | POST only |
| `RetrieveUpdateDestroyAPIView` | Combined detail operations | GET, PUT, PATCH, DELETE | Write operations only |

## Detailed View Documentation

### Book Views (Separate CRUD Operations)

#### 1. BookListView
```python
class BookListView(generics.ListAPIView)
```

**Purpose**: Retrieve all books with advanced filtering and search capabilities

**Features**:
- **Filtering**: By publication year and author (when django-filter is available)
- **Search**: Full-text search across title and author name
- **Ordering**: Sort by publication year or title
- **Custom Filtering**: Year range filtering via query parameters

**Query Parameters**:
- `search`: Search in title and author name
- `ordering`: Sort by `publication_year` or `title`
- `year_from`: Filter books from specific year
- `year_to`: Filter books up to specific year
- `publication_year`: Filter by exact year (if django-filter available)
- `author`: Filter by author ID (if django-filter available)

**Example Requests**:
```bash
GET /api/books/                           # All books
GET /api/books/?search=Harry              # Search for "Harry"
GET /api/books/?ordering=-publication_year # Newest first
GET /api/books/?year_from=1990&year_to=2000 # Books from 1990-2000
```

#### 2. BookDetailView
```python
class BookDetailView(generics.RetrieveAPIView)
```

**Purpose**: Retrieve a single book by ID

**Features**:
- Detailed book information
- Related author data included
- No authentication required

#### 3. BookCreateView
```python
class BookCreateView(generics.CreateAPIView)
```

**Purpose**: Create new books with custom validation and logging

**Features**:
- **Authentication Required**: Only authenticated users can create books
- **Custom Validation**: Publication year cannot be in the future
- **Custom Response**: Returns success message with created book data
- **Logging**: Logs book creation events
- **Error Handling**: Detailed validation error messages

**Custom Methods**:
- `perform_create()`: Adds custom logic during creation
- `create()`: Custom response formatting

#### 4. BookUpdateView
```python
class BookUpdateView(generics.UpdateAPIView)
```

**Purpose**: Update existing books with change tracking

**Features**:
- **Partial Updates**: Supports PATCH for partial updates
- **Change Tracking**: Logs when book titles are modified
- **Custom Response**: Returns success message with updated data
- **Authentication Required**: Only authenticated users can update

**Custom Methods**:
- `perform_update()`: Tracks changes and logs updates
- `update()`: Custom response formatting

#### 5. BookDeleteView
```python
class BookDeleteView(generics.DestroyAPIView)
```

**Purpose**: Delete books with custom deletion logic

**Features**:
- **Authentication Required**: Only authenticated users can delete
- **Deletion Logging**: Logs deletion events with book details
- **Custom Response**: Returns confirmation message
- **Soft Delete Ready**: Structure supports soft delete implementation

**Custom Methods**:
- `perform_destroy()`: Custom deletion logic and logging
- `destroy()`: Custom response formatting

### Author Views (Combined Operations)

#### 1. AuthorListCreateView
```python
class AuthorListCreateView(generics.ListCreateAPIView)
```

**Purpose**: List all authors and create new authors

**Features**:
- **Nested Serialization**: Authors include their books
- **Name Filtering**: Filter authors by name (case-insensitive)
- **Permission Model**: Read access for all, write access for authenticated users

#### 2. AuthorDetailView
```python
class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView)
```

**Purpose**: Full CRUD operations for individual authors

**Features**:
- **Complete CRUD**: GET, PUT, PATCH, DELETE operations
- **Nested Books**: Includes all books by the author
- **Permission Model**: Read access for all, write access for authenticated users

## Permission System

### Permission Classes Used

1. **`IsAuthenticated`**: Requires user authentication
   - Used for: Book create, update, delete operations

2. **`IsAuthenticatedOrReadOnly`**: Read access for all, write access for authenticated
   - Used for: Author operations, legacy book operations

3. **No Permissions (`[]`)**: Open access
   - Used for: Book list and detail views

### Authentication Flow

```
Unauthenticated User:
├── Can read books and authors
├── Cannot create, update, or delete books
└── Cannot create, update, or delete authors

Authenticated User:
├── Can read books and authors
├── Can create, update, and delete books
└── Can create, update, and delete authors
```

## Custom View Features

### 1. Custom Response Formatting

All create, update, and delete operations return structured responses:

```json
{
    "message": "Operation completed successfully",
    "book": { /* book data */ }
}
```

### 2. Custom Validation

- **Future Year Validation**: Books cannot have publication years in the future
- **Error Messages**: Detailed, user-friendly error messages

### 3. Logging and Tracking

- **Creation Logging**: Logs when new books are created
- **Update Tracking**: Tracks and logs title changes
- **Deletion Logging**: Logs deletion events with book details

### 4. Query Optimization

- **Select Related**: Uses `select_related('author')` for efficient queries
- **Prefetch Related**: Optimizes nested serialization queries

## URL Patterns

### Primary Endpoints
```
/api/                           # API overview
/api/books/                     # List books (with filtering)
/api/books/<id>/                # Book detail
/api/books/create/              # Create book
/api/books/<id>/update/         # Update book
/api/books/<id>/delete/         # Delete book
/api/authors/                   # List/create authors
/api/authors/<id>/              # Author detail/update/delete
```

### Legacy Endpoints (Backward Compatibility)
```
/api/books/legacy/              # Combined list/create
/api/books/<id>/legacy/         # Combined detail/update/delete
```

## Testing

### Automated Testing

The implementation includes comprehensive test scripts:

1. **`test_endpoints.py`**: Tests all endpoints with various scenarios
2. **`test_serializers.py`**: Tests serializer functionality
3. **`check_imports.py`**: Validates import dependencies

### Test Coverage

- ✅ Public endpoint access (no authentication)
- ✅ Protected endpoint access (authentication required)
- ✅ Permission enforcement
- ✅ Custom validation
- ✅ Filtering and search functionality
- ✅ CRUD operations
- ✅ Custom response formatting
- ✅ Error handling

### Running Tests

```bash
# Test all endpoints
python test_endpoints.py

# Test serializers
python test_serializers.py

# Check dependencies
python check_imports.py
```

## Best Practices Implemented

1. **Separation of Concerns**: Separate views for each CRUD operation
2. **Custom Logic**: Override methods for custom behavior
3. **Error Handling**: Comprehensive error responses
4. **Documentation**: Extensive docstrings and comments
5. **Security**: Proper permission implementation
6. **Performance**: Query optimization
7. **Flexibility**: Configurable filtering and search
8. **Backward Compatibility**: Legacy endpoints maintained

## Future Enhancements

1. **Pagination**: Add pagination for large datasets
2. **Rate Limiting**: Implement API rate limiting
3. **Caching**: Add response caching
4. **Versioning**: API versioning support
5. **Soft Delete**: Implement soft delete functionality
6. **Audit Trail**: Enhanced logging and audit trails
