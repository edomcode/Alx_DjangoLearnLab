from django.contrib import admin
from .models import Book  # Replace with your actual model name

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')  # Customize fields
    search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin)
