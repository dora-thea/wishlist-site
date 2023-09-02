from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^friends/$', views.FriendsOfUserListView.as_view(), name='my-friends'),
    re_path(r'^friends/(?P<pk>\d+)/$', views.FriendWishListView.as_view(), name='friend-wishes'),
    re_path(r'^users/$', views.UserListView.as_view(), name='all-users'),
    re_path(r'^users/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='personal-page'),
    re_path(r'^friendshiprequests/$', views.FriendshipRequestListView.as_view(), name='friendship-requests'),
]