from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200, default='DEFAULT VALUE')
    starting_price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(blank=True, upload_to="auctions/images/", default="images/no-image.jpg")
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listed_by")
    category = models.CharField(max_length=64)
    active_listing = models.BooleanField()

class Bid(models.Model):
    user = models.ManyToManyField(User, blank=True)
    listing_title = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid_price = models.DecimalField(max_digits=7, decimal_places=2)
    time_of_bid = models.IntegerField() # not sure

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user", default=1)
    content = models.CharField(max_length=200)
    listings = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comment_listing", default=1)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user", default=1)
    listings = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlist_listing", default=1)
    watchlist = models.BooleanField()