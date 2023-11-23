from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=48, unique=True)

    def __str__(self):
        return self.title


class Listing(models.Model):
    auther = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="user"
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="gallery", blank=True, null=True)
    imageUrl = models.URLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isActive = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bidder = models.ForeignKey(
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
