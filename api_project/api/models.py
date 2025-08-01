from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField(default='2000-01-01')  # Add default here

    def __str__(self):
        return self.title
