from rest_framework import serializers
from bookstore.models import Book, Author, Publisher, Genre, Review


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'description']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    publishers = PublisherSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    cover_image = serializers.ImageField(required=False, allow_null=True)
    publication_date = serializers.DateField(format="%Y-%m-%d", required=False)
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'description',
            'price',
            'isbn',
            'publication_date',
            'pages',
            'cover_image',
            'stock_quantity',
            'language',
            'authors',
            'publishers',
            'genres',
            'is_admin',
        ]

    def get_is_admin(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return request.user.is_staff or request.user.is_superuser
        return False


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = serializers.StringRelatedField(read_only=True)
    review_date = serializers.DateField(format="%Y-%m-%d", required=False, read_only=True)
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'book',
            'rating',
            'comment',
            'review_date',
            'can_edit',
        ]

    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            # Пользователь может редактировать свой отзыв или является админом
            return request.user == obj.user or request.user.is_staff or request.user.is_superuser
        return False

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оценка должна быть от 1 до 5")
        return value