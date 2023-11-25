from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from decimal import Decimal

from .models import User, Category, Listing, Comment, Bid, Watchlist
from .forms import ListingForm, AddCategory, CommentForm, BidForm


def index(request):
    return render(request, "auctions/index.html", {
        "active": Listing.objects.filter(isActive=True),
        "closed": Listing.objects.filter(isActive=False)
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
def listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.auther = request.user
            new_list.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse("listing"))
    else:
        return render(request, 'auctions/listing.html', {
            'form': ListingForm(),
            'category': AddCategory(),
        })
    return render(request, 'auctions/listing.html', {
        'form': form,
        'category': AddCategory(),
    })


@login_required
def add_category(request):
    if request.method == "POST":
        category = AddCategory(request.POST)
        if category.is_valid():
            category.save()
            return render(request, "auctions/listing.html", {
                "form": ListingForm(),
                "category": AddCategory(),
                "message": "Created Successful!"
            })
        else:
            return render(request, "auctions/listing.html", {
                "form": ListingForm(),
                "category": AddCategory(),
                "message": "Already Exists."
            })


class ItemListView(ListView):
    queryset = Listing.objects.filter(isActive=True)
    context_object_name = 'list'
    paginate_by = 2
    template_name = 'auctions/index.html'


@login_required
def bid_place(request, list_id):
    if request.method == 'POST':
        bid_in = request.POST.get('bid_in')
        user = request.user
        item = get_object_or_404(Listing, pk=list_id)
        bid_in_dec = Decimal(bid_in)

        if bid_in_dec >= item.price:
            highest_bid = Bid.objects.filter(item_bid=item).order_by('-bid').first()

            if highest_bid is None or bid_in_dec > highest_bid.bid:
                Bid.objects.create(bidder=user, item_bid=item, bid=bid_in)
                return redirect('list_detail', list_id=list_id)
            else:
                return render(request, 'auctions/detail-alarm.html', context={
                    'massage': "Your bid most be greader than latest bid!"
                })
        else:
            return render(request, 'auctions/detail-alarm.html', context={
                'massage': "Your bid most be greader or equal price!"
            })
    else:
        return render(request, 'auctions/detail-alarm.html', context={
            'massage': "Wrong value...!"
        })


def list_detail(request, list_id):
    item = get_object_or_404(Listing, pk=list_id)
    comments = Comment.objects.filter(item=item)
    last_bid = Bid.objects.filter(item_bid=item).order_by('bid_date').last()
    user = request.user
    win = False
    if not item.isActive:
        if last_bid and last_bid.bidder == user:
            win = True

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comments = form.save(commit=False)
            comments.item = item
            comments.auther = user
            comments.save()
            return redirect('list_detail', list_id=item.pk)
    else:
        comment = CommentForm()

    contex = {
        "item": item,
        'comments': comments,
        'comment': comment,
        'last_bid': last_bid,
        'win': win,
    }
    return render(request, 'auctions/detail.html', contex)


@login_required
def comment_del(request, com_id):
    comment = get_object_or_404(Comment, pk=com_id)
    if comment.auther == request.user:
        comment.delete()
    return redirect('list_detail', list_id=comment.item.pk)


def category(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html',
                  context={
                      'categories': categories,
                  })


def category_select(request, cat_id):
    cat = get_object_or_404(Category, pk=cat_id)
    items = cat.category.filter(isActive=True)
    return render(request, 'auctions/category-item.html',
                  context={
                      'category': cat,
                      'items': items,
                  })


@login_required
def bid_end(request, list_id):
    item = get_object_or_404(Listing, pk=list_id)
    if item.auther == request.user:
        item.isActive = False
        item.save()
        bid = item.bid
        if 0 < bid:
            item.highest_bidder = request.user
            item.save()
    return redirect('list_detail', list_id=item.pk)


@login_required
def add_watch(request, list_id):
    item = get_object_or_404(Listing, pk=list_id)
    Watchlist.objects.create(user=request.user, item=item)
    return redirect('list_detail', list_id=item.pk)


@login_required
def rm_watch(request, list_id):
    item = get_object_or_404(Listing, pk=list_id)
    Watchlist.delete(item.pk)
    return redirect('list_detail', list_id=item.pk)


@login_required
def watch_list(request):
    items = Watchlist.objects.filter('item').all()
    return render(request, 'auctions/watch-list.html',
                  context={
                      'items': items,
                  })


