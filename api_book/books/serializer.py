from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = [
            'title',
            'authors',
            'published_date',
            'average_rating',
            'ratings_count',
            'thumbnail',

        ]