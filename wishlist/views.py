from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Category, Wish, Friendship


def index(request):
    """
    Display function for the home page of the site.
    """
    num_wishes = Wish.objects.all().count()
    num_categories = Category.objects.all().count()

    return render(
        request,
        'index.html',
        context={'num_wishes': num_wishes, 'num_categories': num_categories},
    )


class WishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Wish


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    paginate_by = 15


class FriendWishListView(generic.ListView):
    model = Wish
    template_name = 'wishlist/friend_wish_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs['pk']
        friend_obj = get_object_or_404(Friendship, pk=pk).user
        queryset = queryset.filter(created_by=friend_obj)
        return queryset


class WishesByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing wishes of current user.
    """
    model = Wish
    template_name = 'wishlist/wish_list_of_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Wish.objects.filter(created_by=self.request.user).order_by('price')


class BookedByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing booked of current user.
    """
    model = Wish
    template_name = 'wishlist/booked_by_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Wish.objects.filter(booked_by=self.request.user).order_by('price')


class FriendsOfUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing friends of current user.
    """
    model = Friendship
    template_name = 'wishlist/friends_of_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Friendship.objects.filter(friend=self.request.user)


class WishCreate(LoginRequiredMixin, CreateView):
    model = Wish
    fields = ['title', 'summary', 'price', 'link', 'category']

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.created_by = self.request.user
        fields.save()
        return super().form_valid(form)


class WishUpdate(LoginRequiredMixin, UpdateView):
    model = Wish
    fields = ['summary', 'price', 'link', 'category']


def change_status_booked(request, pk):
    wish = get_object_or_404(Wish, pk=pk)
    if request.method == 'POST':
        wish.booked_by = request.POST.get('Booked')
        wish.save()
    return render(request, 'wishlist/friend_wish_list.html')


class WishDelete(LoginRequiredMixin, DeleteView):
    model = Wish
    success_url = reverse_lazy('my-wishes')
