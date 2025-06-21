from django import forms
from .models import Book, Author, Publisher, Genre

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'price', 'isbn', 'publication_date', 
                 'pages', 'cover_image', 'stock_quantity', 'language', 
                 'authors', 'publishers', 'genres']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
        } 