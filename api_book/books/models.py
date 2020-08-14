from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

class Author(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=128)
    authors = models.ManyToManyField('Author')
    published_date = models.IntegerField(null=True)
    categories = models.ManyToManyField(Category, related_name='books')
    avarage_rating = models.IntegerField(null=True)
    ratings_count = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to='book_image',height_field=None, width_field=None, max_length=100, null=True)

    def __str__(self):
        return f'{self.title}: {self.authors}'
