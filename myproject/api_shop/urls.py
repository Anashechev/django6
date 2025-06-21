from django.urls import path, include
from rest_framework import routers
from .views import (
    BookViewSet,
    AuthorViewSet,
    PublisherViewSet,
    GenreViewSet,
    ReviewViewSet,
    api_root_admin_only,
    user_profile,
    LoginView,
    RegisterView,
    book_reviews,
    create_review,
    update_review,
    delete_review
)

router = routers.DefaultRouter()
router.register('books', BookViewSet, basename='book')
router.register('authors', AuthorViewSet, basename='author')
router.register('publishers', PublisherViewSet, basename='publisher')
router.register('genres', GenreViewSet, basename='genre')
router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='api-login'),
    path('auth/register/', RegisterView.as_view(), name='api-register'),
    path('user-profile/', user_profile, name='user-profile'),
    path('books/<int:book_id>/reviews/', book_reviews, name='book-reviews'),
    path('books/<int:book_id>/reviews/create/', create_review, name='create-review'),
    path('reviews/<int:review_id>/update/', update_review, name='update-review'),
    path('reviews/<int:review_id>/delete/', delete_review, name='delete-review'),
    path('', api_root_admin_only, name='api-root'),
    path('', include(router.urls)),
]