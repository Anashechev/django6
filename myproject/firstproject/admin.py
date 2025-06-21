from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Collection)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Clothes)
class CategoryAdmin(admin.ModelAdmin):
    pass