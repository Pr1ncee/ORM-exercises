from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_day = models.DateTimeField()


class Publisher(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    publish_date = models.DateTimeField()
    price = models.FloatField()


class Sales(models.Model):
    date = models.DateTimeField()
    total_sold_usd = models.FloatField()
