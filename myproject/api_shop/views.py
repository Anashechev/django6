from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from bookstore.models import Book, Author, Publisher, Genre, Review
from .serializer import (
    BookSerializer,
    AuthorSerializer,
    PublisherSerializer,
    GenreSerializer,
    ReviewSerializer
)
from .permissions import IsAdminOrReadOnly, ImageHandlingMixin
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Q

@api_view(['GET'])
def api_root_admin_only(request, format=None):
    if not request.user.is_staff:
        raise Http404()
    from rest_framework.routers import DefaultRouter
    # Собираем ссылки на все viewset-ы
    return Response({
        'books': reverse('book-list', request=request, format=format),
        'authors': reverse('author-list', request=request, format=format),
        'publishers': reverse('publisher-list', request=request, format=format),
        'genres': reverse('genre-list', request=request, format=format),
        'reviews': reverse('review-list', request=request, format=format),
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
    })

class BookViewSet(ImageHandlingMixin, viewsets.ModelViewSet):
    """ViewSet для работы с книгами"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
        return queryset

class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с авторами"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

class PublisherViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с издателями"""
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с жанрами"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с отзывами"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        book_id = self.request.query_params.get('book_id')
        if book_id:
            return Review.objects.filter(book_id=book_id)
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'detail': 'ok'})
        return Response({'detail': 'Неверный логин или пароль'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'detail': 'Имя пользователя и пароль обязательны'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'detail': 'Пользователь с таким именем уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return Response({'detail': 'ok'})

@api_view(['GET'])
@permission_classes([AllowAny])
def book_reviews(request, book_id):
    """Получить отзывы для конкретной книги"""
    reviews = Review.objects.filter(book_id=book_id)
    serializer = ReviewSerializer(reviews, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, book_id):
    """Создать отзыв для книги"""
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'detail': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    # Проверяем, не оставлял ли пользователь уже отзыв на эту книгу
    if Review.objects.filter(user=request.user, book=book).exists():
        return Response({'detail': 'Вы уже оставляли отзыв на эту книгу'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, book=book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request, review_id):
    """Редактировать отзыв"""
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({'detail': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)
    
    # Проверяем, что пользователь редактирует свой отзыв или является админом
    if review.user != request.user and not (request.user.is_staff or request.user.is_superuser):
        return Response({'detail': 'У вас нет прав для редактирования этого отзыва'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = ReviewSerializer(review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, review_id):
    """Удалить отзыв"""
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({'detail': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)
    
    # Проверяем, что пользователь удаляет свой отзыв или является админом
    if review.user != request.user and not (request.user.is_staff or request.user.is_superuser):
        return Response({'detail': 'У вас нет прав для удаления этого отзыва'}, status=status.HTTP_403_FORBIDDEN)
    
    review.delete()
    return Response({'detail': 'Отзыв удален'}, status=status.HTTP_204_NO_CONTENT)