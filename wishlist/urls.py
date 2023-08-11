from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^wish/(?P<pk>\d+)$', views.WishDetailView.as_view(), name='wish-detail'),
    re_path(r'^categories/$', views.CategoryListView.as_view(), name='categories'),
    re_path(r'^mywishes/$', views.WishesByUserListView.as_view(), name='my-wishes'),
    re_path(r'^mybooked/$', views.BookedByUserListView.as_view(), name='my-booked'),
]

urlpatterns += [
    re_path(r'^wish/create/$', views.WishCreate.as_view(), name='wish-create'),
    re_path(r'^wish/(?P<pk>\d+)/update/$', views.WishUpdate.as_view(), name='wish-update'),
    re_path(r'^wish/(?P<pk>\d+)/delete/$', views.WishDelete.as_view(), name='wish-delete'),
]

urlpatterns += [
    re_path(r'^friends/$', views.FriendsOfUserListView.as_view(), name='my-friends'),
    re_path(r'^friends/(?P<pk>\d+)/$', views.FriendWishListView.as_view(), name='friend-wishes')
]
