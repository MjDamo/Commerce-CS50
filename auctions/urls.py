from django.urls import path

from . import views

urlpatterns = [
    path("", views.ItemListView.as_view(), name="index"),
    # path("myacc", views.MyAccView.as_view(), name="myacc"),
    path("mylist", views.my_acc, name="my_acc"),
    path("mywin", views.my_acc, name="my_acc"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing, name="listing"),
    path('listing/<int:list_id>/', views.list_detail, name='list_detail'),
    path('listing/<int:list_id>/end/', views.bid_end, name='bid_end'),
    path('listing/<int:com_id>/del_comment/', views.comment_del, name='comment_del'),
    path('listing/<int:list_id>/add', views.add_watch, name='add_watch'),
    path('listing/<int:list_id>/rm', views.rm_watch, name='rm_watch'),
    path('listing/<int:list_id>/bid', views.bid_place, name='bid_place'),
    path('watch-list', views.watch_list, name='watch_list'),
    path('categories', views.category, name='category'),
    path('category-item/<int:cat_id>', views.category_select, name='category_item'),
    path("add_category", views.add_category, name="add_category"),
]
