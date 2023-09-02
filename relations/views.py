from pyexpat.errors import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic

from relations.models import Friendship, FriendshipRequest
from wishlist.models import Wish


class FriendsOfUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing friends of current user.
    """
    model = Friendship
    template_name = 'relations/friends_of_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Friendship.objects.select_related("from_user"). \
            filter(to_user=self.request.user).order_by('from_user')


class FriendWishListView(LoginRequiredMixin, generic.ListView):
    model = Wish
    template_name = 'relations/friend_wish_list.html'
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        if 'book' in request.POST:
            book = request.POST['book']
            wish_object = get_object_or_404(Wish, pk=book)
            wish_object.booked_by = self.request.user
            wish_object.save()
            pk = self.kwargs['pk']
            return redirect('friend-wishes', pk=pk)

        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs['pk']
        friend_obj = get_object_or_404(User, pk=pk)
        queryset = queryset.filter(created_by=friend_obj)
        return queryset


class UserListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'relations/user_list.html'
    paginate_by = 10

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user.username).order_by('username')


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'relations/personal_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.get_object()
        friendship_exists = Friendship.objects.filter(from_user=self.request.user, to_user=user).exists()
        context['friendship_exists'] = friendship_exists
        request_exists = FriendshipRequest.objects.filter(from_user=self.request.user, to_user=user).exists()
        context['request_exists'] = request_exists

        return context

    def post(self, request, *args, **kwargs):
        if 'to_username' in request.POST:
            to_username = request.POST['to_username']
            if to_username != request.user.username:
                to_user = User.objects.get(username=to_username)
                from_user = request.user
                new_request = FriendshipRequest(from_user=from_user, to_user=to_user)
                new_request.save()
                return redirect('personal-page', pk=to_user.pk)
        return self.get(request, *args, **kwargs)


class FriendshipRequestListView(LoginRequiredMixin, generic.ListView):
    model = FriendshipRequest
    template_name = 'relations/friendship_requests.html'
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        if 'action' in request.POST:
            action = request.POST['action']
            friendship_request_id = request.POST['friendship_request_id']
            friendship_request = FriendshipRequest.objects.get(pk=friendship_request_id)

            if action == 'accept':
                FriendshipRequest.accept(friendship_request)
            elif action == 'reject':
                FriendshipRequest.reject(friendship_request)
            return redirect('friendship-requests')

        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        return FriendshipRequest.objects.filter(to_user=self.request.user, rejected=False).order_by('from_user')
