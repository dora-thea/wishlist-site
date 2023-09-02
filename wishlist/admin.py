from django.contrib import admin
from .models import Category, Wish

# Register your models here.
admin.site.register(Category)


# Register the Admin classes for Book using the decorator
@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'title', 'price', 'display_category', 'booked_by')
    list_filter = ('price', 'booked_by', 'created_by')
    fields = ['created_by', ('title', 'booked_by'), 'summary', ('price', 'link'), 'category']
