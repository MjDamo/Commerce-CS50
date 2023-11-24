from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# Category List
class Category(models.Model):
    title = models.CharField(max_length=48, unique=True)

    def __str__(self):
        return self.title


class Listing(models.Model):
    auther = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="listing"
    )
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=300)
    image = models.ImageField(upload_to="gallery", blank=True, null=True)
    imageUrl = models.URLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isActive = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='winner')
    bid = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    highest_bidder = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bidder'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="category", null=True
    )

    def __str__(self):
        return f"{self.title}, {self.auther}, {self.category}"


class Comment(models.Model):
    auther = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name='item_comment')
    text = models.TextField(max_length=1000)
    publish = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Write by: {Comment.auther.username}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    item_bid = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='item_bid')
    bid = models.DecimalField(max_digits=12, decimal_places=2)
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Bidder: {self.bidder}, item: {self.item_bid}, bid: {self.bid}'


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"user: {self.user}, item: {self.item}"
