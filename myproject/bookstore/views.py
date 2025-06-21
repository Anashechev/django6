from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from .models import Book, Author, Publisher, Genre
from .forms import BookForm
from django.urls import reverse_lazy

class BookListView(ListView):
    template_name = 'bookstore/book_list.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class BookDetailView(DetailView):
    template_name = 'bookstore/book_detail.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'bookstore/book_form.html'
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'bookstore/book_form.html'
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'bookstore/book_confirm_delete.html'
    success_url = reverse_lazy('bookstore:book_list')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

def home(request):
    featured_books = Book.objects.all()[:6]  # Get 6 featured books
    return render(request, 'bookstore/home.html', {'featured_books': featured_books})

def login_view(request):
    return render(request, 'bookstore/auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('bookstore:login')

def register_view(request):
    return render(request, 'bookstore/auth/register.html')

def profile_view(request):
    return render(request, 'bookstore/auth/profile.html')

def password_change_view(request):
    if not request.user.is_authenticated:
        return redirect('bookstore:login')
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')
        if not request.user.check_password(old_password):
            messages.error(request, 'Старый пароль неверен')
        elif new_password != new_password2:
            messages.error(request, 'Новые пароли не совпадают')
        elif len(new_password) < 6:
            messages.error(request, 'Пароль должен быть не менее 6 символов')
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Пароль успешно изменён. Войдите заново.')
            return redirect('bookstore:login')
    return render(request, 'bookstore/auth/password_change.html')

def custom_404_view(request, exception):
    return render(request, 'bookstore/404.html', status=404) 