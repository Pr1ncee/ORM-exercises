from django.contrib import admin

from main.models import Author, Book, Sales, Publisher

admin.register([Author, Book, Sales, Publisher])
