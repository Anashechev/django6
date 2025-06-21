from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.text import slugify
from unidecode import unidecode

def cover_image_upload_to(instance, filename):
    name, ext = os.path.splitext(filename)
    # Транслитерируем имя файла и убираем лишние символы
    safe_name = slugify(unidecode(name))
    return f'book_covers/{safe_name}{ext}'

class Author(models.Model):
    name = models.CharField('Имя', max_length=50)
    biography = models.TextField('Биография')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    price = models.FloatField('Цена')
    isbn = models.CharField('ISBN', max_length=13)
    publication_date = models.DateField('Дата публикации')
    pages = models.IntegerField('Количество страниц')
    cover_image = models.ImageField('Обложка', upload_to=cover_image_upload_to, null=True, blank=True)
    stock_quantity = models.IntegerField('Количество на складе')
    language = models.CharField('Язык', max_length=50)
    authors = models.ManyToManyField(Author, through='BookAuthor', verbose_name='Авторы')
    publishers = models.ManyToManyField(Publisher, through='BookPublisher', verbose_name='Издательства')
    genres = models.ManyToManyField(Genre, through='BookGenre', verbose_name='Жанры')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Автор книги'
        verbose_name_plural = 'Авторы книг'

class BookPublisher(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name='Издательство')

    class Meta:
        verbose_name = 'Издательство книги'
        verbose_name_plural = 'Издательства книг'

class BookGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')

    class Meta:
        verbose_name = 'Жанр книги'
        verbose_name_plural = 'Жанры книг'

class Country(models.Model):
    name = models.CharField('Название', max_length=150)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField('Название', max_length=150)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    street = models.CharField('Улица', max_length=50)
    postal_code = models.CharField('Почтовый индекс', max_length=50)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return f"{self.street}, {self.city.name}, {self.country.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    creation_date = models.DateField('Дата создания', auto_now_add=True)
    last_update_date = models.DateField('Дата последнего обновления', auto_now=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    quantity = models.IntegerField('Количество')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f"{self.quantity} шт. {self.book.title} в корзине"

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'В обработке'),
        ('PROCESSING', 'Обрабатывается'),
        ('SHIPPED', 'Отправлен'),
        ('DELIVERED', 'Доставлен'),
        ('CANCELLED', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    total_price = models.FloatField('Общая стоимость')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='PENDING')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Адрес')
    order_date = models.DateField('Дата заказа', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ {self.id} от {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    quantity = models.IntegerField('Количество')
    price_at_order_time = models.FloatField('Цена на момент заказа')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return f"{self.quantity} шт. {self.book.title} в заказе {self.order.id}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    rating = models.IntegerField('Оценка')
    comment = models.TextField('Комментарий')
    review_date = models.DateField('Дата отзыва', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв от {self.user.username} на книгу {self.book.title}" 