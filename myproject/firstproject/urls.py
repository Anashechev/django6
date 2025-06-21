from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.index, name='info'),
    path('clothes/', views.ClothesListView.as_view(), name='clothes_list'),
    path('clothes/create/', views.ClothesCreateView.as_view(), name='clothes_create'),
    path('clothes/<int:pk>/', views.ClothesDetailView.as_view(), name='clothes_detail'),
    path('clothes/<int:pk>/update/', views.ClothesUpdateView.as_view(), name='clothes_update'),
    path('clothes/<int:pk>/delete/', views.ClothesDeleteView.as_view(), name='clothes_delete'),
]