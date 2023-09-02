from django.contrib import admin
from .models import FriendshipRequest, Friendship

from django.contrib import admin

class ReadOnlyModelAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

# Register your models here.
admin.site.register(FriendshipRequest, ReadOnlyModelAdmin)
admin.site.register(Friendship, ReadOnlyModelAdmin)