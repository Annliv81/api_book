
from .models import Book
from rest_framework import viewsets
from .serializer import BookSerializer
from rest_framework.views import APIView
import requests


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ApiCall(APIView):
    def get(self, request):
        request = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit', params={'q':'war'})
        data = request.json()
        print(data)

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