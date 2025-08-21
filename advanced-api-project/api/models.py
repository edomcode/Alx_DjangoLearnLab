from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Author model represents a book author in the system.

    This model stores basic information about authors and establishes
    a one-to-many relationship with the Book model, where one author
    can have multiple books.

    Fields:
        name: A string field to store the author's full name
    """
    name = models.CharField(max_length=100, help_text="The full name of the author")

    def __str__(self):
        """String representation of the Author model"""
        return self.name

    class Meta:
        """Meta options for the Author model"""
        ordering = ['name']  # Order authors alphabetically by name


class Book(models.Model):
    """
    Book model represents a book in the system.

    This model stores information about books and establishes a foreign key
    relationship with the Author model. Each book belongs to one author,
    but an author can have multiple books (one-to-many relationship).

    Fields:
        title: A string field for the book's title
        publication_year: An integer field for the year the book was published
        author: A foreign key linking to the Author model
    """
    title = models.CharField(max_length=200, help_text="The title of the book")
    publication_year = models.IntegerField(help_text="The year the book was published")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The author who wrote this book"
    )

    def __str__(self):
        """String representation of the Book model"""
        return f"{self.title} ({self.publication_year}) by {self.author.name}"

    class Meta:
        """Meta options for the Book model"""
        ordering = ['-publication_year', 'title']  # Order by publication year (newest first), then title
