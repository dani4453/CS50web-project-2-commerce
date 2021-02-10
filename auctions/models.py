from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=300)
    bidprice = models.DecimalField(max_digits=6, decimal_places=2)
    datetime = models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="%(class)s_category", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_user", null=True)
    status = models.BooleanField(default=True, db_index=True)
    watch = models.ManyToManyField(User, blank=True, related_name="%(class)s_watch")

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="%(class)s_listing")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    bidprice = models.DecimalField(max_digits=6, decimal_places=2)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="%(class)s_listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_user", null=True)
    datetime = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=300)