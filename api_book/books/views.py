import requests
from datetime import datetime

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Book, Category, Author
from .serializer import BookSerializer


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        if self.request.GET.get('author'):
            return Book.objects.filter(
                authors__name__in=[
                    a.replace('"', '') for a in self.request.GET.getlist('author')
                ]).distinct()
        else:
            return Book.objects.all()


class ApiCall(APIView):
    def post(self, request):
        if request.POST.get('q', None):
            request = requests.get('https://www.googleapis.com/books/v1/volumes', params={'q': request.POST['q']})
            data = request.json()

            new_books = 0
            new_category = 0
            new_authors = 0

            for book in data['items']:
                publish_date = datetime.strptime(
                    book['volumeInfo']['publishedDate'],
                    '%Y-%m-%d'
                ).year if len(book['volumeInfo']['publishedDate']) > 4 else book['volumeInfo']['publishedDate']

                book_object, created = Book.objects.update_or_create(
                    title=book['volumeInfo']['title'],
                    published_date=publish_date,
                    average_rating=book['volumeInfo'].get('averageRating'),
                    ratings_count=book['volumeInfo'].get('ratingsCount'),
                    thumbnail=book['volumeInfo']['imageLinks']['thumbnail'],
                )
                new_books += 1 if created else 0
                if book['volumeInfo'].get('categories'):
                    for c in book['volumeInfo']['categories']:
                        category, created = Category.objects.update_or_create(name=c)
                        new_category += 1 if created else 0
                        book_object.category.add(category)

                if book['volumeInfo'].get('authors'):
                    for a in book['volumeInfo']['authors']:
                        author, created = Author.objects.update_or_create(name=a)
                        new_authors += 1 if created else 0
                        book_object.authors.add(author)

            return Response({
                'new_books': new_books,
                'new_category': new_category,
                'new_authors': new_authors,
            })
        else:
            return Response({
                'error': "q is required"
            })

"""
class BooksListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('published_date')
        return render(
            request,
            'books/bookslist.html',
            {'books': books}
        )
"""