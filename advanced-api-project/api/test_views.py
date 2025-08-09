"""
Comprehensive unit tests for Django REST Framework API endpoints.

This module contains unit tests for all API endpoints including:
- CRUD operations for Book model
- Authentication and permission testing
- Filtering, searching, and ordering functionality
- Response data integrity and status code verification
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime
import json

from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


class BookAPITestCase(APITestCase):
    """
    Test cases for Book API endpoints.
    
    Tests CRUD operations, permissions, and data integrity for Book model.
    """
    
    def setUp(self):
        """
        Set up test data for each test method.
        
        Creates test users, authors, and books for testing.
        """
        # Create test users with unique usernames
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        self.user = User.objects.create_user(
            username=f'testuser_{unique_id}',
            email=f'test_{unique_id}@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username=f'admin_{unique_id}',
            email=f'admin_{unique_id}@example.com',
            password='adminpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author2
        )
        
        # Set up API client
        self.client = APIClient()
        
        # Define API endpoints
        self.book_list_url = reverse('book-list')
        self.book_create_url = reverse('book-create')
        self.book_detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})
        self.book_update_url = lambda pk: reverse('book-update', kwargs={'pk': pk})
        self.book_delete_url = lambda pk: reverse('book-delete', kwargs={'pk': pk})
    
    def test_book_list_unauthenticated(self):
        """
        Test that unauthenticated users can access book list.
        
        Expected: 200 OK with list of books
        """
        response = self.client.get(self.book_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify book data structure
        book_data = response.data[0]
        self.assertIn('id', book_data)
        self.assertIn('title', book_data)
        self.assertIn('publication_year', book_data)
        self.assertIn('author', book_data)
    
    def test_book_detail_unauthenticated(self):
        """
        Test that unauthenticated users can access book detail.
        
        Expected: 200 OK with book details
        """
        response = self.client.get(self.book_detail_url(self.book1.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.book1.author.id)
    
    def test_book_detail_not_found(self):
        """
        Test accessing non-existent book detail.
        
        Expected: 404 Not Found
        """
        response = self.client.get(self.book_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_book_create_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        
        Expected: 401 Unauthorized or 403 Forbidden
        """
        book_data = {
            'title': 'Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, book_data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_book_create_authenticated(self):
        """
        Test that authenticated users can create books.
        
        Expected: 201 Created with book data
        """
        self.client.force_authenticate(user=self.user)
        
        book_data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, book_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('book', response.data)
        self.assertEqual(response.data['book']['title'], 'New Test Book')
        
        # Verify book was created in database
        self.assertTrue(Book.objects.filter(title='New Test Book').exists())
    
    def test_book_create_invalid_data(self):
        """
        Test creating book with invalid data.
        
        Expected: 400 Bad Request with validation errors
        """
        self.client.force_authenticate(user=self.user)
        
        # Test with missing required fields
        invalid_data = {
            'title': '',  # Empty title
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_book_create_future_year_validation(self):
        """
        Test custom validation for future publication year.
        
        Expected: 400 Bad Request with validation error
        """
        self.client.force_authenticate(user=self.user)
        
        future_year = datetime.now().year + 1
        book_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, book_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_book_update_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books.
        
        Expected: 401 Unauthorized or 403 Forbidden
        """
        book_data = {
            'title': 'Updated Title',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.put(self.book_update_url(self.book1.id), book_data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_book_update_authenticated(self):
        """
        Test that authenticated users can update books.
        
        Expected: 200 OK with updated book data
        """
        self.client.force_authenticate(user=self.user)
        
        book_data = {
            'title': 'Updated Harry Potter',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(self.book_update_url(self.book1.id), book_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['book']['title'], 'Updated Harry Potter')
        
        # Verify book was updated in database
        updated_book = Book.objects.get(id=self.book1.id)
        self.assertEqual(updated_book.title, 'Updated Harry Potter')
    
    def test_book_partial_update(self):
        """
        Test partial update (PATCH) of book.
        
        Expected: 200 OK with partially updated book data
        """
        self.client.force_authenticate(user=self.user)
        
        partial_data = {'title': 'Partially Updated Title'}
        
        response = self.client.patch(self.book_update_url(self.book1.id), partial_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['book']['title'], 'Partially Updated Title')
        
        # Verify other fields remain unchanged
        updated_book = Book.objects.get(id=self.book1.id)
        self.assertEqual(updated_book.publication_year, 1997)  # Should remain unchanged
    
    def test_book_delete_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books.
        
        Expected: 401 Unauthorized or 403 Forbidden
        """
        response = self.client.delete(self.book_delete_url(self.book1.id))
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_book_delete_authenticated(self):
        """
        Test that authenticated users can delete books.
        
        Expected: 200 OK with deletion confirmation
        """
        self.client.force_authenticate(user=self.user)
        
        book_id = self.book1.id
        response = self.client.delete(self.book_delete_url(book_id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Verify book was deleted from database
        self.assertFalse(Book.objects.filter(id=book_id).exists())
    
    def test_book_delete_not_found(self):
        """
        Test deleting non-existent book.

        Expected: 404 Not Found
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.book_delete_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookFilteringTestCase(APITestCase):
    """
    Test cases for Book API filtering, searching, and ordering functionality.
    """

    def setUp(self):
        """Set up test data for filtering tests."""
        # Create test authors
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")
        self.author3 = Author.objects.create(name="Isaac Asimov")

        # Create test books with different years and authors
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            publication_year=1998,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author2
        )
        self.book5 = Book.objects.create(
            title="Foundation",
            publication_year=1951,
            author=self.author3
        )

        self.client = APIClient()
        self.book_list_url = reverse('book-list')

    def test_book_search_by_title(self):
        """
        Test searching books by title.

        Expected: Returns books matching search term
        """
        response = self.client.get(self.book_list_url, {'search': 'Harry'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two Harry Potter books

        titles = [book['title'] for book in response.data]
        self.assertTrue(all('Harry' in title for title in titles))

    def test_book_search_by_author_name(self):
        """
        Test searching books by author name.

        Expected: Returns books by matching author
        """
        response = self.client.get(self.book_list_url, {'search': 'Orwell'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two Orwell books

    def test_book_search_no_results(self):
        """
        Test searching with term that has no matches.

        Expected: Returns empty list
        """
        response = self.client.get(self.book_list_url, {'search': 'NonexistentBook'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_book_ordering_by_publication_year(self):
        """
        Test ordering books by publication year.

        Expected: Books ordered by publication year
        """
        # Test ascending order
        response = self.client.get(self.book_list_url, {'ordering': 'publication_year'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))

        # Test descending order
        response = self.client.get(self.book_list_url, {'ordering': '-publication_year'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_book_ordering_by_title(self):
        """
        Test ordering books by title.

        Expected: Books ordered alphabetically by title
        """
        response = self.client.get(self.book_list_url, {'ordering': 'title'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_book_year_range_filtering(self):
        """
        Test custom year range filtering.

        Expected: Returns books within specified year range
        """
        # Test books from 1990 onwards
        response = self.client.get(self.book_list_url, {'year_from': 1990})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertTrue(all(year >= 1990 for year in years))

        # Test books up to 1950
        response = self.client.get(self.book_list_url, {'year_to': 1950})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertTrue(all(year <= 1950 for year in years))

        # Test books in specific range
        response = self.client.get(self.book_list_url, {
            'year_from': 1945,
            'year_to': 1955
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertTrue(all(1945 <= year <= 1955 for year in years))

    def test_combined_filtering_and_search(self):
        """
        Test combining search with filtering.

        Expected: Returns books matching both criteria
        """
        response = self.client.get(self.book_list_url, {
            'search': 'Harry',
            'ordering': 'publication_year'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Verify results are ordered and contain search term
        titles = [book['title'] for book in response.data]
        years = [book['publication_year'] for book in response.data]

        self.assertTrue(all('Harry' in title for title in titles))
        self.assertEqual(years, sorted(years))


class AuthorAPITestCase(APITestCase):
    """
    Test cases for Author API endpoints.

    Tests CRUD operations and nested serialization for Author model.
    """

    def setUp(self):
        """Set up test data for author tests."""
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        self.user = User.objects.create_user(
            username=f'testuser_author_{unique_id}',
            password='testpass123'
        )

        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")

        # Create books for testing nested serialization
        self.book1 = Book.objects.create(
            title="Harry Potter",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author2
        )

        self.client = APIClient()
        self.author_list_url = reverse('author-list-create')
        self.author_detail_url = lambda pk: reverse('author-detail', kwargs={'pk': pk})

    def test_author_list_unauthenticated(self):
        """
        Test that unauthenticated users can access author list.

        Expected: 200 OK with list of authors and nested books
        """
        response = self.client.get(self.author_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Verify nested books are included
        author_data = response.data[0]
        self.assertIn('books', author_data)
        self.assertIn('books_count', author_data)

    def test_author_detail_with_nested_books(self):
        """
        Test author detail endpoint includes nested books.

        Expected: 200 OK with author data and nested books
        """
        response = self.client.get(self.author_detail_url(self.author1.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author1.name)
        self.assertIn('books', response.data)
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books_count'], 1)

    def test_author_create_unauthenticated(self):
        """
        Test that unauthenticated users cannot create authors.

        Expected: 401 Unauthorized or 403 Forbidden
        """
        author_data = {'name': 'New Author'}

        response = self.client.post(self.author_list_url, author_data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_author_create_authenticated(self):
        """
        Test that authenticated users can create authors.

        Expected: 201 Created with author data
        """
        self.client.force_authenticate(user=self.user)

        author_data = {'name': 'New Test Author'}

        response = self.client.post(self.author_list_url, author_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Test Author')
        self.assertEqual(response.data['books_count'], 0)

        # Verify author was created in database
        self.assertTrue(Author.objects.filter(name='New Test Author').exists())

    def test_author_update_authenticated(self):
        """
        Test that authenticated users can update authors.

        Expected: 200 OK with updated author data
        """
        self.client.force_authenticate(user=self.user)

        author_data = {'name': 'Updated Author Name'}

        response = self.client.put(self.author_detail_url(self.author1.id), author_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Author Name')

        # Verify author was updated in database
        updated_author = Author.objects.get(id=self.author1.id)
        self.assertEqual(updated_author.name, 'Updated Author Name')

    def test_author_delete_authenticated(self):
        """
        Test that authenticated users can delete authors.

        Expected: 204 No Content
        """
        self.client.force_authenticate(user=self.user)

        author_id = self.author2.id
        response = self.client.delete(self.author_detail_url(author_id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify author was deleted from database
        self.assertFalse(Author.objects.filter(id=author_id).exists())

    def test_author_name_filtering(self):
        """
        Test filtering authors by name.

        Expected: Returns authors matching name filter
        """
        response = self.client.get(self.author_list_url, {'name': 'Rowling'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('Rowling', response.data[0]['name'])


class APIOverviewTestCase(APITestCase):
    """
    Test cases for API overview and utility endpoints.
    """

    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
        self.api_overview_url = reverse('api-overview')

    def test_api_overview_accessible(self):
        """
        Test that API overview is accessible to all users.

        Expected: 200 OK with API endpoint information
        """
        response = self.client.get(self.api_overview_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)

        # Verify it contains endpoint information
        self.assertIn('Books', response.data)
        self.assertIn('Authors', response.data)


class SerializerTestCase(TestCase):
    """
    Test cases for custom serializers.

    Tests serializer validation and data transformation.
    """

    def setUp(self):
        """Set up test data for serializer tests."""
        self.author = Author.objects.create(name="Test Author")

    def test_book_serializer_valid_data(self):
        """
        Test BookSerializer with valid data.

        Expected: Serializer is valid and saves correctly
        """
        valid_data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': self.author.id
        }

        serializer = BookSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

        book = serializer.save()
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.publication_year, 2020)
        self.assertEqual(book.author, self.author)

    def test_book_serializer_future_year_validation(self):
        """
        Test BookSerializer validation for future years.

        Expected: Serializer is invalid with validation error
        """
        future_year = datetime.now().year + 1
        invalid_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.id
        }

        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)

    def test_author_serializer_nested_books(self):
        """
        Test AuthorSerializer includes nested books.

        Expected: Serialized data includes books and books_count
        """
        # Create books for the author
        Book.objects.create(title="Book 1", publication_year=2020, author=self.author)
        Book.objects.create(title="Book 2", publication_year=2021, author=self.author)

        serializer = AuthorSerializer(self.author)
        data = serializer.data

        self.assertEqual(data['name'], self.author.name)
        self.assertIn('books', data)
        self.assertEqual(len(data['books']), 2)
        self.assertEqual(data['books_count'], 2)


class EdgeCaseTestCase(APITestCase):
    """
    Test cases for edge cases and error handling.
    """

    def setUp(self):
        """Set up test data for edge case tests."""
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        self.user = User.objects.create_user(username=f'testuser_edge_{unique_id}', password='testpass123')
        self.author = Author.objects.create(name="Test Author")
        self.client = APIClient()

    def test_book_create_with_nonexistent_author(self):
        """
        Test creating book with non-existent author ID.

        Expected: 400 Bad Request with validation error
        """
        self.client.force_authenticate(user=self.user)

        book_data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': 9999  # Non-existent author ID
        }

        response = self.client.post(reverse('book-create'), book_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_create_with_empty_title(self):
        """
        Test creating book with empty title.

        Expected: 400 Bad Request with validation error
        """
        self.client.force_authenticate(user=self.user)

        book_data = {
            'title': '',
            'publication_year': 2020,
            'author': self.author.id
        }

        response = self.client.post(reverse('book-create'), book_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_create_with_invalid_year(self):
        """
        Test creating book with invalid publication year.

        Expected: 400 Bad Request with validation error
        """
        self.client.force_authenticate(user=self.user)

        book_data = {
            'title': 'Test Book',
            'publication_year': 'invalid_year',
            'author': self.author.id
        }

        response = self.client.post(reverse('book-create'), book_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_large_dataset_performance(self):
        """
        Test API performance with larger dataset.

        Expected: Reasonable response time for list operations
        """
        # Create multiple authors and books
        authors = []
        for i in range(10):
            authors.append(Author.objects.create(name=f"Author {i}"))

        for i in range(50):
            Book.objects.create(
                title=f"Book {i}",
                publication_year=2000 + (i % 23),
                author=authors[i % 10]
            )

        import time
        start_time = time.time()
        response = self.client.get(reverse('book-list'))
        end_time = time.time()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 50)

        # Response should be reasonably fast (less than 1 second)
        response_time = end_time - start_time
        self.assertLess(response_time, 1.0)

    def test_concurrent_book_creation(self):
        """
        Test handling of concurrent book creation requests.

        Expected: All requests should be handled correctly
        """
        self.client.force_authenticate(user=self.user)

        book_data = {
            'title': 'Concurrent Test Book',
            'publication_year': 2023,
            'author': self.author.id
        }

        # Simulate multiple concurrent requests
        responses = []
        for i in range(5):
            book_data['title'] = f'Concurrent Test Book {i}'
            response = self.client.post(reverse('book-create'), book_data)
            responses.append(response)

        # All requests should succeed
        for response in responses:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify all books were created
        self.assertEqual(Book.objects.filter(title__startswith='Concurrent Test Book').count(), 5)


class IntegrationTestCase(APITestCase):
    """
    Integration tests for complete API workflows.
    """

    def setUp(self):
        """Set up test data for integration tests."""
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        self.user = User.objects.create_user(username=f'testuser_integration_{unique_id}', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_complete_book_lifecycle(self):
        """
        Test complete book lifecycle: create author, create book, update, delete.

        Expected: All operations succeed in sequence
        """
        # Step 1: Create an author
        author_data = {'name': 'Integration Test Author'}
        author_response = self.client.post(reverse('author-list-create'), author_data)

        self.assertEqual(author_response.status_code, status.HTTP_201_CREATED)
        author_id = author_response.data['id']

        # Step 2: Create a book for the author
        book_data = {
            'title': 'Integration Test Book',
            'publication_year': 2023,
            'author': author_id
        }
        book_response = self.client.post(reverse('book-create'), book_data)

        self.assertEqual(book_response.status_code, status.HTTP_201_CREATED)
        book_id = book_response.data['book']['id']

        # Step 3: Verify book appears in author's book list
        author_detail_response = self.client.get(reverse('author-detail', kwargs={'pk': author_id}))
        self.assertEqual(len(author_detail_response.data['books']), 1)

        # Step 4: Update the book
        updated_book_data = {
            'title': 'Updated Integration Test Book',
            'publication_year': 2024,
            'author': author_id
        }
        update_response = self.client.put(
            reverse('book-update', kwargs={'pk': book_id}),
            updated_book_data
        )

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['book']['title'], 'Updated Integration Test Book')

        # Step 5: Search for the updated book
        search_response = self.client.get(reverse('book-list'), {'search': 'Updated Integration'})
        self.assertEqual(len(search_response.data), 1)

        # Step 6: Delete the book
        delete_response = self.client.delete(reverse('book-delete', kwargs={'pk': book_id}))
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)

        # Step 7: Verify book is no longer in author's book list
        final_author_response = self.client.get(reverse('author-detail', kwargs={'pk': author_id}))
        self.assertEqual(len(final_author_response.data['books']), 0)

    def test_bulk_operations_workflow(self):
        """
        Test workflow involving multiple books and authors.

        Expected: Complex operations work correctly together
        """
        # Create multiple authors
        authors = []
        for i in range(3):
            author_data = {'name': f'Bulk Author {i}'}
            response = self.client.post(reverse('author-list-create'), author_data)
            authors.append(response.data['id'])

        # Create multiple books for each author
        books = []
        for author_id in authors:
            for j in range(2):
                book_data = {
                    'title': f'Bulk Book {author_id}-{j}',
                    'publication_year': 2020 + j,
                    'author': author_id
                }
                response = self.client.post(reverse('book-create'), book_data)
                books.append(response.data['book']['id'])

        # Verify total count
        list_response = self.client.get(reverse('book-list'))
        self.assertEqual(len(list_response.data), 6)  # 3 authors × 2 books each

        # Test filtering by year
        year_filter_response = self.client.get(reverse('book-list'), {'year_from': 2021})
        self.assertEqual(len(year_filter_response.data), 3)  # One book per author from 2021

        # Test search across all books
        search_response = self.client.get(reverse('book-list'), {'search': 'Bulk'})
        self.assertEqual(len(search_response.data), 6)  # All books contain 'Bulk'

        # Test ordering
        ordered_response = self.client.get(reverse('book-list'), {'ordering': 'title'})
        titles = [book['title'] for book in ordered_response.data]
        self.assertEqual(titles, sorted(titles))
