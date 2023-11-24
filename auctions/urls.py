from django.urls import path

from . import views

urlpatterns = [
    path("", views.ItemListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing, name="listing"),
    path('listing/<int:list_id>/', views.list_detail, name='list_detail'),
    path('listing/<int:list_id>/', views.bid_place, name='bid_place'),
    path("add_category", views.add_category, name="add_category"),
]
