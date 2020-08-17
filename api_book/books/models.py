from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256)
    authors = models.ManyToManyField('Author')
    category = models.ManyToManyField('Category')
    published_date = models.IntegerField()
    average_rating = models.FloatField(default=0, null=True)
    ratings_count = models.IntegerField(default=None, null=True)
    thumbnail = models.URLField()


class Author(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=128)