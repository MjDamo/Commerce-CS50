from django.urls import path

from . import views

urlpatterns = [
    path("", views.ItemListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing, name="listing"),
    path('listing/<int:list_id>/', views.list_detail, name='list_detail'),
    path('listing/<int:list_id>/', views.add_watch, name='add_watch'),
    path('listing/<int:list_id>/', views.rm_watch, name='rm_watch'),
    path('listing/<int:list_id>/', views.watch_list, name='watch_list'),
    path('watch-list', views.watch_list, name='watch_list'),
    path("add_category", views.add_category, name="add_category"),
]
