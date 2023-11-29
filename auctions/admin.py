from django.contrib import admin
from .models import Category, Listing, Watchlist, Comment, Bid


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'auther', 'price', 'category', 'date', 'isActive']


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'item']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['item', 'auther', 'text']


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_bid', 'bid']
