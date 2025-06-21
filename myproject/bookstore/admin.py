from django.contrib import admin
from .models import (
    Author, Publisher, Genre, Book, BookAuthor, BookPublisher, BookGenre,
    Country, City, Address, Cart, CartItem, Order, OrderItem, Review
)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1

class BookPublisherInline(admin.TabularInline):
    model = BookPublisher
    extra = 1

class BookGenreInline(admin.TabularInline):
    model = BookGenre
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock_quantity', 'publication_date')
    list_filter = ('publication_date', 'language')
    search_fields = ('title', 'isbn')
    inlines = [BookAuthorInline, BookPublisherInline, BookGenreInline]

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country',)
    search_fields = ('name',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'city', 'street')
    list_filter = ('country', 'city')
    search_fields = ('street', 'postal_code')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation_date', 'last_update_date')
    list_filter = ('creation_date',)
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    inlines = [OrderItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('comment',) 