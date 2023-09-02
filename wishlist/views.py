from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.models import User

from relations.models import Friendship
from .models import Category, Wish


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


class WishDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Wish

    def test_func(self):
        wish = self.get_object()
        return self.request.user == wish.created_by or Friendship.objects.filter(to_user=self.request.user,
                                                                                 from_user=wish.created_by).exists()


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


class WishCreate(LoginRequiredMixin, CreateView):
    model = Wish
    fields = ['title', 'summary', 'price', 'link', 'category']

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.created_by = self.request.user
        fields.save()
        return super().form_valid(form)


class WishUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Wish
    fields = ['summary', 'price', 'link', 'category']

    def test_func(self):
        wish = self.get_object()
        return self.request.user == wish.created_by


class WishDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Wish
    success_url = reverse_lazy('my-wishes')

    def test_func(self):
        wish = self.get_object()
        return self.request.user == wish.created_by


def change_status_booked(request, pk):
    wish = get_object_or_404(Wish, pk=pk)
    if request.method == 'POST':
        wish.booked_by = request.POST.get('Booked')
        wish.save()
    return render(request, 'relations/friend_wish_list.html')