from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST

from .models import User, Category, Listing
from .forms import ListingForm, AddCategory, CommentForm


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


# def listing(request):
#     if request.method == "POST":
#         title = request.POST['title']
#         description = request.POST['description']
#         auther = request.user
#         # category = Category.objects.create(request.POST['category'])
#         price = request.POST['price']
#         image_url = request.POST['image']
#
#         new_list = Listing(
#             title=title, description=description,
#             auther=auther,
#             price=price, imageUrl=image_url,
#             isActive=True
#         )
#         new_list.save()
#         return redirect('index')
#     else:
#         return render(request, "auctions/listing.html", {
#             "message": "Fuck",
#         })
#
#     return render(request, 'auctions/listing.html')

@login_required
def listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.auther = request.user
            new_list.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse("index"))
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


@require_POST
def list_comment(request, list_id):
    item_list = get_object_or_404(request, id=list_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.item = item_list
        comment.save()

        context = {
            'item_list': item_list,
            'form': form,
            'comment': comment,
        }
        return render(request, 'auctions/comment.html', context)

