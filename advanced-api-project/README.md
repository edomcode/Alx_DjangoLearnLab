# Advanced API Project with Django REST Framework

This project demonstrates advanced API development with Django REST Framework, focusing on custom serializers that handle complex data structures and nested relationships.

## Project Overview

The project implements a book management system with two main models:
- **Author**: Represents book authors
- **Book**: Represents books with a foreign key relationship to authors

## Features

### Custom Serializers
- **BookSerializer**: Handles book serialization with custom validation
- **AuthorSerializer**: Includes nested book serialization and additional metadata

### Key Functionality
1. **Nested Relationships**: Authors are serialized with all their related books
2. **Custom Validation**: Books cannot have publication years in the future
3. **Dynamic Data**: Author serialization includes book count
4. **Comprehensive API**: Full CRUD operations for both models

## Models

### Author Model
```python
class Author(models.Model):
    name = models.CharField(max_length=100)
```

### Book Model
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
```

## Serializers

### BookSerializer
- Serializes all Book model fields
- **Custom Validation**: Ensures `publication_year` is not in the future
- Returns validation error with current year information

### AuthorSerializer
- Serializes Author model with nested books
- **Nested Serialization**: Uses BookSerializer for related books
- **Dynamic Fields**: Adds `books_count` to the serialized output
- **Relationship Handling**: Utilizes Django's `related_name='books'`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/` | GET | API overview |
| `/api/authors/` | GET, POST | List all authors or create new author |
| `/api/authors/<id>/` | GET, PUT, PATCH, DELETE | Author detail operations |
| `/api/books/` | GET, POST | List all books or create new book |
| `/api/books/<id>/` | GET, PUT, PATCH, DELETE | Book detail operations |

## Setup Instructions

### 1. Install Dependencies
```bash
pip install django djangorestframework
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

## Testing

### Automated Testing
Run the included test script to verify serializer functionality:
```bash
python test_serializers.py
```

This script tests:
- Model creation and relationships
- Serializer functionality
- Custom validation (future year rejection)
- Nested serialization
- Multiple object serialization

### Manual Testing via Django Admin
1. Access admin at `http://127.0.0.1:8000/admin/`
2. Create authors and books
3. Verify relationships and data integrity

### API Testing
1. Visit `http://127.0.0.1:8000/api/` for API overview
2. Test endpoints using tools like Postman or curl
3. Verify nested serialization in author endpoints

## Example API Responses

### Author with Books
```json
{
    "id": 1,
    "name": "J.K. Rowling",
    "books": [
        {
            "id": 1,
            "title": "Harry Potter and the Philosopher's Stone",
            "publication_year": 1997,
            "author": 1
        },
        {
            "id": 2,
            "title": "Harry Potter and the Chamber of Secrets",
            "publication_year": 1998,
            "author": 1
        }
    ],
    "books_count": 2
}
```

### Validation Error Example
```json
{
    "publication_year": [
        "Publication year cannot be in the future. Current year is 2025."
    ]
}
```

## Project Structure
```
advanced-api-project/
├── advanced_api_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── manage.py
├── test_serializers.py
└── README.md
```

## Custom Views and Generic Views

### Generic Views Implementation

The project implements comprehensive CRUD operations using Django REST Framework's generic views:

#### Book Views (Separate CRUD Operations)

1. **BookListView** (`generics.ListAPIView`)
   - **Purpose**: Retrieve all books with filtering and search
   - **Permissions**: Open to all users
   - **Features**:
     - Filtering by publication year and author
     - Search by title and author name
     - Custom year range filtering
     - Ordering capabilities

2. **BookDetailView** (`generics.RetrieveAPIView`)
   - **Purpose**: Retrieve a single book by ID
   - **Permissions**: Open to all users
   - **Features**: Detailed book information

3. **BookCreateView** (`generics.CreateAPIView`)
   - **Purpose**: Create new books
   - **Permissions**: Requires authentication
   - **Features**:
     - Custom validation through serializer
     - Custom response formatting
     - Creation logging

