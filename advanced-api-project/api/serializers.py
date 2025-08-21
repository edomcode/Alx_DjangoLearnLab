from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the Book model.
    
    This serializer handles the serialization of Book instances and includes
    custom validation to ensure the publication_year is not in the future.
    
    Fields:
        - All fields from the Book model (title, publication_year, author)
    
    Custom Validation:
        - publication_year: Validates that the year is not in the future
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the Author model with nested Book serialization.
    
    This serializer includes the author's basic information and dynamically
    serializes all related books using the BookSerializer. The relationship
    is handled through Django's related_name='books' on the Book model's
    foreign key to Author.
    
    Fields:
        - name: The author's name
        - books: A nested serialization of all books by this author
    
    Relationship Handling:
        The 'books' field uses the related_name defined in the Book model's
        foreign key relationship. This allows us to access all books by an
        author through the reverse relationship. The many=True parameter
        indicates that an author can have multiple books.
    """
    
    # Nested serializer for related books
    # The 'books' field corresponds to the related_name in the Book model
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
    
    def to_representation(self, instance):
        """
        Custom representation method to provide additional control over
        the serialized output if needed.
        
        This method can be used to modify the serialized data before
        it's returned to the client.
        
        Args:
            instance (Author): The Author instance being serialized
            
        Returns:
            dict: The serialized representation of the Author
        """
        representation = super().to_representation(instance)
        
        # Add the count of books for convenience
        representation['books_count'] = len(representation['books'])
        
        return representation
