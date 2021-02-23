from django.contrib import admin
from .models import AuctionListing, Bid, Comment, User, Watchlist

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username",)

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image", "listed_by", "category", "active_listing", "starting_price")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing_title", "bid_price",)
    # filter_horizontal = ("user",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "listings")
    # filter_horizontal = ("id", "user",)

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "listings", "watchlist")
    # filter_horizontal = ("listings",)

admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Watchlist, WatchlistAdmin)