4. **BookUpdateView** (`generics.UpdateAPIView`)
   - **Purpose**: Update existing books (PUT/PATCH)
   - **Permissions**: Requires authentication
   - **Features**:
     - Partial update support
     - Change tracking and logging
     - Custom response formatting

5. **BookDeleteView** (`generics.DestroyAPIView`)
   - **Purpose**: Delete books
   - **Permissions**: Requires authentication
   - **Features**:
     - Custom deletion logic
     - Deletion logging
     - Custom response formatting

#### Author Views (Combined Operations)

1. **AuthorListCreateView** (`generics.ListCreateAPIView`)
   - **Purpose**: List authors and create new authors
   - **Permissions**: Read-only for unauthenticated, full access for authenticated
   - **Features**: Name-based filtering

2. **AuthorDetailView** (`generics.RetrieveUpdateDestroyAPIView`)
   - **Purpose**: Full CRUD operations for individual authors
   - **Permissions**: Read-only for unauthenticated, full access for authenticated

### Permission System

The API implements a comprehensive permission system:

- **Public Access**: List and detail views for books and authors
- **Authenticated Access**: Create, update, and delete operations
- **Permission Classes Used**:
  - `IsAuthenticated`: Requires user authentication
  - `IsAuthenticatedOrReadOnly`: Read access for all, write access for authenticated users

### URL Patterns

| Endpoint | Method | View | Description |
|----------|--------|------|-------------|
| `/api/` | GET | `api_overview` | API documentation |
| `/api/books/` | GET | `BookListView` | List all books with filtering |
| `/api/books/<id>/` | GET | `BookDetailView` | Get specific book |
| `/api/books/create/` | POST | `BookCreateView` | Create new book |
| `/api/books/<id>/update/` | PUT/PATCH | `BookUpdateView` | Update book |
| `/api/books/<id>/delete/` | DELETE | `BookDeleteView` | Delete book |
| `/api/authors/` | GET/POST | `AuthorListCreateView` | List/create authors |
| `/api/authors/<id>/` | GET/PUT/PATCH/DELETE | `AuthorDetailView` | Full author CRUD |

### Custom View Features

#### Filtering and Search
```python
# BookListView supports:
filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
filterset_fields = ['publication_year', 'author']
search_fields = ['title', 'author__name']
ordering_fields = ['publication_year', 'title']
```

#### Custom Query Parameters
- `year_from`: Filter books from specific year
- `year_to`: Filter books up to specific year
- `name`: Filter authors by name (case-insensitive)

#### Custom Response Formatting
All create, update, and delete operations return custom formatted responses with success messages and relevant data.

### Testing

#### Automated Testing
Run the comprehensive view test script:
```bash
python test_views.py
```

This script tests:
- Unauthenticated access (should work for read operations)
- Authenticated access (should work for all operations)
- Permission enforcement
- Custom validation
- Filtering and search functionality
- Author endpoints with nested serialization

#### Manual Testing Examples

**Create a book (requires authentication):**
```bash
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"title": "New Book", "publication_year": 2023, "author": 1}'
```

**Filter books by year:**
```bash
curl "http://127.0.0.1:8000/api/books/?publication_year=1997"
```

**Search books by title:**
```bash
curl "http://127.0.0.1:8000/api/books/?search=Harry"
```

## Key Learning Points

1. **Custom Serializer Validation**: Implementing field-level validation methods
2. **Nested Serialization**: Handling one-to-many relationships in serializers
3. **Django Model Relationships**: Using foreign keys with related_name
4. **API Design**: Creating RESTful endpoints with proper HTTP methods
5. **Generic Views**: Utilizing DRF's powerful generic views for CRUD operations
6. **Permission System**: Implementing authentication-based access control
7. **Filtering and Search**: Adding dynamic filtering and search capabilities
8. **Custom View Behavior**: Extending generic views with custom logic
9. **Testing**: Comprehensive testing of view functionality and permissions
