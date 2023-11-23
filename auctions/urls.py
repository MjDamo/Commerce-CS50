from django.urls import path

from . import views

urlpatterns = [
    path("", views.ItemListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing, name="listing"),
    path("add_category", views.add_category, name="add_category"),
]
