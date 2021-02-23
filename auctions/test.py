def place_bid(request, listing_id):
    # get bids on that particular listing
    # @logged_in
    form = NewBidForm(request.POST)
    listing = AuctionListing.objects.get(id=listing_id)
    if request.method == 'POST':
        if form.is_valid():
            bid = form.cleaned_data["bid_price"]
            user = request.user
            listing_title = AuctionListing.objects.get(id=listing_id)
            # listing_title = Bid.objects.filter(listing_title=listing_id)
            # bid_price = request.POST["bid_price"]
            time_of_bid = "null"
            if bid <= listing.starting_price:
                return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))

                # return HttpResponse("Bid too small")
            else:
                bid = Bid(listing_title=listing_id, bid_price=bid, time_of_bid=time_of_bid)
                # bid = Bid(listing_title=f"AuctionListing object ({listing_id})", bid_price=bid, time_of_bid=time_of_bid)
                bid.user.add(user)
                bid.save()
                return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))
        else: 
            return render(request, "auctions/listing.html")
    # else:
        # bids = Bid.objects.filter(listing_title=listing_id)
        # # bid_price = bids.bid_price
        # bid_count = len(bids)

        # bid_prices = [bid.bid_price for bid in bids]

        # return render(request, "auctions/place_bid.html", {
        #     # "active_listings": active_listings,
        #     "bid_prices": bid_prices,
        #     "bid_count": bid_count,
        #     "listing" : listing
        # })