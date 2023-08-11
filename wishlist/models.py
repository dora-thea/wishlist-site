from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Model representing a wish category (e.g. Clothes, Jewellery).
    """
    name = models.CharField(max_length=200, help_text="Enter a wish category (e.g. Clothes, Jewellery etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Wish(models.Model):
    """
    Model representing a wish.
    """
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='created_wishes')
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the wish")
    price = models.FloatField(default=0)
    link = models.URLField(max_length=200, null=True)
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None,
                                  related_name='booked_wishes')
    category = models.ManyToManyField(Category, help_text="Select a category for this wish")

    # ManyToManyField used because category can contain many wishes. Wishes can cover many categories.
    # Category class has already been defined, so we can specify the object above.

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def save(self, *args, **kwargs):
        if not self.created_by_id:
            self.created_by = kwargs.pop('created_by', None)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('wish-detail', args=[str(self.id)])

    def display_category(self):
        """
        Creates a string for the Category. This is required to display category in Admin.
        """
        return ', '.join([category.name for category in self.category.all()[:3]])

    display_category.short_description = 'Category'


class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"
