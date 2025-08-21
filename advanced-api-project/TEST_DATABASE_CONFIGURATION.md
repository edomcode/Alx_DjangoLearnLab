# Test Database Configuration

## Overview

This document explains how the separate test database is configured to avoid impacting production or development data during unit testing.

## Database Configuration

### Development Database
- **File**: `db.sqlite3`
- **Purpose**: Development and production data
- **Location**: Project root directory

### Test Database
- **File**: `test_db.sqlite3`
- **Purpose**: Isolated testing environment
- **Location**: Project root directory
- **Auto-managed**: Created and destroyed automatically during tests

## Settings Configuration

The database configuration in `advanced_api_project/settings.py` includes explicit test database settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'TEST': {
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }
}
```

### Key Features:

1. **Separate Database File**: Test database uses `test_db.sqlite3` instead of `db.sqlite3`
2. **Automatic Management**: Django automatically creates and destroys the test database
3. **Data Isolation**: Test data never affects development or production data
4. **Clean State**: Each test run starts with a fresh, empty database

## How It Works

### Test Database Lifecycle

1. **Before Tests**: Django creates `test_db.sqlite3` with the same schema as the main database
2. **During Tests**: All database operations use the test database
3. **After Tests**: Django destroys `test_db.sqlite3` automatically

### Test Data Management

- **Fresh Start**: Each test class gets a clean database
- **Transaction Rollback**: Each test method runs in a transaction that's rolled back
- **Isolation**: Tests don't interfere with each other's data

## Authentication Methods in Tests

The test suite demonstrates both authentication methods supported by Django:

### 1. Force Authentication (Token-based)
```python
self.client.force_authenticate(user=self.user)
```
- Used for API token authentication
- Bypasses normal authentication flow
- Ideal for testing API endpoints directly

### 2. Session Authentication (Login-based)
```python
login_successful = self.client.login(
    username=self.user.username,
    password='testpass123'
)
```
- Uses Django's session-based authentication
- Simulates real user login process
- Tests the complete authentication flow

## Test Methods Using client.login

The following test methods demonstrate `self.client.login` usage:

### BookAPITestCase
- `test_book_create_with_login()` - Create book using session authentication
- `test_book_update_with_login()` - Update book using session authentication  
- `test_book_delete_with_login()` - Delete book using session authentication

### AuthorAPITestCase
- `test_author_create_with_login()` - Create author using session authentication

## Benefits of Separate Test Database

### 1. Data Safety
- **No Risk**: Production/development data is never modified during testing
- **Isolation**: Tests can create, modify, and delete data without consequences
- **Consistency**: Tests always start with the same clean state

### 2. Performance
- **Speed**: SQLite test database is fast for unit tests
- **Parallel Testing**: Multiple test processes can run simultaneously
- **No Cleanup**: No need to manually clean up test data

### 3. Reliability
- **Predictable**: Tests always run against known data state
- **Repeatable**: Same results every time tests are run
- **Independent**: Tests don't depend on existing data

## Running Tests

### Commands
```bash
# Run all tests (uses test database automatically)
python manage.py test api

# Run specific test file
python manage.py test api.test_views

# Run with verbose output to see database operations
python manage.py test api.test_views --verbosity=2

# Run specific test method
python manage.py test api.test_views.BookAPITestCase.test_book_create_with_login
```

### Test Database Creation
When you run tests, you'll see output like:
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..................................
----------------------------------------------------------------------
Ran 42 tests in 15.234s

OK
Destroying test database for alias 'default'...
```

## Verification

### Check Database Files
After running tests, you can verify the separation:

```bash
# List database files
ls -la *.sqlite3

# You should see:
# db.sqlite3      (development database - unchanged)
# test_db.sqlite3 (may exist temporarily during tests)
```

### Test Database Content
During test execution, the test database contains:
- All model tables (Author, Book, User, etc.)
- Test data created by setUp() methods
- No production or development data

## Best Practices

### 1. Test Data Creation
- Use `setUp()` method to create test data
- Create minimal data needed for each test
- Use unique identifiers to avoid conflicts

### 2. Database Operations
- Don't rely on existing data in tests
- Create all necessary test data explicitly
- Test both success and failure scenarios

### 3. Authentication Testing
- Test both authenticated and unauthenticated scenarios
- Use appropriate authentication method for each test
- Verify permission enforcement

## Troubleshooting

### Common Issues
1. **Permission Errors**: Ensure test database directory is writable
2. **Migration Issues**: Run `python manage.py migrate` before testing
3. **Data Conflicts**: Use unique test data to avoid conflicts

### Solutions
- Check file permissions in project directory
- Ensure all migrations are applied
- Use UUIDs or timestamps for unique test data

## Conclusion

The separate test database configuration ensures:
- ✅ Complete isolation from production/development data
- ✅ Safe testing environment for all operations
- ✅ Consistent and repeatable test results
- ✅ Support for both authentication methods
- ✅ Automatic database lifecycle management

This setup provides a robust foundation for comprehensive API testing without any risk to production data.
