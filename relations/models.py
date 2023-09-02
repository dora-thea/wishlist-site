from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class FriendshipRequest(models.Model):
    """
    Model representing friendship requests.
    """
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_send')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_received')
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user.username} send the request to {self.to_user.username}"

    def accept(self):
        # double-sided relationships
        Friendship.objects.create(from_user=self.from_user, to_user=self.to_user)
        Friendship.objects.create(from_user=self.to_user, to_user=self.from_user)

        # delete requests
        self.delete()
        FriendshipRequest.objects.filter(from_user=self.to_user, to_user=self.from_user).delete()

    def reject(self):
        self.rejected = True
        self.save()
        return True

    def cancel(self):
        self.delete()
        return True


class Friendship(models.Model):
    """
    Model representing friendships.
    """
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='_unused')

    def __str__(self):
        return f"{self.to_user.username} is friends with {self.from_user.username}"

    def save(self, *args, **kwargs):
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super().save(*args, **kwargs)
