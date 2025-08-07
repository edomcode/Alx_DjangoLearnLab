# Advanced Features and Security - Custom User Model

This Django project demonstrates the implementation of a custom user model with additional fields and comprehensive admin integration.

## Project Overview

This project extends Django's default user authentication system by implementing a custom user model that includes additional fields beyond the standard Django User model.

## Custom User Model Features

### CustomUser Model
Located in `bookshelf/models.py`, the CustomUser model extends `AbstractUser` and includes:

- **date_of_birth**: DateField - User's date of birth (optional)
- **profile_photo**: ImageField - User's profile photo (optional, uploads to 'profile_photos/')
- All standard Django User fields (username, email, password, etc.)

### CustomUserManager
A custom user manager that handles:
- **create_user()**: Creates regular users with proper field handling
- **create_superuser()**: Creates administrative users with required permissions

## Admin Integration

### CustomUserAdmin
Located in `bookshelf/admin.py`, provides:
- Enhanced admin interface for managing custom users
- Additional fields displayed in list view (username, email, date_of_birth, etc.)
- Filtering capabilities by staff status, active status, and date of birth
- Search functionality across username, name, and email fields
- Custom fieldsets for organized form layout
- Support for adding new users with custom fields

## Configuration

### Settings Configuration
In `library_config/settings.py`:
```python
AUTH_USER_MODEL = 'bookshelf.CustomUser'
```

This setting tells Django to use our custom user model instead of the default User model.

## Database Models

### Relationship App Models
The project also includes models from the relationship app:
- **Author**: Book authors
- **Book**: Books with author relationships
- **Library**: Libraries containing books
- **Librarian**: Library staff with one-to-one library relationships
- **UserProfile**: User profiles with role-based access (updated to use CustomUser)

## Testing

### Test Script
`test_custom_user.py` provides comprehensive testing of:
- Creating regular users with custom fields
- Creating superusers with administrative privileges
- Querying and displaying user information
- Verifying custom field functionality

## Installation and Setup

1. **Install Dependencies**:
   ```bash
   pip install Django Pillow
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

5. **Test Custom User Model**:
   ```bash
   python test_custom_user.py
   ```

## Key Implementation Details

### Step 1: Custom User Model
- Extended `AbstractUser` instead of `AbstractBaseUser` for easier integration
- Added `date_of_birth` and `profile_photo` fields
- Implemented proper `__str__` method and Meta class

### Step 2: Settings Configuration
- Set `AUTH_USER_MODEL` to point to the custom user model
- Ensures all Django components use the custom user model

### Step 3: Custom User Manager
- Implemented `create_user` and `create_superuser` methods
- Proper handling of additional fields during user creation
- Email normalization and password hashing

### Step 4: Admin Integration
- Extended `UserAdmin` to include custom fields
- Configured list display, filters, and search fields
- Added custom fieldsets for organized admin forms

### Step 5: Model Updates
- Updated existing models to use `get_user_model()` for proper user model references
- Ensured compatibility with the custom user model

## Security Considerations

- Password validation remains intact
- User permissions and groups functionality preserved
- Admin interface security maintained
- Custom fields properly validated and sanitized

## File Structure

```
advanced_features_and_security/
├── bookshelf/
│   ├── models.py          # CustomUser and CustomUserManager
│   ├── admin.py           # CustomUserAdmin configuration
│   └── migrations/        # Database migrations
├── relationship_app/      # Existing relationship models
├── library_config/        # Project settings
├── test_custom_user.py    # Testing script
└── README.md             # This file
```

## Usage Examples

### Creating Users Programmatically
```python
from bookshelf.models import CustomUser
from datetime import date

# Create regular user
user = CustomUser.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='secure_password',
    date_of_birth=date(1990, 1, 1)
)

# Create superuser
admin = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin_password',
    date_of_birth=date(1985, 5, 15)
)
```

### Admin Interface
Access the admin interface at `/admin/` to:
- View and manage all users
- Filter users by various criteria
- Search users by username, name, or email
- Add new users with custom fields
- Edit existing user profiles

## Benefits of Custom User Model

1. **Extensibility**: Easy to add more fields as requirements grow
2. **Consistency**: Single user model across the entire application
3. **Admin Integration**: Seamless management through Django admin
4. **Backward Compatibility**: Maintains all Django authentication features
5. **Future-Proof**: Easier to modify than trying to extend the default User model later

This implementation provides a solid foundation for applications requiring user attributes beyond Django's built-in user model while maintaining all the security and functionality of Django's authentication system.