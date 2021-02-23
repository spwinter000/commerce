from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
import datetime 

from .models import User, AuctionListing, Bid, Comment, Watchlist

class NewCreateListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label="Title", required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'input'}), label="Description", required=True)
    starting_price = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    category = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label="Category", required=True)
    image = forms.FileField()

def index(request):
    active_listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
    })

def listing(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)

    bid_count = Bid.objects.filter(listing_title=listing_id).count

    bids = Bid.objects.filter(listing_title=listing_id)

    # watchlist
    watchlist = Watchlist.objects.filter(user=request.user.id)
    watchlist_listings = [item.listings for item in watchlist]

    # get highest bid, if no bid on listing set starting price equal to bid
    highest_bid = Bid.objects.filter(listing_title=listing_id)
    if highest_bid.exists():
        highest_bid = highest_bid.order_by('-bid_price').first()
        highest_bid = highest_bid.bid_price
    else: 
        highest_bid = listing.starting_price

    # get user of highest/winning bid
    winning_bidder = Bid.objects.filter(listing_title=listing_id)
    if winning_bidder.exists():
        winning_bidder = winning_bidder.order_by('-bid_price').first()
        winning_bidder = winning_bidder.user.first()
    else: 
        winning_bidder = listing.listed_by

    # minimum bid allowed
    minimum_bid = float(highest_bid)+0.01
    minimum_bid = round(minimum_bid, 2)

    # comments and number of comments
    comments = Comment.objects.filter(listings=listing_id)
    comment_count = len(comments)

    return render(request, "auctions/listing.html", {
        "highest_bid": highest_bid,
        "minimum_bid" : minimum_bid,
        "winning_bidder": winning_bidder,
        "bids": bids,
        "bid_count": bid_count,
        "watchlist_listings": watchlist_listings,
        "listing": listing,
        "comments": comments,
        "comment_count": comment_count
    })

def categories(request):
    listings = AuctionListing.objects.filter()
    unique_categories = []
    categories = [listing.category for listing in listings]
    for category in categories:
        if category not in unique_categories:
            unique_categories.append(category)
    return render(request, "auctions/categories.html", {
        "listings": listings,
        "unique_categories": unique_categories,
        "categories": categories
    })

def category_listings(request, category):
    listings = AuctionListing.objects.filter(category=category)
    return render(request, "auctions/category_listings.html", {
        "listings": listings
    })

def place_bid(request, listing_id):
    user = request.user
    if request.method == 'POST':
        bid = request.POST["bid_price"]
        time_of_bid=638    
        listing = AuctionListing.objects.get(pk=listing_id) # this was moved from top to here
        highest_bid = Bid.objects.filter(listing_title=listing_id)
        if highest_bid.exists():
            highest_bid = highest_bid.order_by('-bid_price').first()
            highest_bid = highest_bid.bid_price  
        else: 
            highest_bid = listing.starting_price
        if float(highest_bid) >= float(bid):
            return HttpResponseRedirect(reverse("listing", args=(listing.id, )))
        else:
            new_bid = Bid(listing_title=listing, bid_price=bid, time_of_bid=time_of_bid)
            new_bid.save()
            new_bid.user.add(user)
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def create_listing(request):
    listed_by_id = request.user.id
    title = request.POST.get('title')
    description = request.POST.get('description')
    starting_price = request.POST.get('starting_price')
    category = request.POST.get('category')
    if request.method == "POST":
        image = request.FILES['image'] #image data is only accessible this way
        new_listing = AuctionListing.objects.create(listed_by_id=listed_by_id,title=title, description=description, starting_price=starting_price, active_listing=True, category=category, image=image)
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html", {
        "form": NewCreateListingForm()
    })

def watchlist(request, user_id):
    watchlist = Watchlist.objects.filter(user=user_id)
    watchlist_listings = [listing.listings for listing in watchlist]
    watchlist_count = len(watchlist_listings)
    return render(request, "auctions/watchlist.html", {
        "watchlist_listings": watchlist_listings,
        "watchlist": watchlist,
        "watchlist_count": watchlist_count
    })

def add_to_watchlist(request, listing_id):
    user = request.user
    listing = AuctionListing.objects.get(pk=listing_id)
    watchlist = True
    if request.method == 'POST': 
        new_watchlist_item = Watchlist(user=user, listings=listing, watchlist=watchlist)
        new_watchlist_item.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id, )))
    return render(request, "auctions/watchlist.html")

def remove_from_watchlist(request, listing_id):
    watchlist = Watchlist.objects.filter(listings=listing_id).delete()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def close_listing(request, listing_id):
    # user of highest bid is winner
    # listing becomes no longer active
    listing = AuctionListing.objects.get(pk=listing_id)
    listed_by = listing.listed_by
    if request.method == 'POST':
        listing.active_listing = False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id, )))
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def create_comment(request, listing_id):
    user = request.user
    if request.method == 'POST':
        listing = AuctionListing.objects.get(pk=listing_id)
        comment = request.POST.get("comment")
        # create new comment
        new_comment = Comment(user=user, content=comment, listings=listing)
        new_comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id, )))
    return render(request, "auctions/listing.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
