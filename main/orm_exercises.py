from datetime import datetime

from django.db.models import Count, Q, Sum

from main.models import Author, Book, Publisher, Sales


def books_published_after_2000():
    """Посчитать количесто книг выпущенных после 2000 года"""
    return Book.objects.filter(publish_date__gt=datetime(2000, 12, 31)).count()


def books_where_not_a_in_author_name():
    """Вывести только имена авторов для книг которые не содержат букву А в своем имени"""
    return Book.objects.exclude(name__icontains='A').values('name')


def get_the_latest_book_and_the_first():
    """Получить последнюю опубликованную книгу двумя способами. Аналогично с первой опубликованной книгой"""
    latest_book_1 = Book.objects.all().latest('publish_date')
    latest_book_2 = Book.objects.all().order_by('-publish_date').first()

    first_book_1 = Book.objects.all().earliest('publish_date')
    first_book_2 = Book.objects.all().order_by('publish_date').first()

    results = {
        'The first book': (latest_book_1, latest_book_2),
        'The latest book': (first_book_1, first_book_2)
    }
    return results


def authors_books():
    """Посчитать для каждого автора его количество книг"""
    return [{author.name: author.books.count()} for author in Author.objects.all()]


def authors_which_have_book_gt_5():
    """Вывести авторов у которых количество книг больше 5, используя метод alias"""
    return Author.objects.alias(number_of_books=Count('books')).filter(number_of_books__gt=5)


def book_for_every_year():
    """Вывести по одному имени книги для каждого года"""
    return Book.objects.all().distinct('publish_date__year').values('name')


def publishers_with_select_related():
    """Одним запросом получить для книг имена паблишеров, не подгружая остальные поля из связанной модели"""
    return Book.objects.select_related('publisher').only('publisher_name')


def get_books_fields_for_author_except_price(pk: int):
    """В один запрос для автора выбрать список всех книг исключая их цену"""
    return Author.objects.get(pk=pk).books.all().values('name', 'authors', 'publisher', 'publish_date')


def get_all_author_objects_using_raw_sql():
    """С помощью Django ORM написать сырой SQL запрос для получения всех объектов автора"""
    return [author for author in Author.objects.raw('SELECT * FROM main_author')]


def does_book_exist():
    """Проверить существует ли книга с id=100"""
    return Book.objects.filter(pk=100).exists()


def get_publishers_whose_books_authors_born_between_16_and_18_centuries():
    """Получить паблишеров у авторов книг которых день рождения в 16 или 18 веке"""
    return Publisher.objects.filter(
            Q(books__authors__birth_day__range=(datetime(1500, 1, 1), datetime(1599, 12, 31))) |
            Q(books__authors__birth_day__range=(datetime(1700, 1, 1), datetime(1799, 12, 31)))
    )


def get_or_create_book(
        authors: list[Author],
        publisher: Publisher,
        publish_date: datetime,
        price: int,
        name: str = 'Эйафьядлаёкюдель'
):
    """Создать если не существует книга с именем Эйафьядлаёкюдель"""
    return Book.objects.get_or_create(
        name=name,
        authors=authors,
        publisher=publisher,
        publish_date=publish_date,
        price=price)


def create_5_books_with_one_query(books_list: list[Book, Book, Book, Book, Book]):
    """Создать 5 книг одном запросом"""
    return Book.objects.bulk_create(books_list)


def get_the_oldest_author():
    """Получить год рождения самого древнего автора"""
    return Author.objects.earliest('birth_day').birth_day.year


def richest_publisher_by_books_cost():
    """Найти самое богатое издания по общей стоимости книг"""
    Publisher.objects.annotate(books_cost=Sum('books__price')).latest('books__price')


def books_which_price_more_than_total_sold_usd_on_specific_date():
    """Показать список книг цена которых больше цены продаж за 20 февраля 2002 года"""
    target_date = datetime(2002, 2, 20)
    return Book.objects.filter(price__gt=Sales.objects.get(date=target_date).total_sold_usd)
