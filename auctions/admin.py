from django.contrib import admin
from .models import Category, Listing


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'auther', 'price', 'category', 'date', 'isActive']
    