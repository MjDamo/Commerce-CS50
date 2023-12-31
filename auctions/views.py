from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
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
    paginate_by = 4
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

            if highest_bid is None or bid_in_dec > highest_bid.bid and (item.isActive == True):
                Bid.objects.create(user=user, item_bid=item, bid=bid_in)
                return redirect('list_detail', list_id=list_id)
            elif not item.isActive:
                return render(request, 'auctions/detail-alarm.html', context={
                    'massage': "This auction is close!"
                })

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
    comments = item.item_comment.all()
    try:
        watch = Watchlist.objects.filter(user=request.user, item=item)
    except:
        watch = None
    try:
        last_bid = Bid.objects.filter(item_bid=item).order_by('-bid_date').first()
    except:
        last_bid = 0
    user = request.user
    win = False
    if last_bid and not item.isActive:
        if last_bid.user == user:
            win = True

    if request.method == 'POST':
        com_form = CommentForm(request.POST)
        if com_form.is_valid():
            com = com_form.save(commit=False)
            com.item = item
            com.auther = user
            com.save()
            return redirect('list_detail', list_id=item.pk)
        else:
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    contex = {
        "item": item,
        'user': request.user,
        'comments': comments,
        'comment': comment_form,
        'com_form': CommentForm(),
        'last_bid': last_bid,
        'win': win,
        'watch': watch
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
    high_bid = Bid.objects.filter(item_bid=item).order_by('-bid').first()
    if item.auther == request.user:
        item.isActive = False
        if high_bid:
            item.winner = high_bid.user
            item.highest_bidder = high_bid.user
            item.bid = Decimal(high_bid.bid)
            item.save()
        item.save()
        if Decimal(high_bid.bid) < Decimal(item.price):
            item.highest_bidder = request.user
            item.winner = request.user
            item.save()
    return redirect('list_detail', list_id=item.pk)


@login_required
def add_watch(request, list_id):
    if request.method == 'POST':
        item = Listing.objects.get(pk=list_id)
        add_item = Watchlist(user=request.user, item=item)
        add_item.save()
    return HttpResponseRedirect(reverse('list_detail', args=[list_id]))


@login_required
def rm_watch(request, list_id):
    item = get_object_or_404(Listing, pk=list_id)
    Watchlist.objects.filter(item=item).delete()
    return HttpResponseRedirect(reverse('list_detail', args=[list_id]))


@login_required
def watch_list(request):
    items = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watch-list.html',
                  context={
                      'items': items,
                  })


@login_required
def my_acc(request):
    items = Listing.objects.filter(auther=request.user).all()
    return render(request, 'auctions/mylist.html',
                  context={
                      'items': items,
                  })


@login_required
def my_win(request):
    items = Listing.objects.filter(isActive=False).all()
    win = items.filter(winner=request.user).all()
    return render(request, 'auctions/mywin.html',
                  context={
                      'all_win': win,
                  })

