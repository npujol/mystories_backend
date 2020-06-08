from django.db import models

from ..core.models import TimestampedModel


class Profile(TimestampedModel):
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False
    )

    favorites = models.ManyToManyField("histories.History", related_name="favorited_by")

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        """Follow `profile` if we're not already following `profile`."""
        self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow `profile` if we're already following `profile`."""
        self.follows.remove(profile)

    def is_following(self, profile):
        """Returns True if we're following `profile`; False otherwise."""
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        """Returns True if `profile` is following us; False otherwise."""
        return self.followed_by.filter(pk=profile.pk).exists()

    def favorite(self, history):
        """Favorite `history` if we haven't already favorited it."""
        self.favorites.add(history)

    def unfavorite(self, history):
        """Unfavorite `history` if we've already favorited it."""
        self.favorites.remove(history)

    def has_favorited(self, history):
        """Returns True if we have favorited `history`; else False."""
        return self.favorites.filter(pk=history.pk).exists()
