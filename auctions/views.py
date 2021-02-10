from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment

def index(request):
    return render(request, "auctions/index.html", {
        "title": "Active Listings",
        "listings": Listing.objects.exclude(status=False).all()
    })

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

@login_required
def newlisting(request):
    if request.method == "POST":
        titleField = request.POST["title"]
        descriptionField = request.POST["description"]
        bidpriceField = request.POST["bidprice"]
        imageField = request.POST["img"]
        category = Category.objects.get(pk=int(request.POST["category"]))
        user = request.user
        listing = Listing(title=titleField, description=descriptionField, bidprice=bidpriceField, image=imageField, category= category, user=user)
        listing.save()
        return render(request, "auctions/newlisting.html", {
            "message": "Create New Listing",
            "pop_up" : titleField,
            "categories": Category.objects.all()
        })
    else:
        return render(request, "auctions/newlisting.html", {
            "message": "Create New Listing",
            "categories": Category.objects.all()
        })

@login_required
def newcategory(request):
    if request.method == "POST":
        categoryField = request.POST["category"]
        category = Category(category=categoryField)
        category.save()
        return render(request, "auctions/newcategory.html", {
            "message": "Create New Category",
            "pop_up" : categoryField
        })
    else:
        return render(request, "auctions/newcategory.html", {
            "message": "Create New Category"
        })

@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watches = listing.watch.all()
    bids = Bid.objects.filter(listing=listing_id)
    maxbid = bids.last()
    comments = Comment.objects.filter(listing=listing_id).order_by('id')
    print(comments)
    #print(comments.reverse())

    addwatchlist = False
    if request.user != listing.user:
        for watch in watches:
            if watch == request.user:
                addwatchlist = True
                break
    else:
        addwatchlist = None

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "addwatchlist": addwatchlist,
        "numberOfBids": len(bids),
        "maxbid": maxbid,
        "comments": comments.reverse()
    })

@login_required
def placebid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        bidPost = float(request.POST["bid"])
        user = User.objects.get(username=request.user)
        bids = Bid.objects.filter(listing=listing_id)
        if bidPost > listing.bidprice:
            listing.bidprice = bidPost
            listing.save()
            bid = Bid(listing=listing, bidder=user, bidprice=bidPost)
            bid.save()
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            comments = Comment.objects.filter(listing=listing_id)
            maxbid = Bid.objects.filter(listing=listing_id).last()
            watches = listing.watch.all()
            addwatchlist = False
            if request.user != listing.user:
                for watch in watches:
                    if watch == request.user:
                        addwatchlist = True
                        break
            else:
                addwatchlist = None
            return render(request, "auctions/listing.html",{
                "listing": listing,
                "addwatchlist": addwatchlist,
                "numberOfBids": len(bids),
                "maxbidder": maxbid,
                "error_min_value": True,
                "comments": comments.reverse()
            })

@login_required
def closelisting(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.status = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required
def addwatchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user)
    listing.watch.add(user)
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required
def comment(request, listing_id):
    userField = request.user
    commentField = request.POST["comment"]
    listingField = Listing.objects.get(pk=listing_id)
    print(commentField)
    comment = Comment(listing=listingField, user=userField, comment=commentField)
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def watchlist(request):
    listings = Listing.objects.filter(watch=request.user).all
    return render(request, "auctions/index.html", {
        "title": "WatchList Listings",
        "listings": listings
    })

@login_required
def deletewatchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user)
    listing.watch.remove(user)
    return HttpResponseRedirect(reverse("watchlist"))


def category(request):
    if request.method == "POST":
        category = Category.objects.get(pk=int(request.POST["category"]))
        print(category)
        
        listings = Listing.objects.filter(category=category)
        return render(request, "auctions/category.html", {
            "categories": Category.objects.all(),
            "listings": listings.exclude(status=False)
        })

    else:
        
        return render(request, "auctions/category.html", {
            "categories": Category.objects.all()
        })