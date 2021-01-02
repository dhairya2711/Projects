from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionList, Bid, Comment, WatchList, Catagory


def index(request):
    if request.method == "POST":
        ac = request.POST.get("addedCatagory")
        newc = Catagory(catagory=str(ac))
        newc.save()

    cat = Catagory.objects.all()
    auctionlist = AuctionList.objects.filter(status = True).all()
    bidlist = []
    for a in auctionlist:
        bidlist.append(Bid.objects.get(auction = a))
    list = []
    for i in range(0, len(auctionlist)):
        list.append({"item": auctionlist[i], "bid": bidlist[i]})

    return render(request, "auctions/index.html", {"title": "Index", "list": list, "cat": cat})


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
        make_watchList = WatchList(user = user)
        make_watchList.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_list(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST.get("title")
            discription = request.POST.get("discription")
            bid = request.POST.get("bid")
            img_url = (request.POST.get("image_url"))
            if len(img_url) == 0:
                image_url = "data:image/png;base64,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"
            else:
                image_url = img_url
            catagory = request.POST.get("catagory")
            user = User.objects.get(username=request.user.get_username())
            cat = Catagory.objects.get(catagory=catagory)
            item = AuctionList(user=user, title=title, discription=discription, img_url=image_url, status=True,
                               catagory=cat)
            item.save()
            bid = Bid(auction=item, bid=bid, bidder_name=user)
            bid.save()
            return HttpResponseRedirect(reverse('index'))

        catagories = Catagory.objects.all()
        return render(request, "auctions/CreateList.html", {"catagories": catagories})
    else:
        return render(request, "auctions/ifNotLoggedIn.html")


def details(request, txt):
    if str(txt) == str(None):
        pass
    else:
        logged_in = str(request.user.is_authenticated)
        object = AuctionList.objects.get(pk=int(txt))
        if request.method == "POST":
            newBidder = request.user.username
            user = User.objects.get(username = newBidder)
            newBid = request.POST.get("newBid")
            b = Bid.objects.get(auction = object)
            if int(newBid) > int(b.bid):
                BidItem = Bid.objects.get(auction=object)
                BidItem.bid = newBid
                BidItem.bidder_name = user
                BidItem.save()

        in_watchlist = False
        if logged_in == True:
            wlist = WatchList.objects.get(request.user.username)
            items = AuctionList.objects.filter(items=wlist).all()
            for i in items:
                if i.pk == int(txt):
                    in_watchlist = True

        status = object.status
        bid = Bid.objects.get(auction = object)
        comments = Comment.objects.filter(item=object).all()
        return render(request, "auctions/detailsPage.html", {"object": object,
                "bid": bid, "comments": comments, "logged_in": logged_in, "WatchList": str(in_watchlist), "status": str(status)})


def catagory(request, catagory):
    if str(catagory) == "all":
        return HttpResponseRedirect(reverse('index'))
    else:
        cat = Catagory.objects.get(catagory=catagory)
        object = AuctionList.objects.filter(catagory=cat.pk).all()
        bids = []
        for o in object:
            bids.append(Bid.objects.get(auction=o))
        list = []
        for i in range(0, len(object)):
            list.append({"item": object[i], "bid": bids[i]})
        cat = Catagory.objects.all()
        return render(request, "auctions/index.html", {"title": "Category Page", "list": list, "cat": cat})


def add_to_watchList(request):
    if request.method == "POST":
        remove = request.POST.get("remove")
        user_name = request.POST.get("user_name")
        auction_id = request.POST.get("auction_id")
        user = User.objects.get(username = user_name)
        auction = AuctionList.objects.get(pk= auction_id)
        if remove == "yes":
            w = WatchList.objects.get(user = user)
            w.auction.remove(auction)
        elif remove == "no":
            try:
                w = WatchList.objects.get(user=user)
                w.auction.add(auction)
            except:
                w = WatchList(user=user)
                w.save()
                w.auction.add(auction)
    return HttpResponseRedirect(reverse('watchList'))


def addComment(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        auction_id = request.POST.get("auction_id")
        comment = request.POST.get("addComment")
        user = User.objects.get(username = user_name)
        auction = AuctionList.objects.get(pk = auction_id)
        com = Comment(item = auction, comment_name = user, comment = comment)
        com.save()
        return HttpResponseRedirect(reverse('details' ,args=[auction_id]))
    else:
        return HttpResponse("This URL doesn't exist.")


def watchList(request):
    try:
        try:
            user_name = request.user.username
            u = User.objects.get(username=user_name)
            wlist = WatchList.objects.get(user=u)
            items = AuctionList.objects.filter(items=wlist).all()

            bidlist = []
            for a in items:
                bidlist.append(Bid.objects.get(auction=a))
            list = []
            for i in range(0, len(items)):
                list.append({"item": items[i], "bid": bidlist[i]})

            print(list)
            return render(request, "auctions/WatchList.html", {"list": list})
        except WatchList.DoesNotExist:
            return render(request, "auctions/WatchList.html")

    except User.DoesNotExist:
        raise Http404("Please log in")

def clostList(request):
    id = request.POST.get("item_id")
    item = AuctionList.objects.get(id = int(id))
    item.status = False
    item.save()
    return HttpResponseRedirect(reverse('details', args=[int(id)]))


def closedList(request):
    cat = Catagory.objects.all()
    auctionlist = AuctionList.objects.filter(status=False).all()
    bidlist = []
    for a in auctionlist:
        bidlist.append(Bid.objects.get(auction=a))
    list = []
    for i in range(0, len(auctionlist)):
        list.append({"item": auctionlist[i], "bid": bidlist[i]})
    return render(request, "auctions/index.html", {"title": "Closed Lists", "list": list, "cat": cat, "status": "Falsepython "})
